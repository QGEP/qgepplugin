from pkg_resources import parse_version
from types import SimpleNamespace

from qgis.utils import plugins
from qgis.core import Qgis

import os

from qgis.PyQt.QtWidgets import QApplication, QFileDialog, QProgressDialog

from qgis.core import QgsProject, QgsSettings

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

    # Prepare the temporary ili2pg model
    progress_dialog.setLabelText("Creating ili schema...")
    progress_dialog.setValue(0)
    QApplication.processEvents()
    create_ili_schema(config.ABWASSER_SCHEMA, config.ABWASSER_ILI_MODEL, recreate_schema=True)
    # Export from ili2pg model to file
    progress_dialog.setLabelText("Importing XTF data...")
    progress_dialog.setValue(50)
    QApplication.processEvents()
    import_xtf_data(config.ABWASSER_SCHEMA, file_name)
    # Export to the temporary ili2pg model
    progress_dialog.setLabelText("Converting to QGEP...")
    progress_dialog.setValue(100)
    QApplication.processEvents()
    import_dialog = Gui(plugin.iface.mainWindow())
    from ..qgep.import_ import import_
    import_(precommit_callback=import_dialog.init_with_session)


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

    # Prepare the temporary ili2pg model
    create_ili_schema(config.ABWASSER_SCHEMA, config.ABWASSER_ILI_MODEL, recreate_schema=True)
    # Export to the temporary ili2pg model
    from ..qgep.export import export
    export()
    # Export from ili2pg model to file
    export_xtf_data(config.ABWASSER_SCHEMA, config.ABWASSER_ILI_MODEL_NAME, file_name)


def configure_from_modelbaker(iface):
    """
    Configures config.JAVA/ILI2PG paths using modelbaker.
    Returns whether modelbaker is available, and displays instructions if not.
    """
    REQUIRED_VERSION = 'v6.2.0'
    modelbaker = plugins.get('QgisModelBaker')
    if modelbaker is None:
        iface.messageBar().pushMessage(
            "Error",
            "This feature requires the ModelBaker plugin. Please install and activate it from the plugin manager.",
            level=Qgis.Critical
        )
        return False

    elif parse_version(modelbaker.__version__) < parse_version(REQUIRED_VERSION):
        iface.messageBar().pushMessage(
            "Error",
            f"This feature requires a more recent version of the ModelBaker plugin. Please install and activate version {REQUIRED_VERSION} or newer from the plugin manager.",
            level=Qgis.Critical
        )
        return False

    # We reuse modelbaker's logic to get the java path and ili2pg executables from withing QGIS
    # Maybe we could reuse even more (IliExecutable...) ?
    from QgisModelBaker.libili2db import ili2dbutils, ili2dbconfig, globals

    stdout = SimpleNamespace()
    stdout.emit = print

    config.JAVA = ili2dbutils.get_java_path(ili2dbconfig.BaseConfiguration())
    config.ILI2PG = ili2dbutils.get_ili2db_bin(globals.DbIliMode.ili2pg, 4, print, print)

    return True
