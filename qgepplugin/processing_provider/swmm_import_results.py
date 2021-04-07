# -*- coding: utf-8 -*-

"""
/***************************************************************************
 QGEP-swmm processing provider
                              -------------------
        begin                : 07.2019
        copyright            : (C) 2019 by ig-group.ch
        email                : timothee.produit@ig-group.ch
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

from qgis.core import (
    #QgsFeature,
    #QgsFeatureSink,
    #QgsField,
    #QgsFields,
    QgsProcessingContext,
    QgsProcessingException,
    QgsProcessingFeedback,
    QgsProcessingParameterFile,
    # QgsProcessingParameterFeatureSink
    QgsProcessingParameterString
)

from .qgep_algorithm import QgepAlgorithm
from .QgepSwmm import QgepSwmm

from PyQt5.QtCore import QVariant

__author__ = 'Timothée Produit'
__date__ = '2021-04-30'
__copyright__ = '(C) 2021 by map.ig-group.ch'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'


class SwmmImportResultsAlgorithm(QgepAlgorithm):
    """
    """

    OUT_FILE = 'OUT_FILE'
    DATABASE = 'DATABASE'
    SIM_DESCRIPTION = 'SIM_DESCRIPTION'

    def name(self):
        return 'swmm_import_results'

    def displayName(self):
        return self.tr('SWMM Import Results')

    def initAlgorithm(self, config=None):
        """Here we define the inputs and output of the algorithm, along
        with some other properties.
        """

        # The parameters
        description = self.tr('SWMM summary file (.rpt)')
        self.addParameter(QgsProcessingParameterFile(self.OUT_FILE, description=description))

        description = self.tr('Database')
        self.addParameter(QgsProcessingParameterString(
            self.DATABASE, description=description, defaultValue="pg_qgep_demo_data"))

        description = self.tr('Simulation name')
        self.addParameter(QgsProcessingParameterString(
            self.SIM_DESCRIPTION, description=description, defaultValue="SWMM simulation, rain T100, current"))


    def processAlgorithm(self, parameters, context: QgsProcessingContext, feedback: QgsProcessingFeedback):
        """Here is where the processing itself takes place."""

        feedback.pushInfo('The import started, it can take a few minutes.')
        feedback.setProgress(1)

        # init params
        out_file = self.parameterAsFileOutput(parameters, self.OUT_FILE, context)
        database = self.parameterAsString(parameters, self.DATABASE, context)
        sim_description = self.parameterAsString(parameters, self.SIM_DESCRIPTION, context)

        # Get node summary from output file
        #qs = QgepSwmm(sim_description, database, None, None, None, out_file, None, None, feedback)
        #qs.import_results(sim_description)
        with QgepSwmm(sim_description, database, None, None, None, out_file, None, None, feedback) as qs:
            qs.import_results(sim_description)
        
        feedback.setProgress(100)

        return {}
