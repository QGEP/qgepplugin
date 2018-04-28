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

from qgis.core import QgsProcessingProvider
from .snap_reach import SnapReachAlgorithm

__author__ = 'Matthias Kuhn'
__date__ = '2017-11-18'
__copyright__ = '(C) 2017 by OPENGIS.ch'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'


class QgepProcessingProvider(QgsProcessingProvider):

    def __init__(self):
        QgsProcessingProvider.__init__(self)

        self.activate = True

        # Load algorithms
        self.alglist = [SnapReachAlgorithm()]
        for alg in self.alglist:
            alg.provider = self

    def getAlgs(self):
        algs = [SnapReachAlgorithm()]

        return algs

    def id(self):
        return 'qgep'

    def name(self):
        """This is the name that will appear on the toolbox group.

        It is also used to create the command line name of all the
        algorithms from this provider.
        """
        return 'QGEP'

    def icon(self):
        pass

    def svgIconPath(self):
        pass

    def loadAlgorithms(self):
        self.algs = self.getAlgs()
        for a in self.algs:
            self.addAlgorithm(a)
