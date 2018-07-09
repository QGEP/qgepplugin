# -*- coding: utf-8 -*-
# -----------------------------------------------------------
#
# Qgep
# Copyright (C) 2014  Matthias Kuhn
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
Some map tools for digitizing features
"""

from builtins import next
from builtins import range
from qgis.gui import (
    QgsMapToolAdvancedDigitizing,
    QgsMapTool,
    QgsRubberBand,
    QgsMessageBar,
    QgsMapCanvasSnappingUtils,
    QgsVertexMarker
)
from qgis.core import (
    QgsSnappingConfig,
    QgsPoint,
    QgsPointXY,
    QgsFeature,
    QgsTolerance,
    QgsFeatureRequest,
    QgsGeometry,
    QgsWkbTypes,
    NULL
)
from qgis.PyQt.QtGui import QCursor, QColor
from qgis.PyQt.QtWidgets import QApplication, QDialog, QGridLayout, QLabel, QLineEdit, QDialogButtonBox
from qgis.PyQt.QtCore import Qt, pyqtSignal
from ..utils.qgeplayermanager import QgepLayerManager
import math
import sip


class QgepRubberBand3D(QgsRubberBand):
    def __init__(self, map_canvas, geometry_type):
        QgsRubberBand.__init__(self, map_canvas, geometry_type)
        self.points = []

    def addPoint3D(self, point):
        assert type(point) == QgsPoint
        QgsRubberBand.addPoint(self, QgsPointXY(point.x(), point.y()))
        self.points.append(QgsPoint(point))

    def reset3D(self):
        QgsRubberBand.reset(self)
        self.points = []

    def asGeometry3D(self):
        wkt = 'LineStringZ('\
              + ', '.join(['{} {} {}'.format(p.x(), p.y(), p.z()) for p in self.points])\
              + ')'
        return QgsGeometry.fromWkt(wkt)


class QgepMapToolAddFeature(QgsMapToolAdvancedDigitizing):
    """
    Base class for adding features
    """
    def __init__(self, iface, layer):
        QgsMapToolAdvancedDigitizing.__init__(self, iface.mapCanvas(), iface.cadDockWidget())
        self.iface = iface
        self.canvas = iface.mapCanvas()
        self.layer = layer
        self.rubberband = QgepRubberBand3D(iface.mapCanvas(), layer.geometryType())
        self.rubberband.setColor(QColor("#ee5555"))
        self.rubberband.setWidth(1)
        self.temp_rubberband = QgsRubberBand(iface.mapCanvas(), layer.geometryType())
        self.temp_rubberband.setColor(QColor("#ee5555"))
        self.temp_rubberband.setWidth(1)
        self.temp_rubberband.setLineStyle(Qt.DotLine)

    def activate(self):
        """
        When activating the map tool
        """
        QgsMapToolAdvancedDigitizing.activate(self)
        self.canvas.setCursor(QCursor(Qt.CrossCursor))

    def deactivate(self):
        """
        On deactivating the map tool
        """
        QgsMapToolAdvancedDigitizing.deactivate(self)
        self.canvas.unsetCursor()

    # pylint: disable=no-self-use
    def isZoomTool(self):
        """
        This is no zoom tool
        """
        return False

    # ===========================================================================
    # Events
    # ===========================================================================

    def cadCanvasReleaseEvent(self, event):
        """
        Called when a mouse button is
        :param event:
        :return:
        """
        if event.button() == Qt.RightButton:
            self.right_clicked(event)
        else:
            self.left_clicked(event)

    def left_clicked(self, event):
        """
        When the canvas is left clicked we add a new point to the rubberband.
        :type event: QMouseEvent
        """
        mousepos = self.canvas.getCoordinateTransform()\
            .toMapCoordinates(event.pos().x(), event.pos().y())
        self.rubberband.addPoint(mousepos)
        self.temp_rubberband.reset()

    def right_clicked(self, _):
        """
        On a right click we create a new feature from the existing rubberband and show the add
        dialog
        """
        f = QgsFeature(self.layer.pendingFields())
        f.setGeometry(self.rubberband.asGeometry())
        dlg = self.iface.getFeatureForm(self.layer, f)
        dlg.setIsAddDialog(True)
        dlg.exec_()
        self.rubberband.reset3D()
        self.temp_rubberband.reset()

    def cadCanvasMoveEvent(self, event):
        """
        When the mouse is moved the rubberband needs to be updated
        :param event: The coordinates etc.
        """

        # When a generated event arrives it's a QMoveEvent... No idea why, but this prevents from an exception
        try:
            QgsMapToolAdvancedDigitizing.cadCanvasMoveEvent(self, event)
            mousepos = event.mapPoint()
            self.temp_rubberband.movePoint(mousepos)
            self.mouse_move(event)

        except TypeError:
            pass

    def mouse_move(self, event):
        pass


class QgepMapToolAddReach(QgepMapToolAddFeature):
    """
    Create a new reach with the mouse.
    Will snap to wastewater nodes for the first and last point and auto-connect
    these.
    """
    first_snapping_match = None
    last_snapping_match = None

    def __init__(self, iface, layer):
        QgepMapToolAddFeature.__init__(self, iface, layer)
        self.snapping_marker = None
        self.node_layer = QgepLayerManager.layer('vw_wastewater_node')
        assert self.node_layer
        self.reach_layer = QgepLayerManager.layer('vw_qgep_reach')
        assert self.reach_layer
        self.setMode(QgsMapToolAdvancedDigitizing.CaptureLine)

        layer_snapping_configs = [{'layer': self.node_layer, 'mode': QgsSnappingConfig.SnapToVertex},
                                  {'layer': self.reach_layer, 'mode': QgsSnappingConfig.SnapToVertexAndSegment}]
        self.snapping_configs = []
        self.snapping_utils = QgsMapCanvasSnappingUtils(self.iface.mapCanvas())

        for lsc in layer_snapping_configs:
            config = QgsSnappingConfig()
            config.setMode(QgsSnappingConfig.AdvancedConfiguration)
            config.setEnabled(True)
            settings = QgsSnappingConfig.IndividualLayerSettings(True, lsc['mode'],
                                                                 10, QgsTolerance.Pixels)
            config.setIndividualLayerSettings(lsc['layer'], settings)
            self.snapping_configs.append(config)

    def left_clicked(self, event):
        """
        The mouse is clicked: snap to neary points which are on the wastewater node layer
        and update the rubberband
        :param event: The coordinates etc.
        """
        point3d, match = self.snap(event)
        if self.rubberband.numberOfVertices() == 0:
            self.first_snapping_match = match
        self.last_snapping_match = match
        self.rubberband.addPoint3D(point3d)
        self.temp_rubberband.reset()
        self.temp_rubberband.addPoint(QgsPointXY(point3d.x(), point3d.y()))

        if self.snapping_marker is not None:
            sip.delete(self.snapping_marker)
            self.snapping_marker = None

    def mouse_move(self, event):
        _, match = self.snap(event)
        # snap indicator
        if not match.isValid():
            if self.snapping_marker is not None:
                sip.delete(self.snapping_marker)
                self.snapping_marker = None
            return

        # TODO QGIS 3: see if vertices can be removed

        # we have a valid match
        if self.snapping_marker is None:
            self.snapping_marker = QgsVertexMarker(self.iface.mapCanvas())
            self.snapping_marker.setPenWidth(3)
            self.snapping_marker.setColor(QColor(Qt.magenta))

        if match.hasVertex():
            if match.layer():
                icon_type = QgsVertexMarker.ICON_BOX  # vertex snap
            else:
                icon_type = QgsVertexMarker.ICON_X  # intersection snap
        else:
            icon_type = QgsVertexMarker.ICON_DOUBLE_TRIANGLE  # must be segment snap
        self.snapping_marker.setIconType(icon_type)
        self.snapping_marker.setCenter(match.point())

    def snap(self, event):
        """
        Snap to nearby points on the wastewater node layer which may be used as connection
        points for this reach.
        :param event: The mouse event
        :return: The snapped position in map coordinates
        """

        for config in self.snapping_configs:
            self.snapping_utils.setConfig(config)
            match = self.snapping_utils.snapToMap(QgsPointXY(event.originalMapPoint()))
            if match.isValid():
                return QgsPoint(match.point()), match

        # if no match, snap to all layers (according to map settings) and try to grab Z
        match = self.iface.mapCanvas().snappingUtils().snapToMap(QgsPointXY(event.originalMapPoint()))
        if match.isValid() and match.hasVertex():
            if match.layer():
                req = QgsFeatureRequest(match.featureId())
                f = next(match.layer().getFeatures(req))
                assert f.isValid()
                if match.layer().wkbType() == QgsWkbTypes.WKBPoint25D:
                    point = QgsPoint(f.geometry().geometry())
                else:
                    (ok, vertex_id) = f.geometry().vertexIdFromVertexNr(match.vertexIndex())
                    assert ok
                    point = f.geometry().geometry().vertexAt(vertex_id)
                assert type(point) == QgsPoint
                return point, match
            else:
                return QgsPoint(match.point()), match

        return QgsPoint(event.originalMapPoint()), match

    def right_clicked(self, _):
        """
        The party is over, the reach digitized. Create a feature from the rubberband and
        show the feature form.
        """
        self.temp_rubberband.reset()

        if self.snapping_marker is not None:
            sip.delete(self.snapping_marker)
            self.snapping_marker = None

        if len(self.rubberband.points) >= 2:

            fields = self.layer.fields()
            f = QgsFeature(fields)
            for idx in range(len(fields)):
                # try client side default value first
                v = self.layer.defaultValue(idx, f)
                if v != NULL:
                    f.setAttribute(idx, v)
                else:
                    f.setAttribute(idx, self.layer.dataProvider().defaultValue(idx))

            f.setGeometry(self.rubberband.asGeometry3D())

            snapping_results = {'from': self.first_snapping_match,
                                'to': self.last_snapping_match}
            for dest, match in list(snapping_results.items()):
                level_field_index = self.layer.pendingFields().indexFromName('rp_{dest}_level'.format(dest=dest))
                pt_idx = 0 if dest == 'from' else -1
                if match.isValid() and match.layer() in (self.node_layer, self.reach_layer):
                    request = QgsFeatureRequest(match.featureId())
                    network_element = next(match.layer().getFeatures(request))
                    assert network_element.isValid()
                    # set the related network element
                    field = self.layer.pendingFields().indexFromName('rp_{dest}_fk_wastewater_networkelement'.format(dest=dest))
                    f.setAttribute(field, network_element.attribute('obj_id'))
                    # assign level if the match is a node or if we have 3D from snapping
                    if match.layer() == self.node_layer:
                        level = network_element['bottom_level']
                        f.setAttribute(level_field_index, level)
                elif self.rubberband.points[pt_idx].z() != 0:
                    f.setAttribute(level_field_index, self.rubberband.points[pt_idx].z())

            dlg = self.iface.getFeatureForm(self.layer, f)
            dlg.setIsAddDialog(True)
            dlg.exec_()

        self.rubberband.reset3D()


class QgepMapToolDigitizeDrainageChannel(QgsMapTool):
    '''
    This is used to digitize a drainage channel.

    It lets you digitize two points and then creates a polygon based on these two points
    by adding an orthogonal offset at each side.

    Input:

       x==============x

    Output:

       ----------------
       |              |
       ----------------

    Usage:
      Connect to the signals deactivated() and geometryDigitized()
      If geometryDigitized() is called you can use the member variable geometry
      which will contain a rectangle polygon
      deactivated() will be emited after a right click
    '''

    geometryDigitized = pyqtSignal()

    def __init__(self, iface, layer):
        QgsMapTool.__init__(self, iface.mapCanvas())
        self.iface = iface
        self.canvas = iface.mapCanvas()
        self.layer = layer
        self.rubberband = QgsRubberBand(iface.mapCanvas(), QgsWkbTypes.LineGeometry)
        self.rubberband.setColor(QColor("#ee5555"))
        self.rubberband.setWidth(2)
        self.firstPoint = None
        self.messageBarItem = None
        self.geometry = None

    def activate(self):
        """
        Map tool is activated
        """
        QgsMapTool.activate(self)
        self.canvas.setCursor(QCursor(Qt.CrossCursor))
        msgtitle = self.tr('Digitizing Drainage Channel')
        msg = self.tr('Digitize start and end point. Rightclick to abort.')
        self.messageBarItem = QgsMessageBar.createMessage(msgtitle,
                                                          msg)
        self.iface.messageBar().pushItem(self.messageBarItem)

    def deactivate(self):
        """
        Map tool is deactivated
        """
        QgsMapTool.deactivate(self)
        self.iface.messageBar().popWidget(self.messageBarItem)
        try:
            self.iface.mapCanvas().scene().removeItem(self.rubberband)
            del self.rubberband
        except AttributeError:
            # Called repeatedly... bail out
            pass
        self.canvas.unsetCursor()

    def canvasMoveEvent(self, event):
        """
        Mouse is moved: Update rubberband
        :param event: coordinates etc.
        """
        mousepos = event.mapPoint()
        self.rubberband.movePoint(mousepos)

    def canvasReleaseEvent(self, event):
        """
        Canvas is released. This means:
          * start digitizing
          * stop digitizing (create a rectangle
            * if the Ctrl-modifier is pressed, ask for the rectangle width
        :param event: coordinates etc.
        """
        if event.button() == Qt.RightButton:
            self.deactivate()
        else:
            mousepos = self.canvas.getCoordinateTransform()\
                .toMapCoordinates(event.pos().x(), event.pos().y())
            self.rubberband.addPoint(mousepos)
            if self.firstPoint:  # If the first point was set before, we are doing the second one
                lp1 = self.rubberband.asGeometry().asPolyline()[0]
                lp2 = self.rubberband.asGeometry().asPolyline()[1]
                width = 0.2
                if QApplication.keyboardModifiers() & Qt.ControlModifier:
                    dlg = QDialog()
                    dlg.setLayout(QGridLayout())
                    dlg.layout().addWidget(QLabel(self.tr('Enter width')))
                    txt = QLineEdit('0.2')
                    dlg.layout().addWidget(txt)
                    bb = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
                    dlg.layout().addWidget(bb)
                    bb.accepted.connect(dlg.accept)
                    bb.rejected.connect(dlg.reject)
                    if dlg.exec_():
                        try:
                            width = float(txt.text())
                        except ValueError:
                            width = 0.2

                length = math.sqrt(math.pow(lp1.x() - lp2.x(), 2) + math.pow(lp1.y() - lp2.y(), 2))
                xd = lp2.x() - lp1.x()
                yd = lp2.y() - lp1.y()

                pt1 = QgsPointXY(lp1.x() + width * (yd / length), lp1.y() - width * (xd / length))
                pt2 = QgsPointXY(lp1.x() - width * (yd / length), lp1.y() + width * (xd / length))
                pt3 = QgsPointXY(lp2.x() - width * (yd / length), lp2.y() + width * (xd / length))
                pt4 = QgsPointXY(lp2.x() + width * (yd / length), lp2.y() - width * (xd / length))

                self.geometry = QgsGeometry.fromPolygon([[pt1, pt2, pt3, pt4, pt1]])

                self.geometryDigitized.emit()

            self.firstPoint = mousepos
