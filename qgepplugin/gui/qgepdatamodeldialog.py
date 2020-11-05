# -*- coding: utf-8 -*-
# -----------------------------------------------------------
#
# Profile
# Copyright (C) 2012  Matthias Kuhn
# -----------------------------------------------------------
#
# licensed under the terms of GNU GPL 2
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, print to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# ---------------------------------------------------------------------

import os
import configparser
import functools
import zipfile
import tempfile
import pkg_resources
import subprocess
import psycopg2

from qgis.PyQt.QtWidgets import QDialog, QMessageBox, QProgressDialog, QApplication, QPushButton
from qgis.PyQt.QtCore import QUrl, QFile, QIODevice
from qgis.PyQt.QtNetwork import QNetworkRequest

from qgis.core import QgsMessageLog, QgsNetworkAccessManager, Qgis, QgsProject

from ..utils import get_ui_class

# TODO : get latest dynamically ?
AVAILABLE_RELEASES = {
    'master': 'https://github.com/QGEP/datamodel/archive/master.zip',  # TODO : if we expose this here, we should put a big red warning and not take it default
    '1.5.2': 'https://github.com/QGEP/datamodel/archive/1.5.2.zip',
}
# Allows to pick which QGIS project matches the version (will take the biggest <= match)
DATAMODEL_QGEP_VERSIONS = {
    '1.5.0': '8.0',
    '1.4.0': '7.0',
    '0': '6.2',
}
TEMP_DIR = os.path.join(tempfile.gettempdir(), 'QGEP', 'datamodel-init')

# Path for pg_service.conf
if os.environ.get('PGSERVICEFILE'):
    PG_CONFIG_PATH = os.environ.get('PGSERVICEFILE')
elif os.environ.get('PGSYSCONFDIR'):
    PG_CONFIG_PATH = os.path.join(os.environ.get('PGSYSCONFDIR'), 'pg_service.conf')
else:
    PG_CONFIG_PATH = ' ~/.pg_service.conf'

MAIN_DATAMODEL_RELEASE = '1.5.2'
QGEP_RELEASE = '8.0'

# Derived urls/paths, may require adaptations if release structure changes
DATAMODEL_URL_TEMPLATE = 'https://github.com/QGEP/datamodel/archive/{}.zip'
REQUIREMENTS_PATH_TEMPLATE = os.path.join(TEMP_DIR, "datamodel-{}", 'requirements.txt')
DELTAS_PATH_TEMPLATE = os.path.join(TEMP_DIR, "datamodel-{}", 'delta')
INIT_SCRIPT_URL_TEMPLATE = "https://github.com/QGEP/datamodel/releases/download/{}/qgep_v{}_structure_with_value_lists.sql"
QGEP_PROJECT_URL_TEMPLATE = 'https://github.com/QGEP/QGEP/releases/download/v{}/qgep.zip'
QGEP_PROJECT_PATH_TEMPLATE = os.path.join(TEMP_DIR, "project", 'qgep.qgs')


def qgep_datamodel_error_catcher(func):
    """Display QGEPDatamodelError in error messages rather than normal exception dialog"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except QGEPDatamodelError as e:
            args[0]._show_error(str(e))
    return wrapper


class QGEPDatamodelError(Exception):
    pass


class QgepPgserviceEditorDialog(QDialog, get_ui_class('qgeppgserviceeditordialog.ui')):

    def __init__(self, cur_name, cur_config, taken_names):
        super().__init__()
        self.setupUi(self)
        self.taken_names = taken_names
        self.nameLineEdit.textChanged.connect(self.check_name)
        self.pgconfigUserCheckBox.toggled.connect(self.pgconfigUserLineEdit.setEnabled)
        self.pgconfigPasswordCheckBox.toggled.connect(self.pgconfigPasswordLineEdit.setEnabled)

        self.nameLineEdit.setText(cur_name)
        self.pgconfigHostLineEdit.setText(cur_config.get("host", ""))
        self.pgconfigPortLineEdit.setText(cur_config.get("port", ""))
        self.pgconfigDbLineEdit.setText(cur_config.get("dbname", ""))
        self.pgconfigUserLineEdit.setText(cur_config.get("user", ""))
        self.pgconfigPasswordLineEdit.setText(cur_config.get("password", ""))

        self.pgconfigUserCheckBox.setChecked(cur_config.get("user") is not None)
        self.pgconfigPasswordCheckBox.setChecked(cur_config.get("password") is not None)
        self.pgconfigUserLineEdit.setEnabled(cur_config.get("user") is not None)
        self.pgconfigPasswordLineEdit.setEnabled(cur_config.get("password") is not None)

        self.check_name(cur_name)

    def check_name(self, new_text):
        if new_text in self.taken_names:
            self.nameCheckLabel.setText('will overwrite')
            self.nameCheckLabel.setStyleSheet('color: rgb(170, 65, 0);\nfont-weight: bold;')
        else:
            self.nameCheckLabel.setText('will be created')
            self.nameCheckLabel.setStyleSheet('color: rgb(0, 170, 0);\nfont-weight: bold;')

    def conf_name(self):
        return self.nameLineEdit.text()

    def conf_dict(self):
        retval = {
            "host": self.pgconfigHostLineEdit.text(),
            "port": self.pgconfigPortLineEdit.text(),
            "dbname": self.pgconfigDbLineEdit.text(),
        }
        if self.pgconfigUserCheckBox.isChecked():
            retval.update({
                "user": self.pgconfigUserLineEdit.text(),
            })
        if self.pgconfigPasswordCheckBox.isChecked():
            retval.update({
                "password": self.pgconfigPasswordLineEdit.text(),
            })
        return retval


class QgepDatamodelInitToolDialog(QDialog, get_ui_class('qgepdatamodeldialog.ui')):

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)

        self.progress_dialog = None

        # Populate the versions
        self.releaseVersionComboBox.clear()
        self.releaseVersionComboBox.addItem('- SELECT RELEASE VERSION -')
        self.releaseVersionComboBox.model().item(0).setEnabled(False)
        for version in sorted(list(AVAILABLE_RELEASES.keys()), reverse=True):
            self.releaseVersionComboBox.addItem(version)

        # Show the pgconfig path
        self.pgservicePathLabel.setText(PG_CONFIG_PATH)

        # Connect some signals

        self.releaseVersionComboBox.activated.connect(self.switch_datamodel)

        self.installDepsButton.pressed.connect(self.install_requirements)

        self.pgserviceComboBox.activated.connect(self.select_pgconfig)
        self.pgserviceAddButton.pressed.connect(self.add_pgconfig)

        self.targetVersionComboBox.activated.connect(self.check_version)
        self.versionUpgradeButton.pressed.connect(self.upgrade_version)
        self.initializeButton.pressed.connect(self.initialize_version)

        self.loadProjectButton.pressed.connect(self.load_project)

        # Initialize the checks
        self.checks = {
            'datamodel': False,
            'requirements': False,
            'pgconfig': False,
            'current_version': False,
            'project': False,
        }

    # Properties

    @property
    def version(self):
        return self.releaseVersionComboBox.currentText()

    @property
    def target_version(self):
        return self.targetVersionComboBox.currentText()

    @property
    def conf(self):
        return self.pgserviceComboBox.currentText()

    # Feedback helpers

    def _show_progress(self, message):
        if self.progress_dialog is None:
            self.progress_dialog = QProgressDialog("Starting...", "Cancel", 0, 0)
            cancel_button = QPushButton("Cancel")
            cancel_button.setEnabled(False)
            self.progress_dialog.setCancelButton(cancel_button)
        self.progress_dialog.setLabelText(message)
        self.progress_dialog.show()
        QApplication.processEvents()

    def _done_progress(self):
        self.progress_dialog.close()
        self.progress_dialog.deleteLater()
        self.progress_dialog = None
        QApplication.processEvents()

    def _show_error(self, message):
        self._done_progress()
        err = QMessageBox()
        err.setText(message)
        err.setIcon(QMessageBox.Warning)
        err.exec_()

    # Actions helpers

    def _run_cmd(self, shell_command, cwd=None, error_message='Subprocess error, see logs for more information'):
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
            raise QGEPDatamodelError(f"{error_message}\n{result.stdout.decode()}\n{result.stderr.decode()}")
        return result.stdout.decode()

    def _download(self, url, filename):
        os.makedirs(TEMP_DIR, exist_ok=True)

        network_manager = QgsNetworkAccessManager.instance()
        reply = network_manager.blockingGet(QNetworkRequest(QUrl(url)))
        download_path = os.path.join(TEMP_DIR, filename)
        download_file = QFile(download_path)
        download_file.open(QIODevice.WriteOnly)
        download_file.write(reply.content())
        download_file.close()
        return download_file.fileName()

    def _read_pgservice(self):
        config = configparser.ConfigParser()
        if os.path.exists(PG_CONFIG_PATH):
            config.read(PG_CONFIG_PATH)
        return config

    def _write_pgservice_conf(self, service_name, config_dict):
        config = self._read_pgservice()
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

    def _get_current_version(self):
        # Dirty parsing of pum info
        deltas_dir = DELTAS_PATH_TEMPLATE.format(self.version)
        if not os.path.exists(deltas_dir):
            return None

        pum_info = self._run_cmd(
            f'pum info -p {self.conf} -t qgep_sys.pum_info -d {deltas_dir}',
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

    # Display

    def showEvent(self, event):
        self.update_pgconfig_combobox()
        self.check_datamodel()
        self.check_requirements()
        self.check_pgconfig()
        self.check_version()
        self.check_project()
        super().showEvent(event)

    def enable_buttons_if_ready(self):
        self.installDepsButton.setEnabled(self.checks['datamodel'] and not self.checks['requirements'])
        self.versionUpgradeButton.setEnabled(all(self.checks.values()))
        self.loadProjectButton.setEnabled(self.checks['project'])

    # Datamodel

    def check_datamodel(self):
        requirements_exists = os.path.exists(REQUIREMENTS_PATH_TEMPLATE.format(self.version))
        deltas_exists = os.path.exists(DELTAS_PATH_TEMPLATE.format(self.version))

        check = requirements_exists and deltas_exists

        if check:
            self.releaseCheckLabel.setText('ok')
            self.releaseCheckLabel.setStyleSheet('color: rgb(0, 170, 0);\nfont-weight: bold;')
        else:
            self.releaseCheckLabel.setText('not found')
            self.releaseCheckLabel.setStyleSheet('color: rgb(170, 0, 0);\nfont-weight: bold;')

        self.checks['datamodel'] = check
        self.enable_buttons_if_ready()

        return check

    @qgep_datamodel_error_catcher
    def switch_datamodel(self, _=None):
        # Download the datamodel if it doesn't exist

        if not self.check_datamodel():

            self._show_progress("Downloading the release")

            # Download files
            datamodel_path = self._download(AVAILABLE_RELEASES[self.version], 'datamodel.zip')

            # Unzip
            datamodel_zip = zipfile.ZipFile(datamodel_path)
            datamodel_zip.extractall(TEMP_DIR)

            # Cleanup
            # os.unlink(datamodel_path)

            # Update UI
            self.check_datamodel()

            self._done_progress()

        self.check_requirements()
        self.check_version()

    # Requirements

    def check_requirements(self):

        missing = []
        if not self.check_datamodel():
            missing.append(('unknown', 'no datamodel'))
        else:
            requirements = pkg_resources.parse_requirements(open(REQUIREMENTS_PATH_TEMPLATE.format(self.version)))
            for requirement in requirements:
                try:
                    pkg_resources.require(str(requirement))
                except pkg_resources.DistributionNotFound:
                    missing.append((requirement, 'missing'))
                except pkg_resources.VersionConflict:
                    missing.append((requirement, 'conflict'))

        check = len(missing) == 0

        if check:
            self.pythonCheckLabel.setText('ok')
            self.pythonCheckLabel.setStyleSheet('color: rgb(0, 170, 0);\nfont-weight: bold;')
        else:
            self.pythonCheckLabel.setText('\n'.join(f'{dep}: {err}' for dep, err in missing))
            self.pythonCheckLabel.setStyleSheet('color: rgb(170, 0, 0);\nfont-weight: bold;')

        self.checks['requirements'] = check
        self.enable_buttons_if_ready()

        return check

    @qgep_datamodel_error_catcher
    def install_requirements(self):

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

        self._show_progress("Installing python dependencies with pip")

        # Install dependencies
        requirements_file_path = REQUIREMENTS_PATH_TEMPLATE.format(self.version)
        QgsMessageLog.logMessage(f"Installing python dependencies from {requirements_file_path}", "QGEP")
        self._run_cmd(f'pip install --user -r {requirements_file_path}', error_message='Could not install python dependencies')

        self._done_progress()

        # Update UI
        self.check_requirements()

    # Pgservice

    def check_pgconfig(self):

        check = self.pgserviceComboBox.currentText() != ''
        if check:
            self.pgconfigCheckLabel.setText('ok')
            self.pgconfigCheckLabel.setStyleSheet('color: rgb(0, 170, 0);\nfont-weight: bold;')
        else:
            self.pgconfigCheckLabel.setText('not set')
            self.pgconfigCheckLabel.setStyleSheet('color: rgb(170, 0, 0);\nfont-weight: bold;')

        self.checks['pgconfig'] = check
        self.enable_buttons_if_ready()

        return check

    def add_pgconfig(self):
        taken_names = self._read_pgservice().sections()
        cur_config = self._read_pgservice()[self.conf]
        add_dialog = QgepPgserviceEditorDialog(self.conf, cur_config, taken_names)
        if add_dialog.exec_() == QDialog.Accepted:
            name = add_dialog.conf_name()
            conf = add_dialog.conf_dict()
            self._write_pgservice_conf(name, conf)
            self.update_pgconfig_combobox()
            self.pgserviceComboBox.setCurrentIndex(self.pgserviceComboBox.findText(name))
            self.select_pgconfig()

    def update_pgconfig_combobox(self):
        self.pgserviceComboBox.clear()
        config_names = self._read_pgservice().sections()
        for config_name in config_names:
            self.pgserviceComboBox.addItem(config_name)
        self.pgserviceComboBox.setCurrentIndex(0)

    def select_pgconfig(self, _=None):
        self.check_pgconfig()
        self.check_version()
        self.check_project()

    # Version

    def check_version(self, _=None):
        check = False

        # target version

        # (re)populate the combobox
        prev = self.targetVersionComboBox.currentText()
        self.targetVersionComboBox.clear()
        available_versions = set()
        deltas_dir = DELTAS_PATH_TEMPLATE.format(self.version)
        if os.path.exists(deltas_dir):
            for f in os.listdir(deltas_dir):
                if f.startswith('delta_'):
                    available_versions.add(f.split('_')[1])
        for available_version in sorted(list(available_versions), reverse=True):
            self.targetVersionComboBox.addItem(available_version)
        self.targetVersionComboBox.setCurrentText(prev)  # restore

        target_version = self.targetVersionComboBox.currentText()

        # current version

        self.initializeButton.setVisible(False)
        self.targetVersionComboBox.setVisible(True)
        self.versionUpgradeButton.setVisible(True)

        pgservice = self.pgserviceComboBox.currentText()
        if not pgservice:
            self.versionCheckLabel.setText('service not selected')
            self.versionCheckLabel.setStyleSheet('color: rgb(170, 0, 0);\nfont-weight: bold;')

        elif not available_versions:
            self.versionCheckLabel.setText('no delta in datamodel')
            self.versionCheckLabel.setStyleSheet('color: rgb(170, 0, 0);\nfont-weight: bold;')

        else:

            try:
                current_version = self._get_current_version()
            except QGEPDatamodelError:
                # Can happend if PUM is not initialized, unfortunately we can't really
                # determine if this is a connection error or if PUM is not initailized
                # see https://github.com/opengisch/pum/issues/96
                current_version = None

            if current_version is None:
                check = True
                self.versionCheckLabel.setText('not initialized')
                self.versionCheckLabel.setStyleSheet('color: rgb(170, 65, 0);\nfont-weight: bold;')
            elif current_version <= target_version:
                check = True
                self.versionCheckLabel.setText(current_version)
                self.versionCheckLabel.setStyleSheet('color: rgb(0, 170, 0);\nfont-weight: bold;')
            elif current_version > target_version:
                check = False
                self.versionCheckLabel.setText(f"{current_version} (cannot downgrade)")
                self.versionCheckLabel.setStyleSheet('color: rgb(170, 0, 0);\nfont-weight: bold;')
            else:
                check = False
                self.versionCheckLabel.setText(f"{current_version} (invalid version)")
                self.versionCheckLabel.setStyleSheet('color: rgb(170, 0, 0);\nfont-weight: bold;')

            self.initializeButton.setVisible(current_version is None)
            self.targetVersionComboBox.setVisible(current_version is not None)
            self.versionUpgradeButton.setVisible(current_version is not None)

        self.checks['current_version'] = check
        self.enable_buttons_if_ready()

        return check

    @qgep_datamodel_error_catcher
    def initialize_version(self):

        confirm = QMessageBox()
        confirm.setText(f"You are about to initialize the datamodel on {self.conf} to version {self.version}. ")
        confirm.setInformativeText(
            "Please confirm that you have a backup of your data as this operation can result in data loss."
        )
        confirm.setStandardButtons(QMessageBox.Apply | QMessageBox.Cancel)
        confirm.setIcon(QMessageBox.Warning)

        if confirm.exec_() == QMessageBox.Apply:

            self._show_progress("Initializing the datamodel")

            srid = self.sridLineEdit.text()

            # If we can't get current version, it's probably that the DB is not initialized
            # (or maybe we can't connect, but we can't know easily with PUM)

            self._show_progress("Initializing the datamodel")

            # TODO : this should be done by PUM directly (see https://github.com/opengisch/pum/issues/94)
            # also currently SRID doesn't work
            try:
                self._show_progress("Downloading the structure script")
                url = INIT_SCRIPT_URL_TEMPLATE.format(self.version, self.version)
                sql_path = self._download(url, f"structure_with_value_lists-{self.version}-{srid}.sql")

                # Dirty hack to customize SRID in a dump
                if srid != '2056':
                    with open(sql_path, 'r') as file:
                        contents = file.read()
                    contents = contents.replace('2056', srid)
                    with open(sql_path, 'w') as file:
                        file.write(contents)

                try:
                    conn = psycopg2.connect(f"service={self.conf}")
                except psycopg2.Error:
                    # It may be that the database doesn't exist yet
                    # in that case, we try to connect to the postgres database and to create it from there
                    self._show_progress("Creating the database")
                    dbname = self._read_pgservice()[self.conf]['dbname']
                    self._run_cmd(
                        f'psql -c "CREATE DATABASE {dbname};" "service={self.conf} dbname=postgres"',
                        error_message='Errors when initializing the database.'
                    )
                    conn = psycopg2.connect(f"service={self.conf}")

                self._show_progress("Running the initialization scripts")
                cur = conn.cursor()
                cur.execute('CREATE SCHEMA IF NOT EXISTS qgep_sys;')
                cur.execute('CREATE EXTENSION IF NOT EXISTS postgis;')
                # we cannot use this, as it doesn't support COPY statements
                # this means we'll run through psql without transaction :-/
                # cur.execute(open(sql_path, "r").read())
                conn.commit()
                cur.close()
                conn.close()
                self._run_cmd(
                    f'psql -f {sql_path} "service={self.conf}"',
                    error_message='Errors when initializing the database.'
                )

            except psycopg2.Error as e:
                raise QGEPDatamodelError(str(e))

            self.check_version()
            self.check_project()

            self._done_progress()

            success = QMessageBox()
            success.setText("Datamodel successfully initialized")
            success.setIcon(QMessageBox.Information)
            success.exec_()

    @qgep_datamodel_error_catcher
    def upgrade_version(self):

        confirm = QMessageBox()
        confirm.setText(f"You are about to update the datamodel on {self.conf} to version {self.target_version}. ")
        confirm.setInformativeText(
            "Please confirm that you have a backup of your data as this operation can result in data loss."
        )
        confirm.setStandardButtons(QMessageBox.Apply | QMessageBox.Cancel)
        confirm.setIcon(QMessageBox.Warning)

        if confirm.exec_() == QMessageBox.Apply:

            self._show_progress("Upgrading the datamodel")

            srid = self.sridLineEdit.text()

            self._show_progress("Running pum upgrade")
            deltas_dir = DELTAS_PATH_TEMPLATE.format(self.version)
            return self._run_cmd(
                f'pum upgrade -p {self.conf} -t qgep_sys.pum_info -d {deltas_dir} -u {self.target_version} -v int SRID {srid}',
                cwd=os.path.dirname(deltas_dir),
                error_message='Errors when upgrading the database.'
            )

            self.check_version()

            self._done_progress()

            success = QMessageBox()
            success.setText("Datamodel successfully upgraded")
            success.setIcon(QMessageBox.Information)
            success.exec_()

    # Project

    @qgep_datamodel_error_catcher
    def check_project(self):

        try:
            current_version = self._get_current_version()
        except QGEPDatamodelError:
            # Can happend if PUM is not initialized, unfortunately we can't really
            # determine if this is a connection error or if PUM is not initailized
            # see https://github.com/opengisch/pum/issues/96
            current_version = None

        check = current_version is not None

        if check:
            self.projectCheckLabel.setText('ok')
            self.projectCheckLabel.setStyleSheet('color: rgb(0, 170, 0);\nfont-weight: bold;')
        else:
            self.projectCheckLabel.setText('version not found')
            self.projectCheckLabel.setStyleSheet('color: rgb(170, 0, 0);\nfont-weight: bold;')

        self.checks['project'] = check
        self.enable_buttons_if_ready()

        return check

    @qgep_datamodel_error_catcher
    def load_project(self):

        current_version = self._get_current_version()

        qgis_vers = None
        for dm_vers in sorted(DATAMODEL_QGEP_VERSIONS):
            if dm_vers <= current_version:
                qgis_vers = DATAMODEL_QGEP_VERSIONS[dm_vers]

        url = QGEP_PROJECT_URL_TEMPLATE.format(qgis_vers)
        qgep_path = self._download(url, 'qgep.zip')
        qgep_zip = zipfile.ZipFile(qgep_path)
        qgep_zip.extractall(TEMP_DIR)

        with open(QGEP_PROJECT_PATH_TEMPLATE, 'r') as original_project:
            contents = original_project.read()

        # replace the service name
        contents = contents.replace("service='pg_qgep'", f"service='{self.conf}'")

        output_file = tempfile.NamedTemporaryFile(suffix='.qgs', delete=False)
        output_file.write(contents.encode('utf8'))

        QgsProject.instance().read(output_file.name)
