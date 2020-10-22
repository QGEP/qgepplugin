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

from builtins import str
from qgis.PyQt.QtWidgets import QDialog, QMessageBox
from qgis.core import QgsSettings

from ..utils import get_ui_class
from .. import datamodel_initializer

DIALOG_UI = get_ui_class('qgepdatamodeldialog.ui')

QGEP_SERVICE_NAME = 'pg_qgep'

if os.environ.get('PGSERVICEFILE'):
    PG_CONFIG_PATH = os.environ.get('PGSERVICEFILE')
elif os.environ.get('PGSYSCONFDIR'):
    PG_CONFIG_PATH = os.path.join(os.environ.get('PGSYSCONFDIR'), 'pg_service.conf')
else:
    PG_CONFIG_PATH = ' ~/.pg_service.conf'


def qgep_datamodel_error_catcher(func):
    """Display QGEPDatamodelError in error messages rather than normal exception dialog"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except datamodel_initializer.QGEPDatamodelError as e:
            err = QMessageBox()
            err.setText(str(e))
            err.setIcon(QMessageBox.Warning)
            err.exec_()
    return wrapper


class QgepDatamodelInitToolDialog(QDialog, DIALOG_UI):

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)

        self.installDepsButton.pressed.connect(self.install_deps)

        self.pgconfigWriteButton.pressed.connect(self.write_to_pgservice)
        self.pgconfigLoadButton.pressed.connect(self.read_from_pgservice)
        self.connectionComboBox.currentIndexChanged.connect(self.populate_from_connection_combobox)

        self.pgconfigHostLineEdit.editingFinished.connect(self.update_pgconfig_checks)
        self.pgconfigPortLineEdit.editingFinished.connect(self.update_pgconfig_checks)
        self.pgconfigDbLineEdit.editingFinished.connect(self.update_pgconfig_checks)
        self.pgconfigUserLineEdit.editingFinished.connect(self.update_pgconfig_checks)
        self.pgconfigPasswordLineEdit.editingFinished.connect(self.update_pgconfig_checks)

        self.versionCheckButton.pressed.connect(self.update_versions_checks)
        self.versionUpgradeButton.pressed.connect(self.upgrade_version)
        self.loadProjectButton.pressed.connect(datamodel_initializer.load_project)

        self.checks = {
            'release': False,
            'dependencies': False,
            'pgconfig': False,
            'current_version': False,
        }

    @qgep_datamodel_error_catcher
    def showEvent(self, event):
        self.refresh_connection_combobox()
        self.update_requirements_checks()
        self.read_from_pgservice()
        self.update_versions_checks()
        super().showEvent(event)

    def enable_buttons_if_ready(self):
        self.versionCheckButton.setEnabled(self.checks['dependencies'])
        self.versionUpgradeButton.setEnabled(all(self.checks.values()))
        self.loadProjectButton.setEnabled(self.checks['release'])

    @qgep_datamodel_error_catcher
    def install_deps(self):
        datamodel_initializer.install_deps()
        self.update_requirements_checks()

    @qgep_datamodel_error_catcher
    def update_requirements_checks(self):

        if datamodel_initializer.check_release_exists():
            self.checks['release'] = True
            self.releaseCheckLabel.setText('ok')
            self.releaseCheckLabel.setStyleSheet('color: rgb(0, 170, 0);\nfont-weight: bold;')
        else:
            self.checks['release'] = False
            self.releaseCheckLabel.setText('not found')
            self.releaseCheckLabel.setStyleSheet('color: rgb(170, 0, 0);\nfont-weight: bold;')

        if datamodel_initializer.check_python_requirements():
            self.checks['dependencies'] = True
            self.pythonCheckLabel.setText('ok')
            self.pythonCheckLabel.setStyleSheet('color: rgb(0, 170, 0);\nfont-weight: bold;')
        else:
            self.checks['dependencies'] = False
            errors = datamodel_initializer.missing_python_requirements()
            self.pythonCheckLabel.setText('\n'.join(f'{dep}: {err}' for dep, err in errors))
            self.pythonCheckLabel.setStyleSheet('color: rgb(170, 0, 0);\nfont-weight: bold;')

        self.enable_buttons_if_ready()

    @qgep_datamodel_error_catcher
    def update_pgconfig_checks(self):

        self.checks['pgconfig'] = False

        self.pgconfigCheckLabel.setText('pg_service.conf file missing')
        self.pgconfigCheckLabel.setStyleSheet('color: rgb(170, 0, 0);\nfont-weight: bold;')

        if os.path.exists(PG_CONFIG_PATH):
            config = configparser.ConfigParser()
            config.read(PG_CONFIG_PATH)

            self.pgconfigCheckLabel.setText('pg_qgep configuration missing')
            self.pgconfigCheckLabel.setStyleSheet('color: rgb(170, 0, 0);\nfont-weight: bold;')

            if QGEP_SERVICE_NAME in config:
                mismatches = []
                if self.pgconfigHostLineEdit.text() != config[QGEP_SERVICE_NAME].get('host'):
                    mismatches.append('host')
                if self.pgconfigPortLineEdit.text() != config[QGEP_SERVICE_NAME].get('port'):
                    mismatches.append('port')
                if self.pgconfigDbLineEdit.text() != config[QGEP_SERVICE_NAME].get('dbname'):
                    mismatches.append('dbname')
                if self.pgconfigUserLineEdit.text() != config[QGEP_SERVICE_NAME].get('user'):
                    mismatches.append('user')
                if self.pgconfigPasswordLineEdit.text() != config[QGEP_SERVICE_NAME].get('password'):
                    mismatches.append('password')

                if mismatches:
                    self.pgconfigCheckLabel.setText('mismatches : ' + ','.join(mismatches))
                    self.pgconfigCheckLabel.setStyleSheet('color: rgb(170, 0, 0);\nfont-weight: bold;')
                else:
                    self.checks['pgconfig'] = True
                    self.pgconfigCheckLabel.setText('ok')
                    self.pgconfigCheckLabel.setStyleSheet('color: rgb(0, 170, 0);\nfont-weight: bold;')

        self.enable_buttons_if_ready()

    @qgep_datamodel_error_catcher
    def update_versions_checks(self):
        self.checks['current_version'] = False

        current_version = datamodel_initializer.get_current_version()
        available_versions = datamodel_initializer.get_available_versions()

        if current_version in available_versions:
            self.checks['current_version'] = True
            self.versionCheckLabel.setText(current_version)
            self.versionCheckLabel.setStyleSheet('color: rgb(0, 170, 0);\nfont-weight: bold;')
        elif current_version is None:
            self.versionCheckLabel.setText("could not determine version")
            self.versionCheckLabel.setStyleSheet('color: rgb(170, 0, 0);\nfont-weight: bold;')
        else:
            self.versionCheckLabel.setText(f"invalid version : {current_version}")
            self.versionCheckLabel.setStyleSheet('color: rgb(170, 0, 0);\nfont-weight: bold;')

        self.targetVersionComboBox.clear()
        for version in reversed(available_versions):
            self.targetVersionComboBox.addItem(version)
            if version < current_version:
                i = self.targetVersionComboBox.model().rowCount() - 1
                self.targetVersionComboBox.model().item(i).setEnabled(False)

        self.enable_buttons_if_ready()

    @qgep_datamodel_error_catcher
    def refresh_connection_combobox(self):
        self.connectionComboBox.clear()

        self.connectionComboBox.addItem('-- Populate from browser --')
        self.connectionComboBox.model().item(0).setEnabled(False)

        settings = QgsSettings()
        settings.beginGroup('/PostgreSQL/connections')
        for name in settings.childGroups():
            self.connectionComboBox.addItem(name)
        settings.endGroup()

    @qgep_datamodel_error_catcher
    def read_from_pgservice(self):

        self.pgconfigHostLineEdit.setText('')
        self.pgconfigPortLineEdit.setText('')
        self.pgconfigDbLineEdit.setText('')
        self.pgconfigUserLineEdit.setText('')
        self.pgconfigPasswordLineEdit.setText('')

        if os.path.exists(PG_CONFIG_PATH):
            config = configparser.ConfigParser()
            config.read(PG_CONFIG_PATH)
            if QGEP_SERVICE_NAME in config:
                self.pgconfigHostLineEdit.setText(config[QGEP_SERVICE_NAME].get('host'))
                self.pgconfigPortLineEdit.setText(config[QGEP_SERVICE_NAME].get('port'))
                self.pgconfigDbLineEdit.setText(config[QGEP_SERVICE_NAME].get('dbname'))
                self.pgconfigUserLineEdit.setText(config[QGEP_SERVICE_NAME].get('user'))
                self.pgconfigPasswordLineEdit.setText(config[QGEP_SERVICE_NAME].get('password'))

        self.update_pgconfig_checks()

    @qgep_datamodel_error_catcher
    def write_to_pgservice(self):
        """
        Saves the selected's postgres to pg_service.conf
        """

        config = configparser.ConfigParser()
        if os.path.exists(PG_CONFIG_PATH):
            config.read(PG_CONFIG_PATH)

        config[QGEP_SERVICE_NAME] = {
            "host": self.pgconfigHostLineEdit.text(),
            "port": self.pgconfigPortLineEdit.text(),
            "dbname": self.pgconfigDbLineEdit.text(),
            "user": self.pgconfigUserLineEdit.text(),
            "password": self.pgconfigPasswordLineEdit.text(),
        }

        class EqualsSpaceRemover:
            # see https://stackoverflow.com/a/25084055/13690651
            output_file = None

            def __init__(self, output_file):
                self.output_file = output_file

            def write(self, what):
                self.output_file.write(what.replace(" = ", "=", 1))

        config.write(EqualsSpaceRemover(open(PG_CONFIG_PATH, 'w')))

        self.update_pgconfig_checks()

    @qgep_datamodel_error_catcher
    def populate_from_connection_combobox(self, index):
        if index == 0:
            return
        name = self.connectionComboBox.currentText()
        settings = QgsSettings()
        settings.beginGroup(f"/PostgreSQL/connections/{name}")
        self.pgconfigHostLineEdit.setText(settings.value("host", "", type=str))
        self.pgconfigPortLineEdit.setText(settings.value("port", "", type=str))
        self.pgconfigDbLineEdit.setText(settings.value("database", "", type=str))
        self.pgconfigUserLineEdit.setText(settings.value("username", "", type=str))
        self.pgconfigPasswordLineEdit.setText(settings.value("password", "", type=str))
        settings.endGroup()
        self.update_pgconfig_checks()

    @qgep_datamodel_error_catcher
    def upgrade_version(self):
        version = self.targetVersionComboBox.currentText()

        confirm = QMessageBox()
        confirm.setText(f"You are about to update your datamodel to version {version}. ")
        confirm.setInformativeText(
            "Please confirm that you have a backup of your data as this operation can result in data loss."
        )
        confirm.setStandardButtons(QMessageBox.Apply | QMessageBox.Cancel)
        confirm.setIcon(QMessageBox.Warning)

        if confirm.exec_() == QMessageBox.Apply:
            datamodel_initializer.upgrade_version(version, self.sridLineEdit.text())
            self.update_versions_checks()
