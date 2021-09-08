# -*- coding: utf-8 -*-

"""
/***************************************************************************
 QGEP-swmm processing provider
                              -------------------
        begin                : 07.2019
        copyright            : (C) 2019 by ig-group.ch
        email                : timothee.produit@ig-group.ch
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


import datetime

from qgis.core import (
    QgsProcessingContext,
    QgsProcessingFeedback,
    QgsProcessingParameterEnum,
    QgsProcessingParameterFile,
    QgsProcessingParameterFileDestination,
    QgsProcessingParameterString,
)

from .qgep_algorithm import QgepAlgorithm
from .QgepSwmm import QgepSwmm

__author__ = "Timothée Produit"
__date__ = "2019-08-01"
__copyright__ = "(C) 2019 by IG-Group.ch"

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = "$Format:%H$"


class SwmmCreateInputAlgorithm(QgepAlgorithm):
    """"""

    DATABASE = "DATABASE"
    TEMPLATE_INP_FILE = "TEMPLATE_INP_FILE"
    INP_FILE = "INP_FILE"
    STATE = "STATE"

    def name(self):
        return "swmm_create_input"

    def displayName(self):
        return self.tr("SWMM Create Input")

    def initAlgorithm(self, config=None):
        """Here we define the inputs and output of the algorithm, along
        with some other properties.
        """
        self.stateOptions = ["current", "planned"]
        # The parameters
        description = self.tr("Database")
        self.addParameter(
            QgsProcessingParameterString(
                self.DATABASE, description=description, defaultValue="pg_qgep_demo_data"
            )
        )

        description = self.tr("State (current or planned)")
        self.addParameter(
            QgsProcessingParameterEnum(
                self.STATE,
                description=description,
                options=self.stateOptions,
                defaultValue=self.stateOptions[0],
            )
        )

        description = self.tr("Template INP File")
        self.addParameter(
            QgsProcessingParameterFile(
                self.TEMPLATE_INP_FILE, description=description, extension="inp"
            )
        )

        description = self.tr("Destination INP File")
        self.addParameter(
            QgsProcessingParameterFileDestination(
                self.INP_FILE, description=description, fileFilter="inp (*.inp)"
            )
        )

    def processAlgorithm(
        self, parameters, context: QgsProcessingContext, feedback: QgsProcessingFeedback
    ):
        """Here is where the processing itself takes place."""

        feedback.setProgress(0)

        # init params
        database = self.parameterAsString(parameters, self.DATABASE, context)
        state = self.parameterAsString(parameters, self.STATE, context)
        template_inp_file = self.parameterAsFile(
            parameters, self.TEMPLATE_INP_FILE, context
        )
        inp_file = self.parameterAsFileOutput(parameters, self.INP_FILE, context)
        state = self.stateOptions[int(state)]
        if state not in ["current", "planned"]:
            feedback.reportError(
                'State must be "planned" or "current", state was set to "current"'
            )
            state = "current"
        # Connect to QGEP database and perform translation
        with QgepSwmm(
          datetime.datetime.today().isoformat(), 
          database, 
          state,
          inp_file, 
          template_inp_file, 
          None, 
          None, 
          feedback
        ) as qs:
            qs.write_input()
        feedback.setProgress(100)

        return {self.INP_FILE: inp_file}