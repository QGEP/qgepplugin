# -*- coding: utf-8 -*-

"""
/***************************************************************************
 QGEP processing provider
                              -------------------
        begin                : 15.08.2018
        copyright            : (C) 2018 by OPENGIS.ch
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

from qgis.core import QgsProcessingAlgorithm, QgsProcessingFeatureBasedAlgorithm

from PyQt5.QtCore import QCoreApplication

__author__ = 'Matthias Kuhn'
__date__ = '2018-08-15'
__copyright__ = '(C) 2018 by OPENGIS.ch'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

class QgepAlgorithmMixin:
    """
    Boilerplate mixin for QGEP algorithms
    """

    def group(self):
        return 'QGEP'

    def groupId(self):
        return 'qgep'

    def tr(self, string, context=''):
        if context == '':
            context = self.__class__.__name__
        return QCoreApplication.translate(context, string)

    def createInstance(self):
        return type(self)()


class QgepAlgorithm(QgepAlgorithmMixin, QgsProcessingAlgorithm):
    pass


class QgepFeatureBasedAlgorithm(QgepAlgorithmMixin, QgsProcessingFeatureBasedAlgorithm):
    pass
