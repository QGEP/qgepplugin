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

import qgis.utils as qgis_utils
import os, re

from qgis.core import (
    QgsExpression,
    QgsFeature,
    QgsFeatureRequest,
    QgsFeatureSink,
    QgsField,
    QgsFields,
    QgsGeometry,
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingContext,
    QgsProcessingException,
    QgsProcessingFeedback,
    QgsProcessingParameterString,
    QgsProcessingParameterFile,
    QgsProcessingParameterFileDestination,
    QgsWkbTypes,
    QgsProcessingParameterFeatureSink
)

from processing.core.ProcessingConfig import ProcessingConfig

from .qgep_algorithm import QgepAlgorithm
from .QgepSwmm import QgepSwmm

from ..tools.qgepnetwork import QgepGraphManager

from PyQt5.QtCore import QCoreApplication, QVariant

__author__ = 'Timothée Produit'
__date__ = '2019-08-01'
__copyright__ = '(C) 2019 by IG-Group.ch'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'


class SwmmExecuteAlgorithm(QgepAlgorithm):
    """
    """

    INP_FILE = 'INP_FILE'
    OUT_FILE = 'OUT_FILE'
    LOG_FILE = 'LOG_FILE'


    def name(self):
        return 'swmm_execute'

    def displayName(self):
        return self.tr('SWMM Execute')

    def initAlgorithm(self, config=None):
        """Here we define the inputs and output of the algorithm, along
        with some other properties.
        """

        # The parameters
        description = self.tr('INP File')
        self.addParameter(QgsProcessingParameterFile(self.INP_FILE, description=description, extension="inp"))
        
        description = self.tr('OUT File')
        self.addParameter(QgsProcessingParameterFileDestination(self.OUT_FILE, description=description, fileFilter="out (*.out)"))
        
        description = self.tr('LOG File')
        self.addParameter(QgsProcessingParameterFileDestination(self.LOG_FILE, description=description, fileFilter="log (*.log)"))
        
        
    def processAlgorithm(self, parameters, context: QgsProcessingContext, feedback: QgsProcessingFeedback):
        """Here is where the processing itself takes place."""
        
        # init params
        log_file = self.parameterAsFile(parameters, self.LOG_FILE, context)
        output_file = self.parameterAsFile(parameters, self.OUT_FILE, context)
        inp_file = self.parameterAsFileOutput(parameters, self.INP_FILE, context)
        swmm_cli = os.path.abspath(ProcessingConfig.getSetting('SWMM_PATH'))
        if not swmm_cli:
            #raise GeoAlgorithmExecutionException(
            #'Swmm command line toom is not configured.\n\
            # Please configure it before running Swmm algorithms.')
            raise QgsProcessingException(
                    'Swmm command line toom is not configured.\n\
                    Please configure it before running Swmm algorithms.'
                    )
            pass
        
        qs = QgepSwmm(None, None, inp_file, None, output_file, log_file, swmm_cli, None)
        prompt = qs.execute_swmm()
        
        feedback.pushInfo(prompt)
        
        if re.search('There are errors', prompt):
            feedback.reportError(prompt)
            feedback.reportError('There were errors, look into logs for details: {log_file}'.format(log_file=log_file))


        feedback.setProgress(100)


        return {}
