# -*- coding: utf-8 -*-
# -----------------------------------------------------------
#
# Qgep
# Copyright (C) 2012  Matthias Kuhn
# -----------------------------------------------------------
#
# licensed under the terms of GNU GPL 2
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, print to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# ---------------------------------------------------------------------

"""
This module implements several map tools for QGEP
"""

from qgis.core import (
    QgsGeometry,
    QgsPoint
)
from qgis.gui import (
    QgsMapTool,
    QgsRubberBand,
    QgsVertexMarker,
    QgsMessageBar
)
from PyQt4.QtGui import (
    QCursor,
    QColor,
    QApplication)
from PyQt4.QtCore import (
    Qt,
    QPoint,
    pyqtSignal,
    QSettings
)
from .qgepprofile import (
    QgepProfile,
    QgepProfileNodeElement,
    QgepProfileReachElement,
    QgepProfileSpecialStructureElement
)

import logging


class QgepMapTool(QgsMapTool):
    """
    Base class for all the map tools
    """

    highLightedPoints = []
    logger = logging.getLogger(__name__)

    def __init__(self, iface, button):
        QgsMapTool.__init__(self, iface.mapCanvas())
        self.canvas = iface.mapCanvas()
        self.cursor = QCursor(Qt.CrossCursor)
        self.button = button
        self.msgBar = iface.messageBar()

        settings = QSettings()
        current_profile_color = settings.value("/QGEP/CurrentProfileColor", u'#FF9500')

        self.rubberBand = QgsRubberBand(self.canvas)
        self.rubberBand.setColor(QColor(current_profile_color))
        self.rubberBand.setWidth(3)

    def activate(self):
        """
        Gets called when the tool is activated
        """
        QgsMapTool.activate(self)
        self.canvas.setCursor(self.cursor)
        self.button.setChecked(True)

    def deactivate(self):
        """
        Gets called whenever the tool is deactivated directly or indirectly
        """
        QgsMapTool.deactivate(self)
        self.button.setChecked(False)

    # pylint: disable=no-self-use
    def isZoomTool(self):
        """
        Will return if this is a zoom tool
        """
        return False

    def setCursor(self, cursor):
        """
        Set the cursor for this maptool
        """
        self.cursor = QCursor(cursor)

    # ===========================================================================
    # Events
    # ===========================================================================

    def canvasReleaseEvent(self, event):
        """
        Issues rightClicked and leftClicked events
        """
        if event.button() == Qt.RightButton:
            self.rightClicked(event)
        else:
            self.leftClicked(event)

    def canvasDoubleClickEvent(self, event):
        """
        Forwards to doubleClicked
        """
        try:
            self.doubleClicked(event)
        except AttributeError:
            pass


class QgepProfileMapTool(QgepMapTool):
    """
    The map tool used for PROFILE

    Allows to find the shortest path between several nodes.
    """
    profileChanged = pyqtSignal(object)
    profile = QgepProfile()
    segmentOffset = 0

    selectedPathPoints = []
    pathPolyline = []

    def __init__(self, canvas, button, network_analyzer):
        QgepMapTool.__init__(self, canvas, button)
        settings = QSettings()

        helper_line_color = settings.value("/QGEP/HelperLineColor", u'#FFD900')
        highlight_color = settings.value("/QGEP/HighlightColor", u'#40FF40')

        self.networkAnalyzer = network_analyzer

        # Init rubberband to visualize current status
        self.rbHelperLine = QgsRubberBand(self.canvas)
        self.rbHelperLine.setColor(QColor(helper_line_color))
        self.rbHelperLine.setWidth(2)

        self.rbHighlight = QgsRubberBand(self.canvas)
        self.rbHighlight.setColor(QColor(highlight_color))
        self.rbHighlight.setWidth(5)

        self.profile.setRubberband(self.rbHighlight)

        self.saveTool = None

    def setActive(self):
        """
        activates this map tool
        """
        self.saveTool = self.canvas.mapTool()
        self.canvas.setMapTool(self)

    def deactivate(self):
        """
        Called whenever this map tool is deactivated.
        Used to clean up code
        """
        QgepMapTool.deactivate(self)
        self.rubberBand.reset()
        self.rbHelperLine.reset()
        self.selectedPathPoints = []
        self.pathPolyline = []

    def findPath(self, start_point, end_point):
        """
        Tries to find the shortest path between pStart and pEnd.
        If it finds a path:
         * The path is visualized with a QgsRubberband
         * The profile plot is updated to represent the current path

        @param start_point: The id of the start point of the path
        @param end_point:   The id of the end point of the path
        """
        QApplication.setOverrideCursor(Qt.WaitCursor)
        # try:
        (vertices, edges) = self.networkAnalyzer.shortestPath(start_point, end_point)
        self.appendProfile(vertices, edges)
        #        except:
        #            pass
        QApplication.restoreOverrideCursor()
        if len(vertices) > 0:
            return True
        else:
            return False

    # pylint: disable=too-many-locals
    def appendProfile(self, vertices, edges):
        """
        Appends to the current profile

        @param vertices: A collection of vertices to append
        @param edges:    A collection of edges which connect the vertices
        """
        self.logger.debug('Append profile')
        self.logger.info(' * ' + repr(len(vertices)) + ' vertices')
        for v in vertices:
            self.logger.debug('   *' + repr(v))
        self.logger.info(' * ' + repr(len(edges)) + ' edges')
        for e in edges:
            self.logger.debug('   *' + repr(e))

        # Fetch all the needed edges in one batch
        edge_layer = self.networkAnalyzer.getReachLayer()
        edge_ids = [edge['feature'] for p1, p2, edge in edges]

        edge_features = self.networkAnalyzer.getFeaturesById(edge_layer, edge_ids)

        # We need some additional nodes, where we need to interpolate...
        interpolate_nodes_from = [edge_features.attrAsUnicode(feat, u'from_obj_id_interpolate')
                                  for feat in edge_features.asDict().values()]
        interpolate_nodes_to = [edge_features.attrAsUnicode(feat, u'to_obj_id_interpolate')
                                for feat in edge_features.asDict().values()]
        additional_ids = [self.networkAnalyzer.vertexIds[node] for node in interpolate_nodes_from]
        additional_ids += [self.networkAnalyzer.vertexIds[node] for node in interpolate_nodes_to]

        # Now, fetch the nodes we need
        node_layer = self.networkAnalyzer.getNodeLayer()
        node_ids = vertices + additional_ids
        node_features = self.networkAnalyzer.getFeaturesById(node_layer, node_ids)

        if len(vertices) > 1:
            self.rubberBand.reset()

            elem = QgepProfileNodeElement(vertices[0], node_features, 0)
            self.profile.addElement(vertices[0], elem)

            for p1, p2, edge in edges:
                from_offset = self.segmentOffset
                to_offset = self.segmentOffset + edge['weight']

                if 'reach' == edge['objType']:
                    if self.profile.hasElement(edge['baseFeature']):
                        self.profile[edge['baseFeature']] \
                            .addSegment(p1, p2, edge['feature'], node_features,
                                        edge_features, from_offset, to_offset)
                    else:
                        elem = QgepProfileReachElement(p1, p2, edge['feature'],
                                                       node_features, edge_features,
                                                       from_offset, to_offset)
                        self.profile.addElement(elem.objId, elem)

                elif 'special_structure' == edge['objType']:
                    if self.profile.hasElement(edge['baseFeature']):
                        self.profile[edge['baseFeature']] \
                            .addSegment(p1, p2, edge['feature'], node_features,
                                        edge_features, from_offset, to_offset)
                    else:
                        elem = QgepProfileSpecialStructureElement(p1, p2, edge['feature'],
                                                                  node_features, edge_features,
                                                                  from_offset, to_offset)
                        self.profile.addElement(elem.objId, elem)

                elem = QgepProfileNodeElement(p2, node_features, to_offset)
                self.profile.addElement(p2, elem)

                self.segmentOffset = to_offset

            self.profileChanged.emit(self.profile)

            # Create rubberband geometry
            for featId in edge_ids:
                self.pathPolyline.extend(edge_features[featId].geometry().asPolyline())

            self.rubberBand.addGeometry(QgsGeometry.fromPolyline(self.pathPolyline), node_layer)
            self.profileChanged.emit(self.profile)
            return True
        else:
            return False

    def canvasMoveEvent(self, event):
        """
        Mouse moved: update helper line

        @param event: The mouse event with coordinates and all
        """
        if len(self.selectedPathPoints) > 0:
            self.rbHelperLine.reset()
            for point in self.selectedPathPoints:
                self.rbHelperLine.addPoint(point[1])
            mouse_pos = self.canvas.getCoordinateTransform() \
                .toMapCoordinates(event.pos().x(), event.pos().y())
            self.rbHelperLine.addPoint(mouse_pos)

    def rightClicked(self, _):
        """
        Cancel any ongoing path selection

        @param event: The mouse event with coordinates and all
        """
        self.selectedPathPoints = []
        self.pathPolyline = []
        self.rbHelperLine.reset()
        self.profile.reset()
        self.segmentOffset = 0

    def leftClicked(self, event):
        """
        Select startpoint / intermediate point / endpoint

        @param event: The mouse event with coordinates and all
        """
        snapped_point = self.networkAnalyzer.snapPoint(event)

        if snapped_point is not None:
            if len(self.selectedPathPoints) > 0:
                pf = self.findPath(self.selectedPathPoints[-1][0], snapped_point.snappedAtGeometry)
                if pf:
                    self.selectedPathPoints.append(
                        (snapped_point.snappedAtGeometry, QgsPoint(snapped_point.snappedVertex)))
                else:
                    msg = self.msgBar.createMessage('No path found')
                    self.msgBar.pushWidget(msg, QgsMessageBar.WARNING)
            else:
                self.selectedPathPoints.append((snapped_point.snappedAtGeometry,
                                               QgsPoint(snapped_point.snappedVertex)))


class QgepTreeMapTool(QgepMapTool):
    """
    The map tool used to find TREES (upstream or downstream)
    """
    direction = "downstream"

    def __init__(self, canvas, button, network_analyzer):
        QgepMapTool.__init__(self, canvas, button)

        self.networkAnalyzer = network_analyzer
        self.saveTool = None

    def setDirection(self, direction):
        """
        Set the direction to track the graph.
        :param direction:  Can be 'upstream' or 'downstream'
        """
        self.direction = direction

    def getTree(self, point):
        """
        Does the work. Tracks the graph up- or downstream.
        :param point: The node from which the tracking should be started
        """
        QApplication.setOverrideCursor(Qt.WaitCursor)
        upstream = False
        if self.direction == "upstream":
            upstream = True

        self.rubberBand.reset()

        edges = self.networkAnalyzer.getTree(point, upstream)
        polylines = self.networkAnalyzer.getEdgeGeometry([edge[2]['feature'] for edge in edges])

        # Fix for QGIS < 2.0
        filtered_polylines = [pl for pl in polylines if len(pl) > 0]

        self.rubberBand.addGeometry(QgsGeometry.fromMultiPolyline(filtered_polylines),
                                    self.networkAnalyzer.getNodeLayer())

        QApplication.restoreOverrideCursor()

    def canvasMoveEvent(self, event):
        """
        Whenever the mouse is moved update the rubberband and the snapping.
        :param event: QMouseEvent with coordinates
        """
        point_clicked = QPoint(event.pos().x(), event.pos().y())
        (_, snapped_points) = self.networkAnalyzer.getSnapper().snapPoint(point_clicked, [])

        for marker in self.highLightedPoints:
            self.canvas.scene().removeItem(marker)

        self.highLightedPoints = []

        if len(snapped_points) > 0:
            for point in snapped_points:
                marker = QgsVertexMarker(self.canvas)
                marker.setCenter(point.snappedVertex)
                marker.setColor(QColor("#FFFF33"))
                marker.setIconSize(10)
                marker.setIconType(QgsVertexMarker.ICON_X)
                marker.setPenWidth(2)
                self.highLightedPoints.append(marker)

    def rightClicked(self, _):
        """
        Resets the rubberband on right clickl
        :param _: QMouseEvent
        """
        self.rubberBand.reset()

    def leftClicked(self, event):
        """
        Snaps to the network graph
        :param event: QMouseEvent
        """
        snapped_point = self.networkAnalyzer.snapPoint(event)

        if snapped_point is not None:
            self.getTree(snapped_point.snappedAtGeometry)

    def setActive(self):
        """
        Activates this map tool
        """
        self.saveTool = self.canvas.mapTool()
        self.canvas.setMapTool(self)

    def deactivate(self):
        """
        Deactivates this map tool. Removes the rubberband etc.
        """
        QgepMapTool.deactivate(self)
        self.rubberBand.reset()

        for marker in self.highLightedPoints:
            self.canvas.scene().removeItem(marker)

        self.highLightedPoints = []
