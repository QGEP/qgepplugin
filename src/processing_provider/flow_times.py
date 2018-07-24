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
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterVectorLayer,
    QgsProcessingParameterField,
    QgsWkbTypes
)

from ..tools.qgepnetwork import QgepGraphManager

from PyQt5.QtCore import QCoreApplication, QVariant

__author__ = 'Denis Rouzaud'
__date__ = '2018-07-19'
__copyright__ = '(C) 2018 by OPENGIS.ch'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'


class FlowTimesAlgorithm(QgsProcessingAlgorithm):
    """
    """

    DISTANCE = 'DISTANCE'
    REACH_LAYER = 'REACH_LAYER'
    FLOWTIMES_LAYER= 'FLOWTIMES_LAYER'
    FK_REACH_FIELD = 'FK_REACH_FIELD'
    FLOWTIMES_FIELD = 'FLOWTIMES_FIELD'
    OUTPUT = "OUTPUT"

    def group(self):
        return 'QGEP'

    def groupId(self):
        return 'qgep'

    def name(self):
        return 'qgep_flow_times'

    def displayName(self):
        return self.tr('Flow times downstream')

    def tr(self, text):
        return QCoreApplication.translate('flow_times', text)

    def flags(self):
        return super().flags() | QgsProcessingAlgorithm.FlagNoThreading

    def createInstance(self):
        return FlowTimesAlgorithm()

    def initAlgorithm(self, config=None):
        """Here we define the inputs and output of the algorithm, along
        with some other properties.
        """

        # The parameters
        description = self.tr('Reach layer')
        self.addParameter(QgsProcessingParameterVectorLayer(self.REACH_LAYER, description=description,
                                                            types=[QgsProcessing.TypeVectorLine]))
        description = self.tr('Flow times layer')
        self.addParameter(QgsProcessingParameterVectorLayer(self.FLOWTIMES_LAYER, description=description,
                                                            types=[QgsProcessing.TypeVector]))
        description = self.tr('Reach id field')
        self.addParameter(QgsProcessingParameterField(self.FK_REACH_FIELD, description=description,
                                                      parentLayerParameterName=self.FLOWTIMES_LAYER))
        description = self.tr('Flow times field')
        self.addParameter(QgsProcessingParameterField(self.FLOWTIMES_FIELD, description=description,
                                                      parentLayerParameterName=self.FLOWTIMES_LAYER,
                                                      type=QgsProcessingParameterField.Numeric))

        self.addParameter(QgsProcessingParameterFeatureSink(self.OUTPUT,
                                                            self.tr('Joined layer')))

    def processAlgorithm(self, parameters, context: QgsProcessingContext, feedback: QgsProcessingFeedback):
        """Here is where the processing itself takes place."""

        reach_layer = self.parameterAsVectorLayer(parameters, self.REACH_LAYER, context)
        flow_layer = self.parameterAsVectorLayer(parameters, self.FLOWTIMES_LAYER, context)
        fk_reach = self.parameterAsFields(parameters, self.FK_REACH_FIELD, context)
        flow_times = self.parameterAsFields(parameters, self.FLOWTIMES_FIELD, context)

        fields = QgsFields()
        fields.append(QgsField('flow_time', QVariant.Double))
        (sink, dest_id) = self.parameterAsSink(parameters, self.OUTPUT, context, fields,
                                               QgsWkbTypes.LineString, reach_layer.sourceCrs())

        if sink is None:
            raise QgsProcessingException(self.invalidSinkError(parameters, self.OUTPUT))

        iterator = reach_layer.getSelectedFeatures()
        feature_count = reach_layer.selectedFeatureCount()

        if feature_count != 1:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.REACH_LAYER))

        qgep_reach_feature = QgsFeature()
        iterator.nextFeature(qgep_reach_feature)
        assert qgep_reach_feature.isValid()
        qgep_reach_obj_id = qgep_reach_feature.attribute('obj_id')

        na = qgis_utils.plugins["qgepplugin"].network_analyzer

        reach_features = na.getFeaturesByAttr(na.getReachLayer(), 'obj_id', [qgep_reach_obj_id]).asDict()
        assert len(reach_features) > 0

        feedback.setProgress(50)

        from_pos = 1
        top_node = None
        for fid, reach_feature in reach_features.items():
            if from_pos > reach_feature.attribute('from_pos'):
                top_node = reach_feature.attribute('from_obj_id_interpolate')
                from_pos = reach_feature.attribute('from_pos')
        assert top_node is not None

        nodes = na.getFeaturesByAttr(na.getNodeLayer(), 'obj_id', [top_node]).asDict()
        assert len(nodes) == 1

        top_node_id = next(iter(nodes.values())).id()

        _, edges = na.getTree(top_node_id)

        cache_edge_features = na.getFeaturesById(na.getReachLayer(), [edge[2]['feature'] for edge in edges]).asDict()

        edge = edges[0]
        i = 0
        while True:
            if i >= len(edges):
                break
            edge = edges[i]
            print(cache_edge_features.keys())
            print(edge)
            edge_feature = cache_edge_features[edge[2]['feature']]
            # if top_pos != 1 => merge
            sf = QgsFeature()
            sf.initAttributes(fields.count())
            sf.setGeometry(edge_feature.geometry())
            sink.addFeature(sf, QgsFeatureSink.FastInsert)
            feedback.setProgress(50+i/len(edges)*50)
            i += 1


        polylines = na.getEdgeGeometry([edge[2]['feature'] for edge in edges])

        #f.setAttributes(attrs)
        #sink.addFeature(f, QgsFeatureSink.FastInsert)
        #feedback.setProgress(int(current * total))

        return {self.OUTPUT: dest_id}
