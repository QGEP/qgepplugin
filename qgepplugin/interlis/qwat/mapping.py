
from .model_qwat import get_qwat_model
from .model_wasser import get_wasser_model


def get_qwat_mapping():
    QWAT = get_qwat_model()
    WASSER = get_wasser_model()

    return {
        # Node
        QWAT.node: [WASSER.hydraulischer_knoten],

        # Network elements
        QWAT.hydrant: [WASSER.hydrant],
        QWAT.tank: [WASSER.wasserbehaelter],
        QWAT.pump: [WASSER.foerderanlage],
        QWAT.treatment: [WASSER.anlage],
        QWAT.subscriber: [WASSER.hausanschluss],
        # QWAT.???: [WASSER.absperrorgan],
        # QWAT.???: [WASSER.rohrleitungsteil],
        # QWAT.???: [WASSER.muffen],
        # QWAT.???: [WASSER.uebrige],
        # QWAT.???: [WASSER.wassergewinnungsanlage],

        # Pipe
        QWAT.pipe: [WASSER.leitung],
    }

    # AVAILABLE TABLES
    # WASSER.absperrorgan, WASSER.anlage, WASSER.baseclass, WASSER.foerderanlage, WASSER.hausanschluss, WASSER.hydrant, WASSER.hydraulischer_knoten, WASSER.hydraulischer_strang, WASSER.leitung, WASSER.leitung_strang_assoc, WASSER.leitungsknoten, WASSER.leitungsknoten_knoten_assoc, WASSER.leitungspunkt, WASSER.metaattribute, WASSER.muffen, WASSER.rohrleitungsteil, WASSER.schadenstelle, WASSER.sia405_15_lv95sia405_wasser_lk_anlage, WASSER.sia405_15_lv95sia405_wasser_lk_leitung, WASSER.sia405_15_lv95sia405_wasser_lk_leitung_text, WASSER.sia405_15_lv95sia405_wasser_lk_leitung_textassoc, WASSER.sia405_15_lv95sia405_wasser_lk_leitungsknoten, WASSER.sia405_15_lv95sia405_wasser_lk_leitungsknoten_text, WASSER.sia405_15_lv95sia405_wasser_lk_leitungsknoten_textassoc, WASSER.sia405_15_lv95sia405_wasser_lk_spezialbauwerk, WASSER.sia405_15_lv95sia405_wasser_lk_spezialbauwerk_flaeche, WASSER.sia405_15_lv95sia405_wasser_lk_spezialbauwerk_flaecheassoc, WASSER.sia405_15_lv95sia405_wasser_lk_spezialbauwerk_linie, WASSER.sia405_15_lv95sia405_wasser_lk_spezialbauwerk_linieassoc, WASSER.sia405_15_lv95sia405_wasser_lk_spezialbauwerk_text, WASSER.sia405_15_lv95sia405_wasser_lk_spezialbauwerk_textassoc, WASSER.sia405_baseclass, WASSER.sia405_symbolpos, WASSER.sia405_textpos, WASSER.spezialbauwerk, WASSER.spezialbauwerk_flaeche, WASSER.spezialbauwerk_linie, WASSER.symbolpos, WASSER.t_ili2db_attrname, WASSER.t_ili2db_basket, WASSER.t_ili2db_classname, WASSER.t_ili2db_dataset, WASSER.t_ili2db_inheritance, WASSER.t_ili2db_model, WASSER.t_ili2db_settings, WASSER.textpos, WASSER.uebrige, WASSER.wasserbehaelter, WASSER.wassergewinnungsanlage

    # NOT YET MAPPED
    # QWAT.bedding: [WASSER.REPLACE_ME],
    # QWAT.chamber: [WASSER.REPLACE_ME],
    # QWAT.cistern: [WASSER.REPLACE_ME],
    # QWAT.consumptionzone: [WASSER.REPLACE_ME],
    # QWAT.cover: [WASSER.REPLACE_ME],
    # QWAT.cover_type: [WASSER.REPLACE_ME],
    # QWAT.crossing: [WASSER.REPLACE_ME],
    # QWAT.distributor: [WASSER.REPLACE_ME],
    # QWAT.district: [WASSER.REPLACE_ME],
    # QWAT.folder: [WASSER.REPLACE_ME],
    # QWAT.hydrant_material: [WASSER.REPLACE_ME],
    # QWAT.hydrant_model_inf: [WASSER.REPLACE_ME],
    # QWAT.hydrant_model_sup: [WASSER.REPLACE_ME],
    # QWAT.hydrant_output: [WASSER.REPLACE_ME],
    # QWAT.hydrant_provider: [WASSER.REPLACE_ME],
    # QWAT.installation: [WASSER.REPLACE_ME],
    # QWAT.leak: [WASSER.REPLACE_ME],
    # QWAT.leak_cause: [WASSER.REPLACE_ME],
    # QWAT.meter: [WASSER.REPLACE_ME],
    # QWAT.meter_reference: [WASSER.REPLACE_ME],
    # QWAT.network_element: [WASSER.REPLACE_ME],
    # QWAT.nominal_diameter: [WASSER.REPLACE_ME],
    # QWAT.object_reference: [WASSER.REPLACE_ME],
    # QWAT.overflow: [WASSER.REPLACE_ME],
    # QWAT.part: [WASSER.REPLACE_ME],
    # QWAT.part_type: [WASSER.REPLACE_ME],
    # QWAT.pipe_function: [WASSER.REPLACE_ME],
    # QWAT.pipe_installmethod: [WASSER.REPLACE_ME],
    # QWAT.pipe_material: [WASSER.REPLACE_ME],
    # QWAT.pipe_protection: [WASSER.REPLACE_ME],
    # QWAT.precision: [WASSER.REPLACE_ME],
    # QWAT.precisionalti: [WASSER.REPLACE_ME],
    # QWAT.pressurecontrol_type: [WASSER.REPLACE_ME],
    # QWAT.pressurezone: [WASSER.REPLACE_ME],
    # QWAT.printmap: [WASSER.REPLACE_ME],
    # QWAT.protectionzone: [WASSER.REPLACE_ME],
    # QWAT.protectionzone_type: [WASSER.REPLACE_ME],
    # QWAT.pump_operating: [WASSER.REPLACE_ME],
    # QWAT.pump_type: [WASSER.REPLACE_ME],
    # QWAT.remote: [WASSER.REPLACE_ME],
    # QWAT.remote_type: [WASSER.REPLACE_ME],
    # QWAT.samplingpoint: [WASSER.REPLACE_ME],
    # QWAT.source: [WASSER.REPLACE_ME],
    # QWAT.source_quality: [WASSER.REPLACE_ME],
    # QWAT.source_type: [WASSER.REPLACE_ME],
    # QWAT.status: [WASSER.REPLACE_ME],
    # QWAT.subscriber_reference: [WASSER.REPLACE_ME],
    # QWAT.subscriber_type: [WASSER.REPLACE_ME],
    # QWAT.survey_type: [WASSER.REPLACE_ME],
    # QWAT.surveypoint: [WASSER.REPLACE_ME],
    # QWAT.tank_firestorage: [WASSER.REPLACE_ME],
    # QWAT.valve: [WASSER.REPLACE_ME],
    # QWAT.valve_actuation: [WASSER.REPLACE_ME],
    # QWAT.valve_function: [WASSER.REPLACE_ME],
    # QWAT.valve_type: [WASSER.REPLACE_ME],
    # QWAT.visible: [WASSER.REPLACE_ME],
    # QWAT.watertype: [WASSER.REPLACE_ME],
    # QWAT.worker: [WASSER.REPLACE_ME],
