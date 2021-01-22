from .qgep import Classes as QGEP
from .abwasser import Classes as ABWASSER

QGEP_TO_ABWASSER = {
    # ALREADY MAPPED
    QGEP.organisation: [ABWASSER.organisation, ABWASSER.metaattribute],
    QGEP.channel: [ABWASSER.kanal],
    QGEP.manhole: [ABWASSER.normschacht],
    QGEP.discharge_point: [ABWASSER.einleitstelle],
    QGEP.special_structure: [ABWASSER.spezialbauwerk],
    QGEP.infiltration_installation: [ABWASSER.versickerungsanlage],
    QGEP.pipe_profile: [ABWASSER.rohrprofil],
    QGEP.reach_point: [ABWASSER.haltungspunkt],
    QGEP.wastewater_node: [ABWASSER.abwasserknoten],
    QGEP.reach: [ABWASSER.haltung],
    QGEP.dryweather_downspout: [ABWASSER.trockenwetterfallrohr],
    QGEP.access_aid: [ABWASSER.einstiegshilfe],
    QGEP.dryweather_flume: [ABWASSER.trockenwetterrinne],
    QGEP.cover: [ABWASSER.deckel],
    QGEP.benching: [ABWASSER.bankett],
    # AVAILABLE TABLES
    # todo...
    # NOT YET MAPPED
}