# -*- coding: utf-8 -*-
# -----------------------------------------------------------
#
# Profile
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
# with this progsram; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# ---------------------------------------------------------------------

"""
Manages a graph of a wastewater network
"""

# pylint: disable=no-name-in-module
from collections import defaultdict
import time
import re

from PyQt4.QtCore import QPoint, QPyNullVariant
from PyQt4.QtGui import QMenu, QAction
from qgis.core import QgsTolerance, QgsSnapper, QgsGeometry
import networkx as nx


class QgepGraphManager(object):
    """
    Manages a graph
    """
    reachLayer = None
    reachLayerId = -1
    nodeLayer = None
    nodeLayerId = -1
    dirty = True
    graph = None
    vertexIds = {}
    nodesOnStructure = defaultdict(list)
    # Logs performance of graph creation
    timings = []

    def __init__(self, iface):
        self.iface = iface
        self.snapper = None

    def setReachLayer(self, reachLayer):
        """
        Set the reach layer (edges)
        """
        self.reachLayer = reachLayer
        self.dirty = True

        if reachLayer:
            self.reachLayerId = reachLayer.id()
        else:
            self.reachLayerId = 0

        if self.nodeLayer and self.reachLayer:
            self.createGraph()

    def setNodeLayer(self, nodeLayer):
        """
        Set the node layer
        """
        self.dirty = True

        self.nodeLayer = nodeLayer

        if nodeLayer:
            self.nodeLayerId = nodeLayer.id()

        else:
            self.nodeLayerId = 0

        if self.nodeLayer and self.reachLayer:
            self.createGraph()

    def _addVertices(self):
        """
        Initializes the graph with the vertices from the node layer
        """
        nodeProvider = self.nodeLayer.dataProvider()

        features = nodeProvider.getFeatures()

        # Add all vertices
        for feat in features:
            featId = feat.id()

            objId = feat['obj_id']
            objType = feat['type']

            vertex = feat.geometry().asPoint()
            self.graph.add_node(featId, dict(point=vertex, objType=objType))

            self.vertexIds[unicode(objId)] = featId

        self._profile("add vertices")

    def _addEdges(self):
        """
        Initializes the graph with the edges
        """
        # Add all edges (reach)
        reachProvider = self.reachLayer.dataProvider()

        features = reachProvider.getFeatures()

        # Loop through all reaches
        for feat in features:
            try:
                objId = feat['obj_id']
                objType = feat['type']
                fromObjId = feat['from_obj_id']
                toObjId = feat['to_obj_id']

                length = feat['length_calc']

                ptId1 = self.vertexIds[fromObjId]
                ptId2 = self.vertexIds[toObjId]

                props = { \
                    'weight': length, \
                    'feature': feat.id(), \
                    'baseFeature': objId, \
                    'objType': objType \
                    }
                self.graph.add_edge(ptId1, ptId2, props)
            except KeyError as e:
                print e

        self._profile("add edges")

    def _profile(self, name):
        """
        Adds a performance profile snapshot with the given name
        """
        spenttime = 0
        if len(self.timings) != 0:
            spenttime = time.clock() - self.timings[-1][1]
        self.timings.append((name, spenttime))

    # Creates a network graph
    def createGraph(self):
        """
        Create a graph
        """
        self._profile("create graph")
        # try:
        self.vertexIds = {}
        self.nodesOnStructure = defaultdict(list)
        self._profile("initiate dicts")
        self.graph = nx.DiGraph()

        self._profile("initiate graph")

        self._addVertices()
        self._addEdges()

        self.print_profile()
        self.dirty = False

    def getNodeLayer(self):
        """
        Getter for the node layer
        """
        return self.nodeLayer

    def getReachLayer(self):
        """
        Getter for the reach layer
        :return:
        """
        return self.reachLayer

    def getNodeLayerId(self):
        """
        Getter for the node layer's id
        """
        return self.nodeLayerId

    def getReachLayerId(self):
        """
        Getter for the reach layer's id
        """
        return self.reachLayerId

    def getSnapper(self):
        """
        Getter for the snapper
        """
        return self.snapper

    def snapPoint(self, event):
        """
        Snap to a point on this network
        :param event: A QMouseEvent
        """
        pClicked = QPoint(event.pos().x(), event.pos().y())

        self.snapper = QgsSnapper(self.iface.mapCanvas().mapRenderer())
        snapLayer = QgsSnapper.SnapLayer()
        snapLayer.mLayer = self.nodeLayer
        snapLayer.mTolerance = 10
        snapLayer.mUnitType = QgsTolerance.Pixels
        snapLayer.mSnapTo = QgsSnapper.SnapToVertex
        self.snapper.setSnapLayers([snapLayer])

        (_, snappedPoints) = self.snapper.snapPoint(pClicked, [])

        if len(snappedPoints) == 0:
            return None
        elif len(snappedPoints) == 1:
            return snappedPoints[0]
        elif len(snappedPoints) > 1:

            pointIds = [point.snappedAtGeometry for point in snappedPoints]
            nodeFeatures = self.getFeaturesById(self.getNodeLayer(), pointIds)

            # Filter wastewater nodes
            filteredFeatures = {id: nodeFeatures.featureById(id) for id in nodeFeatures.asDict() if
                                nodeFeatures.attrAsUnicode(nodeFeatures.featureById(id), u'type') == u'wastewater_node'}

            # Only one wastewater node left: return this
            if len(filteredFeatures) == 1:
                return \
                [point for point in snappedPoints if point.snappedAtGeometry == filteredFeatures.iterkeys().next()][0]

            # Still not sure which point to take?
            # Are there no wastewater nodes filtered? Let the user choose from the reach points
            if len(filteredFeatures) == 0:
                filteredFeatures = nodeFeatures.asDict()

            # Ask the user which point he wants to use
            actions = dict()

            menu = QMenu(self.iface.mapCanvas())

            for _, feature in filteredFeatures.iteritems():
                try:
                    title = feature.attribute('description') + " (" + feature.attribute('obj_id') + ")"
                except TypeError:
                    title = " (" + feature.attribute('obj_id') + ")"
                action = QAction(title, menu)
                actions[action] = point
                menu.addAction(action)

            clickedAction = menu.exec_(self.iface.mapCanvas().mapToGlobal(event.pos()))

            if clickedAction is not None:
                return actions[clickedAction]

            return None

    def shortestPath(self, pStart, pEnd):
        """
        Finds the shortes path from the start point
        to the end point
        :param pStart: The start node
        :param pEnd:   The end node
        :return:       A (path, edges) tuple
        """
        if self.dirty:
            self.createGraph()

        try:
            path = nx.algorithms.dijkstra_path(self.graph, pStart, pEnd)
            edges = [(u, v, self.graph[u][v]) for (u, v) in zip(path[0:], path[1:])]

            p = (path, edges)

        except nx.NetworkXNoPath:
            print "no path found"
            p = ([], [])

        return p

    def getTree(self, node, reverse=False):
        """
        Get
        :param node:    A start node
        :param reverse: Should the graph be reversed (upstream search)
        :return:        A list of edges
        """
        if self.dirty:
            self.createGraph()

        if reverse:
            myGraph = self.graph.reverse()
        else:
            myGraph = self.graph

        # Returns pred, weight
        pred, _ = nx.bellman_ford(myGraph, node)
        edges = [(v, u, myGraph[v][u]) for (u, v) in pred.items() if v is not None]

        return edges

    def getEdgeGeometry(self, edges):
        """
        Get the geometry for some edges
        :param edges:  A list of edges
        :return:       A list of polylines
        """
        cache = self.getFeaturesById(self.reachLayer, edges)
        polylines = [feat.geometry().asPolyline() for feat in cache.asDict().values()]
        return polylines

    # pylint: disable=no-self-use
    def getFeaturesById(self, layer, ids):
        """
        Get some features by their id
        """
        featCache = QgepFeatureCache(layer)
        dataProvider = layer.dataProvider()

        features = dataProvider.getFeatures()

        for feat in features:
            if feat.id() in ids:
                featCache.addFeature(feat)

        return featCache

    # pylint: disable=no-self-use
    def getFeaturesByAttr(self, layer, attr, values):
        """
        Get some features by an attribute value
        """
        featCache = QgepFeatureCache(layer)
        dataProvider = layer.dataProvider()

        # Batch query and filter locally
        features = dataProvider.getFeatures()

        for feat in features:
            if featCache.attrAsUnicode(feat, attr) in values:
                featCache.addFeature(feat)

        return featCache

    def print_profile(self):
        """
        Will print some performance profiling information
        """
        for (name, spenttime) in self.timings:
            print name + ":" + str(spenttime)

class QgepFeatureCache(object):
    """
    A feature cache.
    The DB can be slow sometimes, so if we know, that we'll be using some features
    several times consecutively it's better to keep it in memory.
    There is no check done for maximum size. You have to care for your memory
    yourself, when using this class!
    """
    _featuresById = None
    _featuresByObjId = None
    objIdField = None
    layer = None

    def __init__(self, layer, objIdField='obj_id'):
        self._featuresById = {}
        self._featuresByObjId = {}
        self.objIdField = objIdField
        self.layer = layer

    def __getitem__(self, key):
        return self.featureById(key)

    def addFeature(self, feat):
        """
        Add a feature to the cache
        """
        self._featuresById[feat.id()] = feat
        self._featuresByObjId[self.attrAsUnicode(feat, self.objIdField)] = feat

    def featureById(self, featId):
        """
        Get a feature by its feature id
        """
        return self._featuresById[featId]

    def featureByObjId(self, objId):
        """
        Get a feature by its object id
        """
        return self._featuresByObjId[objId]

    def attrAsFloat(self, feat, attr):
        """
        Get an attribute as float
        """
        try:
            return float(self.attr(feat, attr))
        except TypeError:
            return None

    def attrAsUnicode(self, feat, attr):
        """
        Get an attribute as unicode string
        """
        return self.attr(feat, attr)

    # pylint: disable=no-self-use
    def attr(self, feat, attr):
        """
        Get an attribute
        """
        try:
            if isinstance(feat[attr], QPyNullVariant):
                return None
            else:
                return feat[attr]
        except KeyError:
            return None

    def attrAsGeometry(self, feat, attr):
        """
        Get an attribute as geometry
        """
        ewktString = self.attrAsUnicode(feat, attr)
        # Strip SRID=21781; token, TODO: Fix this upstream
        m = re.search('(.*;)?(.*)', ewktString)
        return QgsGeometry.fromWkt(m.group(2))

    def asDict(self):
        """
        Returns all features a s a dictionary with ids as keys
        """
        return self._featuresById

    def asObjIdDict(self):
        """
        Returns all features as a dictionary with object ids as keys.
        """
        return self._featuresById
