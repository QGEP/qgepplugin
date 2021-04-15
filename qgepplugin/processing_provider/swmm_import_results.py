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
    QgsProcessingContext,
    QgsProcessingException,
    QgsProcessingFeedback,
    QgsProcessingParameterFile,
    QgsProcessingParameterBoolean,
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

    RPT_FILE = 'RPT_FILE'
    DATABASE = 'DATABASE'
    SIM_DESCRIPTION = 'SIM_DESCRIPTION'
    IMPORT_FULL_RESULTS = 'IMPORT_FULL_RESULTS'

    def name(self):
        return 'swmm_import_results'

    def displayName(self):
        return self.tr('SWMM Import Results')

    def initAlgorithm(self, config=None):
        """Here we define the inputs and output of the algorithm, along
        with some other properties.
        """

        # The parameters
        description = self.tr('SWMM report file (.rpt)')
        self.addParameter(QgsProcessingParameterFile(self.RPT_FILE, description=description))

        description = self.tr('Database')
        self.addParameter(QgsProcessingParameterString(
            self.DATABASE, description=description, defaultValue="pg_qgep_demo_data"))

        description = self.tr('Simulation name')
        self.addParameter(QgsProcessingParameterString(
            self.SIM_DESCRIPTION, description=description, defaultValue="SWMM simulation, rain T100, current"))

        description = self.tr('Import full results in addition to summary')
        self.addParameter(QgsProcessingParameterBoolean(
            self.IMPORT_FULL_RESULTS, description=description, defaultValue=False))

    def processAlgorithm(self, parameters, context: QgsProcessingContext, feedback: QgsProcessingFeedback):
        """Here is where the processing itself takes place."""

        feedback.pushInfo('The import started, it can take a few minutes.')
        feedback.setProgress(1)

        # init params
        rpt_file = self.parameterAsFileOutput(parameters, self.RPT_FILE, context)
        database = self.parameterAsString(parameters, self.DATABASE, context)
        sim_description = self.parameterAsString(parameters, self.SIM_DESCRIPTION, context)
        import_full_result = self.parameterAsBoolean(parameters, self.IMPORT_FULL_RESULTS, context)

        # Get node summary from output file
        with QgepSwmm(sim_description, database, None, None, None, rpt_file, None, feedback) as qs:
            qs.import_summary(sim_description)
            if import_full_result:
                qs.import_full_results(sim_description)

        feedback.setProgress(100)

        return {}
