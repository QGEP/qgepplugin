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
    QgsWkbTypes,
    QgsProcessingParameterFeatureSink
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


class SwmmExtractResultsAlgorithm(QgepAlgorithm):
    """
    """

    OUT_FILE = 'OUT_FILE'
    NODE_SUMMARY = 'NODE_SUMMARY'
    LINK_SUMMARY = 'LINK_SUMMARY'
    XSECTION_SUMMARY = 'XSECTION_SUMMARY'

    def name(self):
        return 'swmm_extract_results'

    def displayName(self):
        return self.tr('SWMM Extract Results')

    def initAlgorithm(self, config=None):
        """Here we define the inputs and output of the algorithm, along
        with some other properties.
        """

        # The parameters
        description = self.tr('OUT File')
        self.addParameter(QgsProcessingParameterFile(self.OUT_FILE, description=description))
        
        self.addParameter(QgsProcessingParameterFeatureSink(self.NODE_SUMMARY,self.tr('Node summary')))
        self.addParameter(QgsProcessingParameterFeatureSink(self.LINK_SUMMARY,self.tr('Link summary')))
        self.addParameter(QgsProcessingParameterFeatureSink(self.XSECTION_SUMMARY,self.tr('Cross section summary')))


    def processAlgorithm(self, parameters, context: QgsProcessingContext, feedback: QgsProcessingFeedback):
        """Here is where the processing itself takes place."""

        feedback.setProgress(0)

        # init params
        out_file = self.parameterAsFileOutput(parameters, self.OUT_FILE, context)
        
        # create feature sink for node summary
        fields = QgsFields()

        fields.append(QgsField('id', QVariant.String))
        fields.append(QgsField('type', QVariant.String))
        fields.append(QgsField('average_depth', QVariant.Double))
        fields.append(QgsField('maximum_depth', QVariant.Double))
        fields.append(QgsField('maximum_hgl', QVariant.Double))
        fields.append(QgsField('time_max_day', QVariant.Int))
        fields.append(QgsField('time_max_time', QVariant.Double))
        fields.append(QgsField('reported_max_depth', QVariant.Double))
        (sinkNode, dest_id) = self.parameterAsSink(parameters, self.NODE_SUMMARY, context, fields)
        if sinkNode is None:
            raise QgsProcessingException(self.invalidSinkError(parameters, self.NODE_SUMMARY))
            
        # Get node summary from output file
        qs = QgepSwmm(None, None, None, None, out_file)
        node_summary = qs.extract_node_depth_summary()
        
        # Fill node summary with data
        for ns in node_summary:
            print ('ns', ns)
            sf = QgsFeature()
            sf.setFields(fields)
            for k in ns.keys():
                sf.setAttribute(k, ns[k])
            sinkNode.addFeature(sf, QgsFeatureSink.FastInsert)
        feedback.setProgress(50)
        
        # create feature sink for link summary
        fields = QgsFields()
        fields.append(QgsField('id', QVariant.String))
        fields.append(QgsField('type', QVariant.String))
        fields.append(QgsField('maximum_flow', QVariant.Double))
        fields.append(QgsField('time_max_day', QVariant.Int))
        fields.append(QgsField('time_max_time', QVariant.String))
        fields.append(QgsField('maximum_velocity', QVariant.Double))
        fields.append(QgsField('max_over_full_flow', QVariant.Double))
        fields.append(QgsField('max_over_full_depth', QVariant.Double))
        (sinkLink, dest_id) = self.parameterAsSink(parameters, self.LINK_SUMMARY, context, fields)
        if sinkLink is None:
            raise QgsProcessingException(self.invalidSinkError(parameters, self.LINK_SUMMARY))
            
        # Get link summary from output file
        link_summary = qs.extract_link_flow_summary()
        
        # Fill node summary with data
        for ns in link_summary:
            sf = QgsFeature()
            sf.setFields(fields)
            for k in ns.keys():
                sf.setAttribute(k, ns[k])
            sinkLink.addFeature(sf, QgsFeatureSink.FastInsert)
        feedback.setProgress(100)
        

        return {self.NODE_SUMMARY: sinkNode, self.LINK_SUMMARY: sinkLink}