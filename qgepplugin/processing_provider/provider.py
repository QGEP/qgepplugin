# -*- coding: utf-8 -*-

"""
/***************************************************************************
 QGEP processing provider
                              -------------------
        begin                : 18.11.2017
        copyright            : (C) 2017 by OPENGIS.ch
        email                : matthias@opengis.ch
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from qgis.core import QgsProcessingProvider
from processing.core.ProcessingConfig import ProcessingConfig, Setting
from .snap_reach import SnapReachAlgorithm
from .flow_times import FlowTimesAlgorithm
from .sum_up_upstream import SumUpUpstreamAlgorithm
from .change_reach_direction import ChangeReachDirection
from .swmm_create_input import SwmmCreateInputAlgorithm
from .swmm_extract_results import SwmmExtractResultsAlgorithm
from .swmm_execute import SwmmExecuteAlgorithm

from PyQt5.QtGui import QIcon
import os

__author__ = 'Matthias Kuhn'
__date__ = '2017-11-18'
__copyright__ = '(C) 2017 by OPENGIS.ch'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'


class QgepProcessingProvider(QgsProcessingProvider):

    def __init__(self):
        QgsProcessingProvider.__init__(self)
        # AlgorithmProvider.__init__(self)

        self.activate = True

        # Load algorithms
        self.alglist = [SnapReachAlgorithm(), FlowTimesAlgorithm(), ChangeReachDirection(), SumUpUpstreamAlgorithm(
        ), SwmmCreateInputAlgorithm(), SwmmExtractResultsAlgorithm(), SwmmExecuteAlgorithm()]
        for alg in self.alglist:
            alg.provider = self

    def getAlgs(self):
        algs = [SnapReachAlgorithm(), FlowTimesAlgorithm(), SumUpUpstreamAlgorithm(), ChangeReachDirection(
        ), SwmmCreateInputAlgorithm(), SwmmExtractResultsAlgorithm(), SwmmExecuteAlgorithm()]
        return algs

    def id(self):
        return 'qgep'

    def name(self):
        """This is the name that will appear on the toolbox group.

        It is also used to create the command line name of all the
        algorithms from this provider.
        """
        return 'QGEP'

    def icon(self):
        return QIcon(self.svgIconPath())

    def svgIconPath(self):
        basepath = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(basepath, '..', 'icons', 'qgepIcon.svg')

    def loadAlgorithms(self):
        self.algs = self.getAlgs()
        for a in self.algs:
            self.addAlgorithm(a)

    def load(self):
        ProcessingConfig.settingIcons[self.name()] = self.icon()
        ProcessingConfig.addSetting(Setting(self.name(),
                                            'SWMM_PATH',
                                            self.tr(r'SWMM executable (e.g. C:\Program Files (x86)\EPA SWMM 5.1.013\swmm55.exe)'),
                                            None,
                                            valuetype=Setting.FILE))

        ProcessingConfig.readSettings()
        self.refreshAlgorithms()
        return True

    def unload(self):
        ProcessingConfig.removeSetting('SWMM_PATH')
