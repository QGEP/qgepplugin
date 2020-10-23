"""
This is an algorithm to be used from the QGIS processing toolbox to
update multiple attributes of the catchment_area table in a QGEP
datamodel from planned to current.

Please refer to Gruner Boeringer about the exact logic, as he is the
author of the initial SQL query below that served as a base.
Original work : https://gist.github.com/m-kuhn/713a4f05d78182daf9432e159c79d1d5

All configuration is done in the CONFIG object :
- COPY means copy the value from planned to current
- dictionnaries allows to convert values
"""

from .qgep_algorithm import QgepFeatureBasedAlgorithm

CONFIG = {
    "drainage_system": {
        5186: 5191,
        5187: 5192,
        5188: 5193,
        5189: 5195,
        5185: 5194,
        5537: 5536,
        None: None,
    },
    "direct_discharge": {
        5457: 5459,
        5458: 5460,
        5463: 5464,
        None: None,
    },
    "infiltration": {
        5452: 5461,
        5453: 5462,
        5165: 5170,
        None: None,
    },
    "retention": {
        5467: 5470,
        5468: 5471,
        5169: 5472,
        None: None,
    },
    "discharge_coefficient_rw": "COPY",
    "discharge_coefficient_ww": "COPY",
    "population_density": "COPY",
    "runoff_limit": "COPY",
    "seal_factor_rw": "COPY",
    "seal_factor_ww": "COPY",
    "sewer_infiltration_water_production": "COPY",
    "waste_water_production": "COPY",
    "fk_wastewater_networkelement_rw": "COPY",
    "fk_wastewater_networkelement_ww": "COPY",
}


class PlannedToCurrentCatchmentAlgorithm(QgepFeatureBasedAlgorithm):

    def name(self):
        return "planned_to_current_catchment"

    def displayName(self):
        return "Planned to Current (Catchment Area)"

    def shortHelpString(self):
        return "Change catchment areas to have planned=current, according to some hard-coded update rules.\n\nSelect the 'catchment areas' layer, toggle edit mode, then run this algorithm in place.\n\nThe functionality was adapted from SQL developed by Gruner Boeringer found here : https://gist.github.com/m-kuhn/713a4f05d78182daf9432e159c79d1d5"

    def outputName(self):
        return 'OUTPUT'

    def processFeature(self, feature, context, feedback):

        updated = False
        for key, conversion in CONFIG.items():

            current_key = key + "_current"
            planned_key = key + "_planned"

            try:
                planned_value = feature[planned_key]
            except KeyError:
                feedback.reportError(f"Feature {feature.id()} / {key} : attribute not found !")
                continue

            if conversion == "COPY":
                current_value = planned_value
            else:
                try:
                    current_value = conversion[planned_value]
                except KeyError:
                    # feedback.reportError(f"Feature {feature.id()} / {key} : no conversion defined for value {planned_value}")
                    continue

            if feature[current_key] != current_value:
                feature[current_key] = current_value
                updated = True

        if updated:
            feedback.pushInfo(f"Updated feature {feature.id()}")

        return [feature]
