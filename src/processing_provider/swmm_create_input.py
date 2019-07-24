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

import datetime

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
    QgsWkbTypes
)

from .qgep_algorithm import QgepAlgorithm
from .QgepSwmm import QgepSwmm

from ..tools.qgepnetwork import QgepGraphManager

from PyQt5.QtCore import QCoreApplication, QVariant

__author__ = 'Timothée Produit'
__date__ = '2019-08-01'
__copyright__ = '(C) 2019 by IG-Group.ch'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'


class SwmmCreateInputAlgorithm(QgepAlgorithm):
    """
    """

    DATABASE = 'DATABASE'
    TEMPLATE_INP_FILE = 'TEMPLATE_INP_FILE'
    INP_FILE = 'INP_FILE'

    def name(self):
        return 'swmm_create_input'

    def displayName(self):
        return self.tr('SWMM Create Input')

    def initAlgorithm(self, config=None):
        """Here we define the inputs and output of the algorithm, along
        with some other properties.
        """

        # The parameters
        description = self.tr('Database')
        self.addParameter(QgsProcessingParameterString(self.DATABASE, description=description, defaultValue="pg_qgep_demo_data"))
        
        description = self.tr('Template INP File')
        self.addParameter(QgsProcessingParameterFile(self.TEMPLATE_INP_FILE, description=description))
        
        description = self.tr('Result INP File')
        self.addParameter(QgsProcessingParameterFileDestination(self.INP_FILE, description=description))


    def processAlgorithm(self, parameters, context: QgsProcessingContext, feedback: QgsProcessingFeedback):
        """Here is where the processing itself takes place."""

        feedback.setProgress(0)

        # init params
        database = self.parameterAsString(parameters, self.DATABASE, context)
        template_inp_file = self.parameterAsFile(parameters, self.TEMPLATE_INP_FILE, context)
        inp_file = self.parameterAsFileOutput(parameters, self.INP_FILE, context)
        
        # Connect to QGEP database and perform translation
        qs = QgepSwmm(datetime.datetime.today().isoformat(), database, inp_file, template_inp_file, None)
        qs.write_input()
        
        #while reading_some_data():
        #feedback.setProgress(100)
        #    write_data

        return {self.INP_FILE: inp_file}
