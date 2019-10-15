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

#import qgis.utils as qgis_utils

import datetime

from qgis.core import (
   # QgsExpression,
    #QgsFeature,
    #QgsFeatureRequest,
    #QgsFeatureSink,
    #QgsField,
    #QgsFields,
    #QgsGeometry,
    #QgsProcessing,
    #QgsProcessingAlgorithm,
    QgsProcessingContext,
    #QgsProcessingException,
    QgsProcessingFeedback,
    QgsProcessingParameterString,
    #QgsProcessingParameterFile,
    QgsProcessingParameterFolderDestination,
    #QgsWkbTypes
)

from .qgep_algorithm import QgepAlgorithm
from .QgepSwmm import QgepSwmm

#from ..tools.qgepnetwork import QgepGraphManager

#from PyQt5.QtCore import QCoreApplication#, QVariant

__author__ = 'Timothée Produit'
__date__ = '2019-08-01'
__copyright__ = '(C) 2019 by IG-Group.ch'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'


class SwmmCreateDbTables(QgepAlgorithm):
    """
    """

    DBMODELPATH = 'DBMODELPATH'
    DATABASE = 'DATABASE'

    def name(self):
        return 'swmm_create_db_tables'

    def displayName(self):
        return self.tr('SWMM Create DB Tables')

    def initAlgorithm(self, config=None):
        """Here we define the inputs and output of the algorithm, along
        with some other properties.
        """

        # The parameters
        description = self.tr('Database')
        self.addParameter(QgsProcessingParameterString(self.DATABASE, description=description, defaultValue="pg_qgep_demo_data"))
        
        description = self.tr('Path to DB Model SQL')
        self.addParameter(QgsProcessingParameterFolderDestination(self.DBMODELPATH, description=description))
        

    def processAlgorithm(self, parameters, context: QgsProcessingContext, feedback: QgsProcessingFeedback):
        """Here is where the processing itself takes place."""

        feedback.setProgress(0)

        # init params
        database = self.parameterAsString(parameters, self.DATABASE, context)
        db_model_path = self.parameterAsFile(parameters, self.DBMODELPATH, context)
        
        # Connect to QGEP database and perform translation
        qs = QgepSwmm(datetime.datetime.today().isoformat(), database, None, None, None, None, None, db_model_path)
        qs.create_swmm_schema()
        feedback.setProgress(25)
        qs.create_swmm_views()
        feedback.setProgress(50)
        qs.delete_swmm_tables()
        feedback.setProgress(75)
        qs.create_fill_swmm_tables()
        feedback.setProgress(100)

        return {}
