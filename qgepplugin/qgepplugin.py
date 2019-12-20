# -*- coding: utf-8 -*-
# -----------------------------------------------------------
#
# QGEP
#
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

from __future__ import print_function
from __future__ import absolute_import
from builtins import str
from builtins import object
import logging
import os

from qgis.PyQt.QtCore import QSettings, Qt, QLocale
from qgis.PyQt.QtWidgets import QAction, QApplication, QToolBar
from qgis.PyQt.QtGui import QIcon

from qgis.utils import qgsfunction
from qgis.core import QgsApplication

from .tools.qgepmaptools import (
    QgepProfileMapTool,
    QgepTreeMapTool,
    QgepMapToolConnectNetworkElements
)
from .tools.qgepnetwork import QgepGraphManager
from .gui.qgepprofiledockwidget import QgepProfileDockWidget
from .gui.qgepplotsvgwidget import QgepPlotSVGWidget
from .gui.qgepsettingsdialog import QgepSettingsDialog
from .gui.qgepwizard import QgepWizard
from .utils.qgeplogging import QgepQgsLogHandler
from .utils.translation import setup_i18n
from .utils.qgeplayermanager import QgepLayerNotifier
from .utils.plugin_utils import plugin_root_path
from .processing_provider.provider import QgepProcessingProvider

LOGFORMAT = '%(asctime)s:%(levelname)s:%(module)s:%(message)s'


@qgsfunction(0, "System")
def locale(values, feature, parent):
    return QSettings().value("locale/userLocale", QLocale.system().name())


class QgepPlugin(object):
    """
    A plugin for wastewater management
    http://www.github.com/qgep/QGEP
    """
    # The networkAnalyzer will manage the networklayers and pathfinding
    network_analyzer = None

    # Remember not to reopen the dock if there's already one opened
    profile_dock = None

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
        self.nodes = None
        self.edges = None

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

        fp = os.path.join(os.path.abspath(
            os.path.dirname(__file__)), "metadata.txt")

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
        self.profileAction = QAction(QIcon(os.path.join(plugin_root_path(), "icons/wastewater-profile.svg")), self.tr("Profile"),
                                     self.iface.mainWindow())
        self.profileAction.setWhatsThis(self.tr("Reach trace"))
        self.profileAction.setEnabled(False)
        self.profileAction.setCheckable(True)
        self.profileAction.triggered.connect(self.profileToolClicked)

        self.downstreamAction = QAction(QIcon(os.path.join(plugin_root_path(), "icons/wastewater-downstream.svg")),
                                        self.tr("Downstream"), self.iface.mainWindow())
        self.downstreamAction.setWhatsThis(self.tr("Downstream reaches"))
        self.downstreamAction.setEnabled(False)
        self.downstreamAction.setCheckable(True)
        self.downstreamAction.triggered.connect(self.downstreamToolClicked)

        self.upstreamAction = QAction(QIcon(os.path.join(plugin_root_path(), "icons/wastewater-upstream.svg")), self.tr("Upstream"),
                                      self.iface.mainWindow())
        self.upstreamAction.setWhatsThis(self.tr("Upstream reaches"))
        self.upstreamAction.setEnabled(False)
        self.upstreamAction.setCheckable(True)
        self.upstreamAction.triggered.connect(self.upstreamToolClicked)

        self.wizardAction = QAction(QIcon(os.path.join(plugin_root_path(), "icons/wizard.svg")),
                                    "Wizard", self.iface.mainWindow())
        self.wizardAction.setWhatsThis(
            self.tr("Create new manholes and reaches"))
        self.wizardAction.setEnabled(False)
        self.wizardAction.setCheckable(True)
        self.wizardAction.triggered.connect(self.wizard)

        self.connectNetworkElementsAction = QAction(
            QIcon(os.path.join(plugin_root_path(), "icons/link-wastewater-networkelement.svg")),
            QApplication.translate('qgepplugin', 'Connect wastewater networkelements'), self.iface.mainWindow())
        self.connectNetworkElementsAction.setEnabled(False)
        self.connectNetworkElementsAction.setCheckable(True)
        self.connectNetworkElementsAction.triggered.connect(self.connectNetworkElements)

        self.refreshNetworkTopologyAction = QAction(QIcon(os.path.join(plugin_root_path(), "icons/refresh-network.svg")),
                                                    "Refresh network topology", self.iface.mainWindow())
        self.refreshNetworkTopologyAction.setWhatsThis(
            self.tr("Refresh network topology"))
        self.refreshNetworkTopologyAction.setEnabled(False)
        self.refreshNetworkTopologyAction.setCheckable(False)
        self.refreshNetworkTopologyAction.triggered.connect(
            self.refreshNetworkTopologyActionClicked)

        self.aboutAction = QAction(self.tr('About'), self.iface.mainWindow())
        self.aboutAction.triggered.connect(self.about)

        self.settingsAction = QAction(
            self.tr('Settings'), self.iface.mainWindow())
        self.settingsAction.triggered.connect(self.showSettings)

        # Add toolbar button and menu item
        self.toolbar = QToolBar(QApplication.translate('qgepplugin', 'QGEP'))
        self.toolbar.addAction(self.profileAction)
        self.toolbar.addAction(self.upstreamAction)
        self.toolbar.addAction(self.downstreamAction)
        self.toolbar.addAction(self.wizardAction)
        self.toolbar.addAction(self.refreshNetworkTopologyAction)
        self.toolbar.addAction(self.connectNetworkElementsAction)

        self.iface.addPluginToMenu("&QGEP", self.profileAction)
        self.iface.addPluginToMenu("&QGEP", self.settingsAction)
        self.iface.addPluginToMenu("&QGEP", self.aboutAction)

        self.iface.addToolBar(self.toolbar)

        # Local array of buttons to enable / disable based on context
        self.toolbarButtons.append(self.profileAction)
        self.toolbarButtons.append(self.upstreamAction)
        self.toolbarButtons.append(self.downstreamAction)
        self.toolbarButtons.append(self.wizardAction)
        self.toolbarButtons.append(self.refreshNetworkTopologyAction)

        self.network_layer_notifier.layersAvailable.connect(self.onLayersAvailable)
        self.network_layer_notifier.layersUnavailable.connect(self.onLayersUnavailable)

        # Init the object maintaining the network
        self.network_analyzer = QgepGraphManager()
        self.network_analyzer.message_emitted.connect(self.iface.messageBar().pushMessage)
        # Create the map tool for profile selection
        self.profile_tool = QgepProfileMapTool(self.iface, self.profileAction, self.network_analyzer)
        self.profile_tool.profileChanged.connect(self.onProfileChanged)

        self.upstream_tree_tool = QgepTreeMapTool(
            self.iface, self.upstreamAction, self.network_analyzer)
        self.upstream_tree_tool.setDirection("upstream")
        self.upstream_tree_tool.treeChanged.connect(self.onTreeChanged)
        self.downstream_tree_tool = QgepTreeMapTool(
            self.iface, self.downstreamAction, self.network_analyzer)
        self.downstream_tree_tool.setDirection("downstream")
        self.downstream_tree_tool.treeChanged.connect(self.onTreeChanged)

        self.maptool_connect_networkelements = QgepMapToolConnectNetworkElements(
            self.iface, self.connectNetworkElementsAction)

        self.wastewater_networkelement_layer_notifier.layersAvailableChanged.connect(
            self.connectNetworkElementsAction.setEnabled)

        self.processing_provider = QgepProcessingProvider()
        QgsApplication.processingRegistry().addProvider(self.processing_provider)

    def unload(self):
        """
        Called when unloading
        """
        self.toolbar.removeAction(self.profileAction)
        self.toolbar.removeAction(self.upstreamAction)
        self.toolbar.removeAction(self.downstreamAction)
        self.toolbar.removeAction(self.wizardAction)
        self.toolbar.removeAction(self.refreshNetworkTopologyAction)
        self.toolbar.removeAction(self.connectNetworkElementsAction)

        self.toolbar.deleteLater()

        self.iface.removePluginMenu("&QGEP", self.profileAction)
        self.iface.removePluginMenu("&QGEP", self.aboutAction)

        QgsApplication.processingRegistry().removeProvider(self.processing_provider)

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
        self.openDock()
        self.upstream_tree_tool.setActive()

    def downstreamToolClicked(self):
        """
        Is executed when the user clicks the downstream search tool
        """
        self.openDock()
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

    def connectNetworkElements(self, checked):
        self.iface.mapCanvas().setMapTool(self.maptool_connect_networkelements)

    def openDock(self):
        """
        Opens the dock
        """
        if self.profile_dock is None:
            self.logger.debug('Open dock')
            self.profile_dock = QgepProfileDockWidget(self.iface.mainWindow(), self.iface.mapCanvas(),
                                                      self.iface.addDockWidget)
            self.profile_dock.closed.connect(self.onDockClosed)
            self.profile_dock.showIt()

            self.plotWidget = QgepPlotSVGWidget(self.profile_dock, self.network_analyzer)
            self.plotWidget.specialStructureMouseOver.connect(self.highlightProfileElement)
            self.plotWidget.specialStructureMouseOut.connect(self.unhighlightProfileElement)
            self.plotWidget.reachMouseOver.connect(self.highlightProfileElement)
            self.plotWidget.reachMouseOut.connect(self.unhighlightProfileElement)
            self.profile_dock.addPlotWidget(self.plotWidget)
            self.profile_dock.setTree(self.nodes, self.edges)

    def onDockClosed(self):  # used when Dock dialog is closed
        """
        Gets called when the dock is closed
        All the cleanup of the dock has to be done here
        """
        self.profile_dock = None

    def onProfileChanged(self, profile):
        """
        The profile changed: update the plot
        @param profile: The profile to plot
        """
        self.profile = profile.copy()

        if self.plotWidget:
            self.plotWidget.setProfile(profile)

    def onTreeChanged(self, nodes, edges):
        if self.profile_dock:
            self.profile_dock.setTree(nodes, edges)
        self.nodes = nodes
        self.edges = edges

    def highlightProfileElement(self, obj_id):
        if self.profile is not None:
            self.profile.highlight(str(obj_id))

    def unhighlightProfileElement(self):
        if self.profile is not None:
            self.profile.highlight(None)

    def about(self):
        from .gui.dlgabout import DlgAbout

        DlgAbout(self.iface.mainWindow()).exec_()

    def showSettings(self):
        settings_dlg = QgepSettingsDialog(self.iface.mainWindow())
        settings_dlg.exec_()
