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
    QgsFeatureRequest,
    QgsGeometry,
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingException,
    QgsProcessingParameterNumber,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterVectorLayer,
    QgsProcessingParameterField
)

from ..tools.qgepnetwork import QgepGraphManager

from PyQt5.QtCore import QCoreApplication

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

    def group(self):
        return 'QGEP'

    def groupId(self):
        return 'qgep'

    def name(self):
        return self.tr('Flow times downstream')

    def displayName(self):
        return self.name()

    def tr(self, text):
        return QCoreApplication.translate('flow_times', text)

    def flags(self):
        return super().flags() | QgsProcessingAlgorithm.FlagNoThreading

    def initAlgorithm(self, config=None):
        """Here we define the inputs and output of the algorithm, along
        with some other properties.
        """

        # The parameters
        description = self.tr('Reach layer')
        self.addParameter(QgsProcessingParameterVectorLayer(self.REACH_LAYER, description=description,
                                                            types=[QgsProcessing.TypeVectorLine]))
        description = self.tr('Flow times layer')
        self.addParameter(QgsProcessingParameterVectorLayer(self.FLOWTIMES_LAYER, description=description))
        description = self.tr('Reach id field')
        self.addParameter(QgsProcessingParameterField(self.FK_REACH_FIELD, description=description,
                                                      parentLayerParameterName=self.FLOWTIMES_LAYER))
        description = self.tr('Flow times field')
        self.addParameter(QgsProcessingParameterField(self.FLOWTIMES_FIELD, description=description,
                                                      parentLayerParameterName=self.FLOWTIMES_LAYER,
                                                      type=QgsProcessingParameterField.Numeric))


    def processAlgorithm(self, parameters, context, feedback):
        """Here is where the processing itself takes place."""

        reach_layer = self.parameterAsVectorLayer(parameters, self.REACH_LAYER)
        flow_layer = self.parameterAsVectorLayer(parameters, self.FLOWTIMES_LAYER)
        fk_reach = self.parameterAsFields(parameters, self.FK_REACH_FIELD, context)
        flow_times = self.parameterAsFields(parameters, self.FLOWTIMES_FIELD, context)

        iterator = reach_layer.selectedFeaturesIterator()
        feature_count = reach_layer.selectedFeatureCount()

        if feature_count != 1:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.REACH_LAYER))

        reach_feature = iterator.next()
        assert reach_feature.isValid()

        na = qgis_utils.plugins["qgep"].network_analyzer

        top_point = reach_feature.geometry().asPolygonXY()[0]

        match = na.snapToMap(top_point)

        if not match.isValid():
            raise QgsProcessingException(self.tr('Could not determine starting node'))

        nodes, edges = na.getTree(top_point)
        polylines = na.getEdgeGeometry([edge[2]['feature'] for edge in edges])

        return

        reach_layer.startEditing()

        feature_count = 0
        if only_selected:
            iterator = reach_layer.selectedFeaturesIterator()
            feature_count = reach_layer.selectedFeatureCount()
        else:
            iterator = reach_layer.getFeatures()
            feature_count = reach_layer.featureCount()

        # Loop through relevant reaches
        reach_layer.beginEditCommand('Snap reaches to points')
        try:
            reaches = list()
            current_feature = 0
            for reach in iterator:
                reaches.append(reach)
                # Batch processing: process blocks of 2000 reaches
                if len(reaches) == 2000:
                    self.processFeatures(
                        reaches, reach_layer, wastewater_node_layer, distance)
                    reaches = list()

                current_feature += 1
                feedback.setProgress(current_feature * 100.0 / feature_count)

            self.processFeatures(reaches, reach_layer,
                                 wastewater_node_layer, distance)
        except:  # NOQA
            reach_layer.destroyEditCommand()
            raise
        reach_layer.endEditCommand()
        feedback.setProgress(100)

    def processFeatures(self, reaches, reach_layer, wastewater_node_layer, distance_threshold):

        return

        ids = list()
        to_ids = list()
        # Gather ids of connected networkelements
        # to_ids are also gathered separately, because they can be either
        # reaches or nodes
        for reach in reaches:
            if reach['rp_from_fk_wastewater_networkelement']:
                ids.append(reach['rp_from_fk_wastewater_networkelement'])

            if reach['rp_to_fk_wastewater_networkelement']:
                ids.append(reach['rp_to_fk_wastewater_networkelement'])
                to_ids.append(reach['rp_to_fk_wastewater_networkelement'])

        # Get all nodes on which to snap
        quoted_ids = [QgsExpression.quotedValue(objid) for objid in ids]
        node_request = QgsFeatureRequest()
        filter_expression = '"obj_id" IN ({ids})'.format(
            ids=','.join(quoted_ids))
        node_request.setFilterExpression(filter_expression)
        node_request.setSubsetOfAttributes([])

        nodes = dict()
        for node in wastewater_node_layer.getFeatures(node_request):
            nodes[node['obj_id']] = node

        # Get all reaches on which to snap
        quoted_to_ids = [QgsExpression.quotedValue(objid) for objid in to_ids]
        reach_request = QgsFeatureRequest()
        filter_expression = '"obj_id" IN ({ids})'.format(
            ids=','.join(quoted_to_ids))
        reach_request.setFilterExpression(filter_expression)
        reach_request.setSubsetOfAttributes([])

        target_reaches = dict()
        for target_reach in reach_layer.getFeatures(reach_request):
            target_reaches[target_reach['obj_id']] = target_reach

        for reach in reaches:
            reach_geometry = QgsGeometry(reach.geometry())
            from_id = reach['rp_from_fk_wastewater_networkelement']
            if from_id in list(nodes.keys()):
                if distance_threshold == 0 or reach_geometry.sqrDistToVertexAt(nodes[from_id].geometry().asPoint(), 0) < distance_threshold:
                    reach_geometry.moveVertex(
                        nodes[from_id].geometry().geometry(), 0)

            to_id = reach['rp_to_fk_wastewater_networkelement']
            if to_id in list(nodes.keys()):
                last_vertex = reach_geometry.geometry().nCoordinates() - 1
                if distance_threshold == 0 or reach_geometry.sqrDistToVertexAt(nodes[to_id].geometry().asPoint(), last_vertex) < distance_threshold:
                    reach_geometry.moveVertex(
                        nodes[to_id].geometry().geometry(), last_vertex)

            if to_id in list(target_reaches.keys()):
                last_vertex = reach_geometry.geometry().nCoordinates() - 1
                target_reach = target_reaches[to_id]
                distance, point, after_vertex = target_reach.geometry(
                ).closestSegmentWithContext(reach_geometry.vertexAt(last_vertex))
                if distance_threshold == 0 or distance < distance_threshold:
                    reach_geometry.moveVertex(
                        point.x(), point.y(), last_vertex)

            reach.setGeometry(reach_geometry)
            reach_layer.updateFeature(reach)
