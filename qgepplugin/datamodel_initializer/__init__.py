import os
import tempfile
import hashlib
import zipfile
import subprocess
import pkg_resources
import site
import importlib
import configparser
import psycopg2

from qgis.PyQt.QtCore import QUrl, QFile, QIODevice
from qgis.PyQt.QtNetwork import QNetworkRequest
from qgis.core import QgsNetworkAccessManager, QgsMessageLog, Qgis, QgsProject


# Basic config
MAIN_DATAMODEL_RELEASE = '1.5.2'
QGEP_RELEASE = '8.0'
TEMP_DIR = os.path.join(tempfile.gettempdir(), 'QGEP', 'datamodel-init')

# Path for pg_service.conf
if os.environ.get('PGSERVICEFILE'):
    PG_CONFIG_PATH = os.environ.get('PGSERVICEFILE')
elif os.environ.get('PGSYSCONFDIR'):
    PG_CONFIG_PATH = os.path.join(os.environ.get('PGSYSCONFDIR'), 'pg_service.conf')
else:
    PG_CONFIG_PATH = ' ~/.pg_service.conf'

# Derived urls/paths, may require adaptations if release structure changes
MAIN_DATAMODEL_RELEASE_URL = f'https://github.com/QGEP/datamodel/archive/{MAIN_DATAMODEL_RELEASE}.zip'
QGEP_RELEASE_URL = f'https://github.com/QGEP/QGEP/releases/download/v{QGEP_RELEASE}/qgep.zip'  # TODO : we should download the release according the the current datamodel version, not the latest one
REQUIREMENTS_PATH = os.path.join(TEMP_DIR, f'datamodel-{MAIN_DATAMODEL_RELEASE}', 'requirements.txt')
DATAMODEL_DELTAS_DIR = os.path.join(TEMP_DIR, f'datamodel-{MAIN_DATAMODEL_RELEASE}', "delta")
QGIS_PROJECT_PATH = os.path.join(TEMP_DIR, 'project', 'qgep.qgs')
INITIAL_STRUCTURE_URL_TEMPLATE = "https://github.com/QGEP/datamodel/releases/download/{version}/qgep_v{version}_structure_with_value_lists.sql"


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


def _download(url, filename):
    os.makedirs(TEMP_DIR, exist_ok=True)

    network_manager = QgsNetworkAccessManager.instance()
    QgsMessageLog.logMessage(f"Downloading {url} to {TEMP_DIR}", "QGEP")
    reply = network_manager.blockingGet(QNetworkRequest(QUrl(url)))
    download_path = os.path.join(TEMP_DIR, filename)
    download_file = QFile(download_path)
    download_file.open(QIODevice.WriteOnly)
    download_file.write(reply.content())
    download_file.close()
    return download_file.fileName()

def check_release_exists():
    return os.path.exists(REQUIREMENTS_PATH) and os.path.exists(DATAMODEL_DELTAS_DIR)

def check_python_requirements():
    return len(missing_python_requirements()) == 0

def missing_python_requirements():
    # see https://stackoverflow.com/a/45474387/13690651

    missing = []
    if not check_release_exists():
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

def install_deps(progress_dialog):

    # Download the files if needed

    progress_dialog.set_action("Downloading the release")

    if not check_release_exists():
        # Download files
        datamodel_path = _download(MAIN_DATAMODEL_RELEASE_URL, 'datamodel.zip')

        # Unzip
        QgsMessageLog.logMessage(f"Extracting files to {TEMP_DIR}", "QGEP")
        datamodel_zip = zipfile.ZipFile(datamodel_path)
        datamodel_zip.extractall(TEMP_DIR)

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

    progress_dialog.set_action("Installing python dependencies with pip")

    # Install dependencies
    QgsMessageLog.logMessage(f"Installing python dependencies from {REQUIREMENTS_PATH}", "QGEP")
    _run_cmd(f'pip install -r {REQUIREMENTS_PATH}', error_message='Could not install python dependencies')


def get_current_version(pgservice):
    if not os.path.exists(DATAMODEL_DELTAS_DIR):
        return None

    pum_info = _run_cmd(
        f'pum info -p {pgservice} -t qgep_sys.pum_info -d {DATAMODEL_DELTAS_DIR}',
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
        version = parts[1]
        if version > MAIN_DATAMODEL_RELEASE:
            # We don't want to list versions that are not yet released
            continue
        versions.add(parts[1])
    return sorted(list(versions))


def upgrade_version(pgservice, version, srid, progress_dialog):
    try:
        # If we can't get current version, it's probably that the DB is not initialized
        # (or maybe we can't connect, but we can't know easily with PUM)
        
        get_current_version(pgservice)
    except QGEPDatamodelError:

        progress_dialog.set_action("Initializing the datamodel")

        QgsMessageLog.logMessage("Upgrading failed, trying to initialize the datamodel", "QGEP")


        # TODO : this should be done by PUM directly (see https://github.com/opengisch/pum/issues/94)
        # also currently SRID doesn't work
        try:
            progress_dialog.set_action("Downloading the structure script")
            sql_path = _download(INITIAL_STRUCTURE_URL_TEMPLATE.format(version=version), f"structure_with_value_lists-{version}-{srid}.sql")
            
            # Dirty hack to customize SRID in a dump
            if srid != '2056':
                with open(sql_path, 'r') as file :
                    contents = file.read()
                contents = contents.replace('2056', srid)
                with open(sql_path, 'w') as file:
                    file.write(contents)
            
            try:
                conn = psycopg2.connect(f"service={pgservice}")
            except psycopg2.Error as e:
                # If may be that the database doesn't exist yet
                progress_dialog.set_action("Creating the database")
                dbname = get_pgservice_database_name(pgservice)
                _run_cmd(
                    f'psql -c "CREATE DATABASE {dbname};" "service={pgservice} dbname=postgres"',
                    error_message='Errors when initializing the database. Consult logs for more information.'
                )
                conn = psycopg2.connect(f"service={pgservice}")
            
            progress_dialog.set_action("Running the initialization scripts")
            cur = conn.cursor()
            cur.execute('CREATE SCHEMA IF NOT EXISTS qgep_sys;')
            cur.execute('CREATE EXTENSION IF NOT EXISTS postgis;')
            # we cannot use this, as it doesn't support COPY statements
            # this means we'll run through psql without transaction :-/
            # cur.execute(open(sql_path, "r").read())  
            conn.commit()
            cur.close()
            conn.close()
            _run_cmd(
                f'psql -f {sql_path} "service={pgservice}"',
                error_message='Errors when initializing the database. Consult logs for more information.'
            )

        except psycopg2.Error as e:
            raise QGEPDatamodelError(str(e))

    progress_dialog.set_action("Running pum upgrade")
    return _run_cmd(
        f'pum upgrade -p {pgservice} -t qgep_sys.pum_info -d {DATAMODEL_DELTAS_DIR} -u {version} -v int SRID {srid}',
        cwd=os.path.dirname(DATAMODEL_DELTAS_DIR),
        error_message='Errors when upgrading the database. Consult logs for more information.'
    )


def load_project(pgservice):

    # Unzip QGEP
    qgep_path = _download(QGEP_RELEASE_URL, 'qgep.zip')
    qgep_zip = zipfile.ZipFile(qgep_path)
    qgep_zip.extractall(TEMP_DIR)

    with open(QGIS_PROJECT_PATH, 'r') as original_project:
        contents = original_project.read()

    # replace the service name
    contents = contents.replace("service='pg_qgep'", f"service='{pgservice}'")

    output_file = tempfile.NamedTemporaryFile(suffix='.qgs', delete=False)
    output_file.write(contents.encode('utf8'))

    QgsProject.instance().read(output_file.name)


def read_pgservice():
    config = configparser.ConfigParser()
    if os.path.exists(PG_CONFIG_PATH):
        config.read(PG_CONFIG_PATH)
    return config


def get_pgservice_configs_names():
    config = read_pgservice()
    return config.sections()


def get_pgservice_database_name(service_name):
    config = read_pgservice()
    return config[service_name]['dbname']


def write_pgservice_conf(service_name, config_dict):
    config = read_pgservice()
    config[service_name] = config_dict

    class EqualsSpaceRemover:
        # see https://stackoverflow.com/a/25084055/13690651
        output_file = None

        def __init__(self, output_file):
            self.output_file = output_file

        def write(self, content):
            content = content.replace(" = ", "=", 1)
            self.output_file.write(content.encode('utf-8'))

    config.write(EqualsSpaceRemover(open(PG_CONFIG_PATH, 'wb')))