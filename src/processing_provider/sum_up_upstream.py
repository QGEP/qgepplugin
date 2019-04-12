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


import qgis
from qgis.core import (
    QgsExpression,
    QgsExpressionContext,
    QgsExpressionContextUtils,
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
    QgsProcessingParameterDefinition,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterVectorLayer,
    QgsProcessingParameterExpression,
    QgsProcessingParameterField,
    QgsWkbTypes,
    NULL
)

from .qgep_algorithm import QgepAlgorithm
from ..tools.qgepnetwork import QgepGraphManager

from PyQt5.QtCore import QCoreApplication, QVariant

__author__ = 'Matthias Kuhn'
__date__ = '2019-04-09'
__copyright__ = '(C) 2018 by OPENGIS.ch'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'


class SumUpUpstreamAlgorithm(QgepAlgorithm):
    """
    """

    REACH_LAYER = 'REACH_LAYER'
    WASTEWATER_NODE_LAYER= 'WASTEWATER_NODE_LAYER'
    VALUE_EXPRESSION = 'VALUE_EXPRESSION'
    REACH_PK_NAME = 'REACH_PK_NAME'
    NODE_PK_NAME = 'NODE_PK_NAME'
    NODE_FROM_FK_NAME = 'NODE_FROM_FK_NAME'
    NODE_TO_FK_NAME = 'NODE_TO_FK_NAME'


    OUTPUT = "OUTPUT"

    def name(self):
        return 'qgep_values_upstream'

    def displayName(self):
        return self.tr('Sum up upstream')

    def initAlgorithm(self, config=None):
        """Here we define the inputs and output of the algorithm, along
        with some other properties.
        """

        # The parameters
        description = self.tr('Source Value Expression')
        self.addParameter(QgsProcessingParameterExpression(self.VALUE_EXPRESSION, description=description,
                                                      parentLayerParameterName=self.REACH_LAYER))

        description = self.tr('Reach Layer')
        self.addAdvancedParameter(QgsProcessingParameterVectorLayer(self.REACH_LAYER, description=description,
                                                            types=[QgsProcessing.TypeVectorLine], defaultValue='vw_qgep_reach'))
        description = self.tr('Wastewater Node Layer')
        self.addAdvancedParameter(QgsProcessingParameterVectorLayer(self.WASTEWATER_NODE_LAYER, description=description,
                                                            types=[QgsProcessing.TypeVector], defaultValue='vw_wastewater_node'))

        description = self.tr('Primary Key Field Reach')
        self.addAdvancedParameter(QgsProcessingParameterField(self.REACH_PK_NAME, description=description,
                                                      parentLayerParameterName=self.REACH_LAYER, defaultValue='obj_id'))

        description = self.tr('Primary Key Field Node')
        self.addAdvancedParameter(QgsProcessingParameterField(self.NODE_PK_NAME, description=description,
                                                      parentLayerParameterName=self.WASTEWATER_NODE_LAYER, defaultValue='obj_id'))

        description = self.tr('Foreign Key Field From')
        self.addAdvancedParameter(QgsProcessingParameterField(self.NODE_FROM_FK_NAME, description=description,
                                                           parentLayerParameterName=self.REACH_LAYER,
                                                           defaultValue='rp_from_fk_wastewater_networkelement'))

        description = self.tr('Foreign Key Field To')
        self.addAdvancedParameter(QgsProcessingParameterField(self.NODE_TO_FK_NAME, description=description,
                                                           parentLayerParameterName=self.REACH_LAYER,
                                                           defaultValue='rp_to_fk_wastewater_networkelement'))

        self.addParameter(QgsProcessingParameterFeatureSink(self.OUTPUT,
                                                            self.tr('Summed up')))

    def addAdvancedParameter(self, parameter):
        parameter.setFlags(parameter.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(parameter)

    def processAlgorithm(self, parameters, context: QgsProcessingContext, feedback: QgsProcessingFeedback):
        """Here is where the processing itself takes place."""

        feedback.setProgress(0)

        # init params
        reach_layer = self.parameterAsVectorLayer(parameters, self.REACH_LAYER, context)
        wastewater_node_layer = self.parameterAsVectorLayer(parameters, self.WASTEWATER_NODE_LAYER, context)
        value_expression = self.parameterAsExpression(parameters, self.VALUE_EXPRESSION, context)
        reach_pk_name = self.parameterAsFields(parameters, self.REACH_PK_NAME, context)[0]
        node_pk_name = self.parameterAsFields(parameters, self.NODE_PK_NAME, context)[0]
        node_from_fk_name = self.parameterAsFields(parameters, self.NODE_FROM_FK_NAME, context)[0]
        node_to_fk_name = self.parameterAsFields(parameters, self.NODE_TO_FK_NAME, context)[0]

        # create feature sink
        fields = wastewater_node_layer.fields()
        fields.append(QgsField('value', QVariant.Double))
        (sink, dest_id) = self.parameterAsSink(parameters, self.OUTPUT, context, fields,
                                               QgsWkbTypes.Point, reach_layer.sourceCrs())
        if sink is None:
            raise QgsProcessingException(self.invalidSinkError(parameters, self.OUTPUT))

        feature_count = reach_layer.featureCount()

        reaches = dict()

        expression = QgsExpression(value_expression)
        context = QgsExpressionContext(QgsExpressionContextUtils.globalProjectLayerScopes(reach_layer))
        expression.prepare(context)

        for reach in reach_layer.getFeatures(QgsFeatureRequest()):
            context.setFeature(reach)
            value = expression.evaluate(context)
            reaches[reach[node_from_fk_name]] = (reach[node_from_fk_name], reach[node_to_fk_name], value)

        qgis.reaches = reaches

        all_nodes = dict()

        current_feature = 0
        for node in wastewater_node_layer.getFeatures():
            time = 0.0

            from_node_id = node[node_pk_name]
            start_node_id = from_node_id

            processed_nodes = []
            while from_node_id in reaches.keys():
                if from_node_id in processed_nodes:
                    feedback.reportError('Loop detected with nodes {}'.format(processed_nodes))
                    break
                current_reach = reaches[from_node_id]
                to_node_id = current_reach[1]
                time += current_reach[2]
                processed_nodes.append(from_node_id)
                from_node_id = to_node_id

            current_feature += 1

            new_node = QgsFeature(node)
            new_node.setFields(fields)
            new_node['value'] = time

            sink.addFeature(new_node, QgsFeatureSink.FastInsert)
            feedback.setProgress(current_feature/feature_count * 100)

        return {self.OUTPUT: dest_id}
