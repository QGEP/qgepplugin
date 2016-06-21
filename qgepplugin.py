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
# with this progsram; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# ---------------------------------------------------------------------

import logging
import os

from PyQt4.QtCore import (
    pyqtSlot,
    QSettings,
    Qt
)
from PyQt4.QtGui import (
    QAction,
    QIcon,
    QApplication
)

from tools.qgepmaptools import (
    QgepProfileMapTool,
    QgepTreeMapTool,
    QgepMapToolConnectNetworkElements
)
from tools.qgepnetwork import QgepGraphManager
from ui.qgepprofiledockwidget import QgepProfileDockWidget
from ui.qgepplotsvgwidget import QgepPlotSVGWidget
from ui.qgepsettingsdialog import QgepSettingsDialog
from ui.qgepwizard import QgepWizard
from utils.qgeplogging import QgepQgsLogHandler
from utils.translation import setup_i18n
from utils.qgeplayermanager import QgepLayerNotifier

import resources  # NOQA

LOGFORMAT = '%(asctime)s:%(levelname)s:%(module)s:%(message)s'


class QgepPlugin:
    """
    A plugin for wastewater management
    http://www.github.com/qgep/QGEP
    """
    # The networkAnalyzer will manage the networklayers and pathfinding
    network_analyzer = None

    # Remember not to reopen the dock if there's already one opened
    profileDock = None

    # Wizard
    wizarddock = None

    # The layer ids the plugin will need
    edgeLayer = None
    nodeLayer = None
    specialStructureLayer = None
    networkElementLayer = None

    profile = None

    def __init__(self, iface):
        self.iface = iface
        self.canvas = iface.mapCanvas()

        self.initLogger()
        setup_i18n()

    def tr(self, source_text):
        """
        This does not inherit from QObject but for the translation to work (in particular to have translatable strings
        picked up) we need a tr method.
        :rtype : unicode
        :param source_text: The text to translate
        :return: The translated text
        """
        return QApplication.translate('QgepPlugin', source_text)

    def initLogger(self):
        """
        Initializes the logger
        """
        self.logger = logging.getLogger(__package__)

        settings = QSettings()

        loglevel = settings.value("/QGEP/LogLevel", 'Warning')
        logfile = settings.value("/QGEP/LogFile", None)

        if hasattr(self.logger, 'qgepFileHandler'):
            self.logger.removeHandler(self.logger.qgepFileHandler)
            del self.logger.qgepFileHandler

        self.logger.addHandler(QgepQgsLogHandler())

        if logfile:
            log_handler = logging.FileHandler(logfile)
            fmt = logging.Formatter(LOGFORMAT)
            log_handler.setFormatter(fmt)
            self.logger.addHandler(log_handler)
            self.logger.fileHandler = log_handler

        if 'Debug' == loglevel:
            self.logger.setLevel(logging.DEBUG)
        elif 'Info' == loglevel:
            self.logger.setLevel(logging.INFO)
        elif 'Warning' == loglevel:
            self.logger.setLevel(logging.WARNING)
        elif 'Error' == loglevel:
            self.logger.setLevel(logging.ERROR)

        fp = os.path.join(os.path.abspath(os.path.dirname(__file__)), "metadata.txt")

        ini_text = QSettings(fp, QSettings.IniFormat)
        verno = ini_text.value("version")

        self.logger.info('QGEP plugin version ' + verno + ' started')

    def initGui(self):
        """
        Called to setup the plugin GUI
        """
        self.network_layer_notifier = QgepLayerNotifier(self.iface.mainWindow(),
                                                        ['vw_network_node', 'vw_network_segment'])
        self.wastewater_networkelement_layer_notifier = QgepLayerNotifier(self.iface.mainWindow(),
                                                                          ['vw_wastewater_node', 'vw_qgep_reach'])
        self.toolbarButtons = []

        # Create toolbar button
        self.profileAction = QAction(QIcon(":/plugins/qgepplugin/icons/wastewater-profile.svg"), self.tr("Profile"),
                                     self.iface.mainWindow())
        self.profileAction.setWhatsThis(self.tr("Reach trace"))
        self.profileAction.setEnabled(False)
        self.profileAction.setCheckable(True)
        self.profileAction.triggered.connect(self.profileToolClicked)

        self.downstreamAction = QAction(QIcon(":/plugins/qgepplugin/icons/wastewater-downstream.svg"),
                                        self.tr("Downstream"), self.iface.mainWindow())
        self.downstreamAction.setWhatsThis(self.tr("Downstream reaches"))
        self.downstreamAction.setEnabled(False)
        self.downstreamAction.setCheckable(True)
        self.downstreamAction.triggered.connect(self.downstreamToolClicked)

        self.upstreamAction = QAction(QIcon(":/plugins/qgepplugin/icons/wastewater-upstream.svg"), self.tr("Upstream"),
                                      self.iface.mainWindow())
        self.upstreamAction.setWhatsThis(self.tr("Upstream reaches"))
        self.upstreamAction.setEnabled(False)
        self.upstreamAction.setCheckable(True)
        self.upstreamAction.triggered.connect(self.upstreamToolClicked)

        self.wizardAction = QAction(QIcon(":/plugins/qgepplugin/icons/wizard.svg"), "Wizard", self.iface.mainWindow())
        self.wizardAction.setWhatsThis(self.tr("Create new manholes and reaches"))
        self.wizardAction.setEnabled(False)
        self.wizardAction.setCheckable(True)
        self.wizardAction.triggered.connect(self.wizard)

        self.connectNetworkElementsAction = QAction(
            QIcon(":/plugins/qgepplugin/icons/link-wastewater-networkelement.svg"),
            QApplication.translate('qgepplugin', 'Connect wastewater networkelements'), self.iface.mainWindow())
        self.connectNetworkElementsAction.setEnabled(False)
        self.connectNetworkElementsAction.setCheckable(True)
        self.connectNetworkElementsAction.triggered.connect(self.connectNetworkElements)

        self.refreshNetworkTopologyAction = QAction(QIcon(":/plugins/qgepplugin/icons/refresh-network.svg"),
                                                    "Refresh network topology", self.iface.mainWindow())
        self.refreshNetworkTopologyAction.setWhatsThis(self.tr("Refresh network topology"))
        self.refreshNetworkTopologyAction.setEnabled(False)
        self.refreshNetworkTopologyAction.setCheckable(False)
        self.refreshNetworkTopologyAction.triggered.connect(self.refreshNetworkTopologyActionClicked)

        self.aboutAction = QAction(self.tr('About'), self.iface.mainWindow())
        self.aboutAction.triggered.connect(self.about)

        self.settingsAction = QAction(self.tr('Settings'), self.iface.mainWindow())
        self.settingsAction.triggered.connect(self.showSettings)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.profileAction)
        self.iface.addToolBarIcon(self.upstreamAction)
        self.iface.addToolBarIcon(self.downstreamAction)
        self.iface.addToolBarIcon(self.wizardAction)
        self.iface.addToolBarIcon(self.refreshNetworkTopologyAction)
        self.iface.addToolBarIcon(self.connectNetworkElementsAction)

        self.iface.addPluginToMenu("&QGEP", self.profileAction)
        self.iface.addPluginToMenu("&QGEP", self.settingsAction)
        self.iface.addPluginToMenu("&QGEP", self.aboutAction)

        # Local array of buttons to enable / disable based on context
        self.toolbarButtons.append(self.profileAction)
        self.toolbarButtons.append(self.upstreamAction)
        self.toolbarButtons.append(self.downstreamAction)
        self.toolbarButtons.append(self.wizardAction)
        self.toolbarButtons.append(self.refreshNetworkTopologyAction)

        self.network_layer_notifier.layersAvailable.connect(self.onLayersAvailable)
        self.network_layer_notifier.layersUnavailable.connect(self.onLayersUnavailable)

        # Init the object maintaining the network
        self.network_analyzer = QgepGraphManager(self.iface)
        # Create the map tool for profile selection
        self.profile_tool = QgepProfileMapTool(self.iface, self.profileAction, self.network_analyzer)
        self.profile_tool.profileChanged.connect(self.onProfileChanged)

        self.upstream_tree_tool = QgepTreeMapTool(self.iface, self.upstreamAction, self.network_analyzer)
        self.upstream_tree_tool.setDirection("upstream")
        self.downstream_tree_tool = QgepTreeMapTool(self.iface, self.downstreamAction, self.network_analyzer)
        self.downstream_tree_tool.setDirection("downstream")

        self.maptool_connect_networkelements = QgepMapToolConnectNetworkElements(
            self.iface, self.connectNetworkElementsAction)

        self.wastewater_networkelement_layer_notifier.layersAvailableChanged.connect(
            self.connectNetworkElementsAction.setEnabled)

    def unload(self):
        """
        Called when unloading
        """
        self.iface.removeToolBarIcon(self.profileAction)
        self.iface.removeToolBarIcon(self.upstreamAction)
        self.iface.removeToolBarIcon(self.downstreamAction)
        self.iface.removeToolBarIcon(self.wizardAction)
        self.iface.removeToolBarIcon(self.refreshNetworkTopologyAction)
        self.iface.removeToolBarIcon(self.connectNetworkElementsAction)

        self.iface.removePluginMenu("&QGEP", self.profileAction)
        self.iface.removePluginMenu("&QGEP", self.aboutAction)

    def onLayersAvailable(self, layers):
        for b in self.toolbarButtons:
            b.setEnabled(True)

        self.network_analyzer.setReachLayer(layers['vw_network_segment'])
        self.network_analyzer.setNodeLayer(layers['vw_network_node'])

    def onLayersUnavailable(self):
        for b in self.toolbarButtons:
            b.setEnabled(False)

    def profileToolClicked(self):
        """
        Is executed when the profile button is clicked
        """
        self.openDock()
        # Set the profile map tool
        self.profile_tool.setActive()

    def upstreamToolClicked(self):
        """
        Is executed when the user clicks the upstream search tool
        """
        self.upstream_tree_tool.setActive()

    def downstreamToolClicked(self):
        """
        Is executed when the user clicks the downstream search tool
        """
        self.downstream_tree_tool.setActive()

    def refreshNetworkTopologyActionClicked(self):
        """
        Is executed when the user clicks the refreshNetworkTopologyAction tool
        """
        self.network_analyzer.refresh()

    def wizard(self):
        """
        """
        if not self.wizarddock:
            self.wizarddock = QgepWizard(self.iface.mainWindow(), self.iface)
        self.logger.debug('Opening Wizard')
        self.iface.addDockWidget(Qt.LeftDockWidgetArea, self.wizarddock)
        self.wizarddock.show()

    @pyqtSlot()
    def connectNetworkElements(self):
        print 'Copnnet them'
        self.iface.mapCanvas().setMapTool(self.maptool_connect_networkelements)

    def openDock(self):
        """
        Opens the dock
        """
        if self.profileDock is None:
            self.logger.debug('Open dock')
            self.profileDock = QgepProfileDockWidget(self.iface.mainWindow(), self.iface.mapCanvas(),
                                                     self.iface.addDockWidget)
            self.profileDock.closed.connect(self.onDockClosed)
            self.profileDock.showIt()

            self.plotWidget = QgepPlotSVGWidget(self.profileDock, self.network_analyzer)
            self.plotWidget.specialStructureMouseOver.connect(self.highlightProfileElement)
            self.plotWidget.specialStructureMouseOut.connect(self.unhighlightProfileElement)
            self.plotWidget.reachMouseOver.connect(self.highlightProfileElement)
            self.plotWidget.reachMouseOut.connect(self.unhighlightProfileElement)
            self.profileDock.addPlotWidget(self.plotWidget)

    @pyqtSlot()
    def onDockClosed(self):  # used when Dock dialog is closed
        """
        Gets called when the dock is closed
        All the cleanup of the dock has to be done here
        """
        self.profileDock = None

    def onProfileChanged(self, profile):
        """
        The profile changed: update the plot
        @param profile: The profile to plot
        """
        self.profile = profile.copy()

        if self.plotWidget:
            self.plotWidget.setProfile(profile)

    @pyqtSlot(unicode)
    def highlightProfileElement(self, obj_id):
        if self.profile is not None:
            self.profile.highlight(unicode(obj_id))

    @pyqtSlot()
    def unhighlightProfileElement(self):
        if self.profile is not None:
            self.profile.highlight(None)

    def about(self):
        from ui.dlgabout import DlgAbout

        DlgAbout(self.iface.mainWindow()).exec_()

    def showSettings(self):
        settings_dlg = QgepSettingsDialog(self.iface.mainWindow())
        settings_dlg.exec_()
