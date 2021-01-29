from pkg_resources import parse_version
from types import SimpleNamespace

from qgis.utils import plugins
from qgis.core import Qgis

from .. import interlis


def configure_from_modelbaker(iface):
    """
    Configures interlis.config.JAVA/ILI2PG paths using modelbaker.
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
    config = ili2dbconfig.BaseConfiguration()

    stdout = SimpleNamespace()
    stdout.emit = print

    interlis.config.JAVA = ili2dbutils.get_java_path(config)
    interlis.config.ILI2PG = ili2dbutils.get_ili2db_bin(globals.DbIliMode.ili2pg, 4, print, print)

    return True
