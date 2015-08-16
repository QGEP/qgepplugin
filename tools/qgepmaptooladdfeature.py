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

from qgis.gui import (
    QgsMapTool,
    QgsRubberBand,
    QgsMessageBar
)
from qgis.core import (
    QgsFeature,
    QgsPoint,
    QgsSnapper,
    QgsTolerance,
    QgsFeatureRequest,
    QGis,
    QgsGeometry
)
from PyQt4.QtGui import (
    QCursor,
    QColor,
    QApplication,
    QDialog,
    QGridLayout,
    QLabel,
    QLineEdit,
    QDialogButtonBox
)
from PyQt4.QtCore import (
    Qt,
    pyqtSignal
)
from qgepplugin.utils.qgeplayermanager import QgepLayerManager
import math


class QgepMapToolAddFeature(QgsMapTool):
    """
    Base class for adding features
    """
    def __init__(self, iface, layer):
        QgsMapTool.__init__(self, iface.mapCanvas())
        self.iface = iface
        self.canvas = iface.mapCanvas()
        self.layer = layer
        self.rubberband = QgsRubberBand(iface.mapCanvas(), layer.geometryType())
        self.rubberband.setColor(QColor("#ee5555"))
        self.rubberband.setWidth(2)
        self.tempRubberband = QgsRubberBand(iface.mapCanvas(), layer.geometryType())
        self.tempRubberband.setColor(QColor("#ee5555"))
        self.tempRubberband.setWidth(2)
        self.tempRubberband.setLineStyle(Qt.DotLine)

    def activate(self):
        """
        When activating the map tool
        """
        QgsMapTool.activate(self)
        self.canvas.setCursor(QCursor(Qt.CrossCursor))

    def deactivate(self):
        """
        On deactivating the map tool
        """
        QgsMapTool.deactivate(self)
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

    def canvasReleaseEvent(self, event):
        """
        Called when a mouse button is
        :param event:
        :return:
        """
        if event.button() == Qt.RightButton:
            self.rightClicked(event)
        else:
            self.leftClicked(event)

    def leftClicked(self, event):
        """
        When the canvas is left clicked we add a new point to the rubberband.
        :type event: QMouseEvent
        """
        mousepos = self.canvas.getCoordinateTransform()\
            .toMapCoordinates(event.pos().x(), event.pos().y())
        self.rubberband.addPoint(mousepos)
        self.tempRubberband.reset()

    def rightClicked(self, _):
        """
        On a right click we create a new feature from the existing rubberband and show the add
        dialog
        """
        f = QgsFeature(self.layer.pendingFields())
        f.setGeometry(self.rubberband.asGeometry())
        dlg = self.iface.getFeatureForm(self.layer, f)
        dlg.setIsAddDialog(True)
        dlg.exec_()
        self.rubberband.reset()
        self.tempRubberband.reset()

    def canvasMoveEvent(self, event):
        """
        When the mouse is moved the rubberband needs to be updated
        :param event: The coordinates etc.
        """
        mousepos = self.canvas.getCoordinateTransform()\
            .toMapCoordinates(event.pos().x(), event.pos().y())
        self.tempRubberband.movePoint(mousepos)


class QgepMapToolAddReach(QgepMapToolAddFeature):
    """
    Create a new reach with the mouse.
    Will snap to wastewater nodes for the first and last point and auto-connect
    these.
    """
    currentSnappingResult = None
    firstSnappingResult = None
    lastSnappingResult = None

    def __init__(self, iface, layer):
        QgepMapToolAddFeature.__init__(self, iface, layer)
        self.nodeLayer = QgepLayerManager.layer('vw_wastewater_node')
        assert self.nodeLayer
        self.reachLayer = QgepLayerManager.layer('vw_qgep_reach')
        assert self.reachLayer

    def canvasMoveEvent(self, event):
        """
        When the mouse is moved the rubberband needs to be updated
        :param event: The coordinates etc.
        """
        mousepos = self.canvas.getCoordinateTransform()\
            .toMapCoordinates(event.pos().x(), event.pos().y())
        self.tempRubberband.movePoint(mousepos)

    def leftClicked(self, event):
        """
        The mouse is clicked: snap to neary points which are on the wastewater node layer
        and update the rubberband
        :param event: The coordinates etc.
        """
        self.snap(event.pos())
        if self.rubberband.numberOfVertices() == 0:
            self.firstSnappingResult = self.currentSnappingResult
        self.lastSnappingResult = self.currentSnappingResult
        if self.currentSnappingResult:
            pt = self.currentSnappingResult.snappedVertex
        else:
            pt = self.canvas.getCoordinateTransform()\
                .toMapCoordinates(event.pos().x(), event.pos().y())
        self.rubberband.addPoint(pt)
        self.tempRubberband.reset()
        self.tempRubberband.addPoint(pt)

    def snap(self, pos):
        """
        Snap to nearby points on the wastewater node layer which may be used as connection
        points for this reach.
        :param pos: The position to snap
        :return: The snapped position
        """
        snapper = QgsSnapper(self.iface.mapCanvas().mapSettings())
        snap_nodelayer = QgsSnapper.SnapLayer()
        snap_nodelayer.mLayer = self.nodeLayer
        snap_nodelayer.mTolerance = 10
        snap_nodelayer.mUnitType = QgsTolerance.Pixels
        snap_nodelayer.mSnapTo = QgsSnapper.SnapToVertex
        snapper.setSnapLayers([snap_nodelayer])
        (_, snappedPoints) = snapper.snapPoint(pos)
        if snappedPoints:
            self.currentSnappingResult = snappedPoints[0]
            return self.currentSnappingResult.snappedVertex
        else:
            snapper = QgsSnapper(self.iface.mapCanvas().mapSettings())
            snap_reachlayer = QgsSnapper.SnapLayer()
            snap_reachlayer.mLayer = self.reachLayer
            snap_reachlayer.mTolerance = 10
            snap_reachlayer.mUnitType = QgsTolerance.Pixels
            snap_reachlayer.mSnapTo = QgsSnapper.SnapToVertexAndSegment
            snapper.setSnapLayers([snap_reachlayer])
            (_, snappedPoints) = snapper.snapPoint(pos)
            if snappedPoints:
                self.currentSnappingResult = snappedPoints[0]
                return self.currentSnappingResult.snappedVertex
            else:
                self.currentSnappingResult = None
                return pos

    def rightClicked(self, _):
        """
        The party is over, the reach digitized. Create a feature from the rubberband and
        show the feature form.
        """
        self.tempRubberband.reset()

        f = QgsFeature(self.layer.pendingFields())
        f.setGeometry(self.rubberband.asGeometry())

        if self.firstSnappingResult is not None:
            req = QgsFeatureRequest(self.firstSnappingResult.snappedAtGeometry)
            from_networkelement = self.firstSnappingResult.layer.getFeatures(req).next()
            from_field = self.layer.pendingFields()\
                .indexFromName('rp_from_fk_wastewater_networkelement')
            f.setAttribute(from_field, from_networkelement.attribute('obj_id'))

        if self.lastSnappingResult is not None:
            req = QgsFeatureRequest(self.lastSnappingResult.snappedAtGeometry)
            to_networkelement = self.lastSnappingResult.layer.getFeatures(req).next()
            to_field = self.layer.pendingFields().indexFromName('rp_to_fk_wastewater_networkelement')
            f.setAttribute(to_field, to_networkelement.attribute('obj_id'))

        dlg = self.iface.getFeatureForm(self.layer, f)
        dlg.setIsAddDialog(True)
        dlg.exec_()
        self.rubberband.reset()


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
        self.rubberband = QgsRubberBand(iface.mapCanvas(), QGis.Line)
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
        mousepos = self.canvas.getCoordinateTransform()\
            .toMapCoordinates(event.pos().x(), event.pos().y())
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

                pt1 = QgsPoint(lp1.x() + width * (yd / length), lp1.y() - width * (xd / length))
                pt2 = QgsPoint(lp1.x() - width * (yd / length), lp1.y() + width * (xd / length))
                pt3 = QgsPoint(lp2.x() - width * (yd / length), lp2.y() + width * (xd / length))
                pt4 = QgsPoint(lp2.x() + width * (yd / length), lp2.y() - width * (xd / length))

                self.geometry = QgsGeometry.fromPolygon([[pt1, pt2, pt3, pt4, pt1]])

                self.geometryDigitized.emit()

            self.firstPoint = mousepos
