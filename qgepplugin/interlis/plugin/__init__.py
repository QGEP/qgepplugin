from pkg_resources import parse_version
from types import SimpleNamespace

from qgis.utils import plugins
from qgis.core import Qgis

import os

from qgis.PyQt.QtWidgets import QApplication, QFileDialog, QProgressDialog

from qgis.core import QgsProject, QgsSettings

from QgisModelBaker.libili2db import ili2dbutils, ili2dbconfig, globals

from ..qgep.import_ import qgep_import
from ..qgep.export import qgep_export
from .gui import Gui

from .. import config
from ..utils.ili2db import create_ili_schema, import_xtf_data, export_xtf_data

import_dialog = None

def action_import(plugin):
    """
    Is executed when the user clicks the importAction tool
    """
    global import_dialog  # avoid garbage collection

    if not configure_from_modelbaker(plugin.iface):
        return

    default_folder = QgsSettings().value('qgep_pluging/last_interlis_path', QgsProject.instance().absolutePath())
    file_name, _ = QFileDialog.getOpenFileName(
        None, plugin.tr("Import file"), default_folder, plugin.tr("Interlis transfer files (*.xtf)")
    )
    if not file_name:
        # Operation canceled
        return
    QgsSettings().setValue('qgep_pluging/last_interlis_path', os.path.dirname(file_name))

    progress_dialog = QProgressDialog("", "", 0, 100, plugin.iface.mainWindow())
    progress_dialog.setCancelButton(None)
    progress_dialog.setModal(True)
    progress_dialog.show()

    # Validating the input file
    progress_dialog.setLabelText("Validating the input file...")
    QApplication.processEvents()
    try:
        validate_xtf_data(file_name)
    except Exception:
        progress_dialog.close()
        QMessageBox.critical(None, "Invalid file", "The selected file is not a valid XTF file. Open the logs for more details on the error.")
        return

    # Prepare the temporary ili2pg model
    progress_dialog.setLabelText("Creating ili schema...")
    QApplication.processEvents()
    create_ili_schema(config.ABWASSER_SCHEMA, config.ABWASSER_ILI_MODEL, recreate_schema=True)
    progress_dialog.setValue(33)

    # Export from ili2pg model to file
    progress_dialog.setLabelText("Importing XTF data...")
    QApplication.processEvents()
    import_xtf_data(config.ABWASSER_SCHEMA, file_name)
    progress_dialog.setValue(66)

    # Export to the temporary ili2pg model
    progress_dialog.setLabelText("Converting to QGEP...")
    QApplication.processEvents()
    import_dialog = Gui(plugin.iface.mainWindow())
    progress_dialog.setValue(100)
    qgep_import(precommit_callback=import_dialog.init_with_session)


def action_export(plugin):
    """
    Is executed when the user clicks the exportAction tool
    """
    if not configure_from_modelbaker(plugin.iface):
        return

    default_folder = QgsSettings().value('qgep_pluging/last_interlis_path', QgsProject.instance().absolutePath())
    file_name, _ = QFileDialog.getSaveFileName(
        None, plugin.tr("Export to file"), os.path.join(default_folder, 'qgep-export.xtf'), plugin.tr("Interlis transfer files (*.xtf)")
    )
    if not file_name:
        # Operation canceled
        return
    QgsSettings().setValue('qgep_pluging/last_interlis_path', os.path.dirname(file_name))

    progress_dialog = QProgressDialog("", "", 0, 100, plugin.iface.mainWindow())
    progress_dialog.setCancelButton(None)
    progress_dialog.setModal(True)
    progress_dialog.show()

    # Prepare the temporary ili2pg model
    progress_dialog.setLabelText("Creating ili schema...")
    QApplication.processEvents()
    create_ili_schema(config.ABWASSER_SCHEMA, config.ABWASSER_ILI_MODEL, recreate_schema=True)
    progress_dialog.setValue(33)

    # Export to the temporary ili2pg model
    progress_dialog.setLabelText("Converting from QGEP...")
    QApplication.processEvents()
    qgep_export()
    progress_dialog.setValue(66)

    # Export from ili2pg model to file
    progress_dialog.setLabelText("Saving XTF file...")
    QApplication.processEvents()
    export_xtf_data(config.ABWASSER_SCHEMA, config.ABWASSER_ILI_MODEL_NAME, file_name)
    progress_dialog.setValue(100)

    plugin.iface.messageBar().pushMessage("Sucess", f"Data successfully exported to {file_name}", level=Qgis.Success)


def configure_from_modelbaker(iface):
    """
    Configures config.JAVA/ILI2PG paths using modelbaker.
    Returns whether modelbaker is available, and displays instructions if not.
    """
    REQUIRED_VERSION = 'v6.4.0'  # TODO : update once https://github.com/opengisch/QgisModelBaker/pull/473 is released
    modelbaker = plugins.get('QgisModelBaker')
    if modelbaker is None:
        iface.messageBar().pushMessage(
            "Error",
            "This feature requires the ModelBaker plugin. Please install and activate it from the plugin manager.",
            level=Qgis.Critical
        )
        return False

    elif modelbaker.__version__ != 'dev' and parse_version(modelbaker.__version__) < parse_version(REQUIRED_VERSION):
        iface.messageBar().pushMessage(
            "Error",
            f"This feature requires a more recent version of the ModelBaker plugin (currently : {modelbaker.__version__}). Please install and activate version {REQUIRED_VERSION} or newer from the plugin manager.",
            level=Qgis.Critical
        )
        return False

    # We reuse modelbaker's logic to get the java path and ili2pg executables from withing QGIS
    # Maybe we could reuse even more (IliExecutable...) ?

    stdout = SimpleNamespace()
    stdout.emit = print

    config.JAVA = ili2dbutils.get_java_path(ili2dbconfig.BaseConfiguration())
    config.ILI2PG = ili2dbutils.get_ili2db_bin(globals.DbIliMode.ili2pg, 4, stdout, stdout)

    return True
