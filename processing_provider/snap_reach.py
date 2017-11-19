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

from processing.core.GeoAlgorithm import GeoAlgorithm
from processing.core.parameters import (
    ParameterNumber,
    ParameterVector,
    ParameterBoolean
)
from processing.tools import dataobjects

from qgis.core import (
    QgsExpression,
    QgsFeatureRequest,
    QgsGeometry,
)

__author__ = 'Matthias Kuhn'
__date__ = '2017-11-18'
__copyright__ = '(C) 2017 by OPENGIS.ch'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'


class SnapReachAlgorithm(GeoAlgorithm):
    """
    """

    DISTANCE = 'DISTANCE'
    REACH_LAYER = 'REACH_LAYER'
    WASTEWATER_NODE_LAYER = 'WASTEWATER_NODE_LAYER'
    ONLY_SELECTED = 'ONLY_SELECTED'

    def defineCharacteristics(self):
        """Here we define the inputs and output of the algorithm, along
        with some other properties.
        """

        # The name that the user will see in the toolbox
        self.name = 'Snap reach geometry'

        # The branch of the toolbox under which the algorithm will appear
        self.group = 'QGEP'

        # The parameters
        self.addParameter(
            ParameterNumber(self.DISTANCE, description=self.tr('Maximum snapping distance in meters. Set to 0 for no maximum.'), default=10.0))
        self.addParameter(
            ParameterBoolean(self.ONLY_SELECTED, description=self.tr('Snap only selected reaches.'), default=True))
        self.addParameter(ParameterVector(self.REACH_LAYER, description=self.tr(
            'Reach layer, will be modified in place and used as snapping target')))
        self.addParameter(ParameterVector(self.WASTEWATER_NODE_LAYER, description=self.tr(
            'Wastewater node layer, will be used as snapping target')))

    def processAlgorithm(self, progress):
        """Here is where the processing itself takes place."""

        reach_layer_uri = self.getParameterValue(self.REACH_LAYER)
        reach_layer = dataobjects.getObjectFromUri(reach_layer_uri)
        distance = self.getParameterValue(self.DISTANCE)
        only_selected = self.getParameterValue(self.ONLY_SELECTED)
        wastewater_node_layer_uri = self.getParameterValue(
            self.WASTEWATER_NODE_LAYER)
        wastewater_node_layer = dataobjects.getObjectFromUri(
            wastewater_node_layer_uri)

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
                progress.setPercentage(current_feature * 100.0 / feature_count)

            self.processFeatures(reaches, reach_layer,
                                 wastewater_node_layer, distance)
        except:
            reach_layer.destroyEditCommand()
            raise
        reach_layer.endEditCommand()
        progress.setPercentage(100)

    def processFeatures(self, reaches, reach_layer, wastewater_node_layer, distance_threshold):
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
            ids=','.join(quoted_ids))
        reach_request.setFilterExpression(filter_expression)
        reach_request.setSubsetOfAttributes([])

        target_reaches = dict()
        for target_reach in reach_layer.getFeatures(reach_request):
            target_reaches[target_reach['obj_id']] = target_reach

        for reach in reaches:
            reach_geometry = QgsGeometry(reach.geometry())
            from_id = reach['rp_from_fk_wastewater_networkelement']
            if from_id in nodes.keys():
                if distance_threshold == 0 or reach_geometry.sqrDistToVertexAt(nodes[from_id].geometry().asPoint(), 0) < distance_threshold:
                    reach_geometry.moveVertex(
                        nodes[from_id].geometry().geometry(), 0)

            to_id = reach['rp_to_fk_wastewater_networkelement']
            if to_id in nodes.keys():
                last_vertex = reach_geometry.geometry().nCoordinates() - 1
                if distance_threshold == 0 or reach_geometry.sqrDistToVertexAt(nodes[to_id].geometry().asPoint(), last_vertex) < distance_threshold:
                    reach_geometry.moveVertex(
                        nodes[to_id].geometry().geometry(), last_vertex)

            if to_id in target_reaches.keys():
                last_vertex = reach_geometry.geometry().nCoordinates() - 1
                target_reach = target_reaches[to_id]
                distance, point, after_vertex = target_reach.geometry(
                ).closestSegmentWithContext(reach_geometry.vertexAt(last_vertex))
                if distance_threshold == 0 or distance < distance_threshold:
                    reach_geometry.moveVertex(
                        point.x(), point.y(), last_vertex)

            reach.setGeometry(reach_geometry)
            reach_layer.updateFeature(reach)
