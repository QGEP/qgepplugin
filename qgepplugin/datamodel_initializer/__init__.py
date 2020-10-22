import os
import tempfile
import hashlib
import zipfile
import subprocess
import pkg_resources
import site
import importlib

from qgis.PyQt.QtCore import QUrl, QFile, QIODevice
from qgis.PyQt.QtNetwork import QNetworkRequest
from qgis.core import QgsNetworkAccessManager, QgsFeedback, QgsMessageLog, Qgis, QgsProject


# Basic config
DATAMODEL_RELEASE = '1.5.2'
QGEP_RELEASE = '8.0'

# Derived urls/paths, may require adaptations if release structure changes
DATAMODEL_RELEASE_URL = f'https://github.com/QGEP/datamodel/archive/v{DATAMODEL_RELEASE}.zip'
QGEP_RELEASE_URL = f'https://github.com/QGEP/QGEP/releases/download/v{QGEP_RELEASE}/qgep.zip'
hash = hashlib.md5((DATAMODEL_RELEASE_URL + QGEP_RELEASE_URL).encode('utf-8')).hexdigest()[0:8]
RELEASE_DIR = os.path.join(tempfile.gettempdir(), 'QGEP', hash)
QGIS_PROJECT_PATH = os.path.join(RELEASE_DIR, 'project', 'qgep.qgs')
DATAMODEL_DIR = os.path.join(RELEASE_DIR, f'datamodel-{DATAMODEL_RELEASE}')
REQUIREMENTS_PATH = os.path.join(DATAMODEL_DIR, 'requirements.txt')
DATAMODEL_DELTAS_DIR = os.path.join(DATAMODEL_DIR, "delta")


class QGEPDatamodelError(Exception):
    pass


def _run_cmd(shell_command, cwd=None, error_message='Subprocess error, see logs for more information'):
    """
    Helper to run commands through subprocess
    """
    QgsMessageLog.logMessage(f"Running command : {shell_command}", "QGEP")
    result = subprocess.run(shell_command, cwd=cwd, shell=True, capture_output=True)
    if result.stdout:
        QgsMessageLog.logMessage(result.stdout.decode(), "QGEP")
    if result.stderr:
        QgsMessageLog.logMessage(result.stderr.decode(), "QGEP", level=Qgis.Critical)
    if result.returncode:
        raise QGEPDatamodelError(error_message)
    return result.stdout.decode()


def check_release_exists():
    return os.path.exists(QGIS_PROJECT_PATH) and os.path.exists(DATAMODEL_DIR)


def check_python_requirements():
    return len(missing_python_requirements()) == 0


def missing_python_requirements():
    # see https://stackoverflow.com/a/45474387/13690651

    missing = []
    if not os.path.exists(REQUIREMENTS_PATH):
        missing.append(('unknown', 'requirements not found'))
    else:
        requirements = pkg_resources.parse_requirements(open(REQUIREMENTS_PATH))
        for requirement in requirements:
            try:
                pkg_resources.require(str(requirement))
            except pkg_resources.DistributionNotFound:
                missing.append((requirement, 'missing'))
            except pkg_resources.VersionConflict:
                missing.append((requirement, 'conflict'))
    return missing


def install_deps():

    network_manager = QgsNetworkAccessManager.instance()
    feedback = QgsFeedback()

    # Download the files if needed

    if check_release_exists():
        QgsMessageLog.logMessage(f"Required files are already present in {RELEASE_DIR}", "QGEP")

    else:
        os.makedirs(RELEASE_DIR, exist_ok=True)

        # Download datamodel
        QgsMessageLog.logMessage(f"Downloading {DATAMODEL_RELEASE_URL} to {RELEASE_DIR}", "QGEP")
        reply = network_manager.blockingGet(QNetworkRequest(QUrl(DATAMODEL_RELEASE_URL)), feedback=feedback)
        datamodel_file = QFile(os.path.join(RELEASE_DIR, 'datamodel.zip'))
        datamodel_file.open(QIODevice.WriteOnly)
        datamodel_file.write(reply.content())
        datamodel_file.close()

        # Download QGEP
        QgsMessageLog.logMessage(f"Downloading {QGEP_RELEASE_URL} to {RELEASE_DIR}", "QGEP")
        reply = network_manager.blockingGet(QNetworkRequest(QUrl(QGEP_RELEASE_URL)), feedback=feedback)
        qgep_file = QFile(os.path.join(RELEASE_DIR, 'qgep.zip'))
        qgep_file.open(QIODevice.WriteOnly)
        qgep_file.write(reply.content())
        qgep_file.close()

        QgsMessageLog.logMessage(f"Extracting files to {RELEASE_DIR}", "QGEP")

        # Unzip datamodel
        datamodel_zip = zipfile.ZipFile(datamodel_file.fileName())
        datamodel_zip.extractall(RELEASE_DIR)

        # Unzip QGEP
        qgep_zip = zipfile.ZipFile(qgep_file.fileName())
        qgep_zip.extractall(RELEASE_DIR)

    # TODO : Ideally, this should be done in a venv, as to avoid permission issues and/or modification
    # of libraries versions that could affect other parts of the system.
    # We could initialize a venv in the user's directory, and activate it.
    # It's almost doable when only running commands from the command line (in which case we could
    # just prepent something like `path/to/venv/Scripts/activate && ` to commands, /!\ syntax differs on Windows),
    # but to be really useful, it would be best to then enable the virtualenv from within python directly.
    # It seems venv doesn't provide a way to do so, while virtualenv does
    # (see https://stackoverflow.com/a/33637378/13690651)
    # but virtualenv isn't in the stdlib... So we'd have to install it globally ! Argh...
    # Anyway, pip deps support should be done in QGIS one day so all plugins can benefit.
    # In the mean time we just install globally and hope for the best.

    # Install dependencies
    QgsMessageLog.logMessage(f"Installing python dependencies from {REQUIREMENTS_PATH}", "QGEP")
    _run_cmd(f'pip install -r {REQUIREMENTS_PATH}', error_message='Could not install python dependencies')

    # Refresh paths
    importlib.reload(site)


def get_current_version():
    if not os.path.exists(DATAMODEL_DELTAS_DIR):
        return None

    pum_info = _run_cmd(
        f'pum info -p pg_qgep -t qgep_sys.pum_info -d {DATAMODEL_DELTAS_DIR}',
        error_message='Could not get current version, are you sure the database is accessible ?'
    )
    for line in pum_info.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split('|')
        if len(parts) > 1:
            version = parts[1].strip()
    return version


def get_available_versions():
    # TODO : this should be done by PUM directly (see https://github.com/opengisch/pum/issues/94)

    if not os.path.exists(DATAMODEL_DELTAS_DIR):
        return []

    versions = set()
    for f in os.listdir(DATAMODEL_DELTAS_DIR):
        if not os.path.isfile(os.path.join(DATAMODEL_DELTAS_DIR, f)):
            continue
        if not f.startswith('delta_'):
            continue
        parts = f.split('_')
        versions.add(parts[1])
    return sorted(list(versions))


def upgrade_version(version, srid):
    return _run_cmd(
        f'pum upgrade -p pg_qgep -t qgep_sys.pum_info -d {DATAMODEL_DELTAS_DIR} -u {version} -v int SRID {srid}',
        cwd=os.path.dirname(DATAMODEL_DELTAS_DIR),
        error_message='Errors when upgrading the database. Consult logs for more information.'
    )


def load_project():
    QgsProject.instance().read(QGIS_PROJECT_PATH)
