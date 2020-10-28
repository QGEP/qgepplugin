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
from qgis.core import QgsSettings, QgsMessageLog

from ..utils import get_ui_class
from .. import datamodel_initializer


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



class QgepPgserviceEditorDialog(QDialog, get_ui_class('qgeppgserviceeditordialog.ui')):

    def __init__(self, existing_config_names, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.existing_config_names = existing_config_names
        self.nameLineEdit.textChanged.connect(self.check_name)

    def check_name(self, new_text):
        if new_text in self.existing_config_names:
            self.nameCheckLabel.setText('will overwrite')
            self.nameCheckLabel.setStyleSheet('color: rgb(170, 65, 0);\nfont-weight: bold;')
        else:
            self.nameCheckLabel.setText('will be created')
            self.nameCheckLabel.setStyleSheet('color: rgb(0, 170, 0);\nfont-weight: bold;')

    def conf_name(self):
        return self.nameLineEdit.text()

    def conf_dict(self):
        return {
            "host": self.pgconfigHostLineEdit.text(),
            "port": self.pgconfigPortLineEdit.text(),
            "dbname": self.pgconfigDbLineEdit.text(),
            "user": self.pgconfigUserLineEdit.text(),
            "password": self.pgconfigPasswordLineEdit.text(),
        }



class QgepDatamodelInitToolDialog(QDialog, get_ui_class('qgepdatamodeldialog.ui')):

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)

        self.installDepsButton.pressed.connect(self.install_deps)

        self.pgserviceComboBox.activated.connect(self.update_pgconfig_checks)
        self.pgserviceAddButton.pressed.connect(self.add_pgconfig)

        self.versionUpgradeButton.pressed.connect(self.upgrade_version)
        self.loadProjectButton.pressed.connect(self.load_project)

        self.checks = {
            'release': False,
            'dependencies': False,
            'pgconfig': False,
            'current_version': False,
        }

    @qgep_datamodel_error_catcher
    def showEvent(self, event):
        self.refresh_pgservice_combobox()
        self.update_requirements_checks()
        self.update_pgconfig_checks()
        self.update_versions_checks()
        self.pgservicePathLabel.setText(datamodel_initializer.PG_CONFIG_PATH)
        super().showEvent(event)

    def enable_buttons_if_ready(self):
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
    def refresh_pgservice_combobox(self):
        self.pgserviceComboBox.clear()
        config_names = datamodel_initializer.get_pgservice_configs_names()
        for config_name in config_names:
            self.pgserviceComboBox.addItem(config_name)
        self.pgserviceComboBox.setCurrentIndex(-1)

    @qgep_datamodel_error_catcher
    def add_pgconfig(self):
        existing_config_names = datamodel_initializer.get_pgservice_configs_names()
        add_dialog = QgepPgserviceEditorDialog(existing_config_names)
        if add_dialog.exec_() == QDialog.Accepted:
            name = add_dialog.conf_name()
            conf = add_dialog.conf_dict()
            datamodel_initializer.write_pgservice_conf(name, conf)
            self.refresh_pgservice_combobox()
            self.pgserviceComboBox.setCurrentIndex(self.pgserviceComboBox.findText(name))
            self.update_pgconfig_checks()

    @qgep_datamodel_error_catcher
    def update_pgconfig_checks(self, _=None):

        if self.pgserviceComboBox.currentText():
            self.checks['pgconfig'] = True
            self.pgconfigCheckLabel.setText('ok')
            self.pgconfigCheckLabel.setStyleSheet('color: rgb(0, 170, 0);\nfont-weight: bold;')
        else:
            self.checks['pgconfig'] = False
            self.pgconfigCheckLabel.setText('not set')
            self.pgconfigCheckLabel.setStyleSheet('color: rgb(170, 0, 0);\nfont-weight: bold;')

        self.update_versions_checks()

    @qgep_datamodel_error_catcher
    def update_versions_checks(self):
        self.checks['current_version'] = False

        available_versions = datamodel_initializer.get_available_versions()
        self.targetVersionComboBox.clear()
        for version in reversed(available_versions):
            self.targetVersionComboBox.addItem(version)

        pgservice = self.pgserviceComboBox.currentText()
        if not pgservice:
            self.versionCheckLabel.setText('service not selected')
            self.versionCheckLabel.setStyleSheet('color: rgb(170, 0, 0);\nfont-weight: bold;')
            return

        try:
            current_version = datamodel_initializer.get_current_version(pgservice)
        except datamodel_initializer.QGEPDatamodelError:
            # Can happend if PUM is not initialized, unfortunately we can't really
            # determine if this is a connection error or if PUM is not initailized
            # see https://github.com/opengisch/pum/issues/96
            current_version = None

        if current_version is None or current_version == '0.0.0' or current_version in available_versions:
            self.checks['current_version'] = True
            self.versionCheckLabel.setText(current_version or 'not initialized')
            self.versionCheckLabel.setStyleSheet('color: rgb(0, 170, 0);\nfont-weight: bold;')
        elif current_version is None:
            self.versionCheckLabel.setText("could not determine version")
            self.versionCheckLabel.setStyleSheet('color: rgb(170, 0, 0);\nfont-weight: bold;')
        else:
            self.versionCheckLabel.setText(f"invalid version : {current_version}")
            self.versionCheckLabel.setStyleSheet('color: rgb(170, 0, 0);\nfont-weight: bold;')

        # disable unapplicable versions
        for i in range(self.targetVersionComboBox.model().rowCount()):
            item_version = self.targetVersionComboBox.model().item(i).text()
            enabled = current_version is None or item_version >= current_version
            self.targetVersionComboBox.model().item(i).setEnabled(enabled)

        self.enable_buttons_if_ready()

    @qgep_datamodel_error_catcher
    def upgrade_version(self):
        version = self.targetVersionComboBox.currentText()
        pgservice = self.pgserviceComboBox.currentText()

        confirm = QMessageBox()
        confirm.setText(f"You are about to update the datamodel on {pgservice} to version {version}. ")
        confirm.setInformativeText(
            "Please confirm that you have a backup of your data as this operation can result in data loss."
        )
        confirm.setStandardButtons(QMessageBox.Apply | QMessageBox.Cancel)
        confirm.setIcon(QMessageBox.Warning)

        if confirm.exec_() == QMessageBox.Apply:
            datamodel_initializer.upgrade_version(pgservice, version, self.sridLineEdit.text())
            self.update_versions_checks()

    @qgep_datamodel_error_catcher
    def load_project(self):
        pgservice = self.pgserviceComboBox.currentText()
        datamodel_initializer.load_project(pgservice)
