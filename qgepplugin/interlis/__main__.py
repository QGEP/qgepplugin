import os

from . import utils
from . import config
from . import qwat
from . import qwat_generator
from . import qgep
from . import qgep_generator

from .ili2py import Ili2Py

# Create the database and import the ILI model
utils.setup_test_db()
utils.create_ili_schema(config.WASSER_SCHEMA, config.WASSER_ILI_MODEL)
utils.create_ili_schema(config.ABWASSER_SCHEMA, config.ABWASSER_ILI_MODEL)
# utils.create_ili_schema(config.WASSER_SCHEMA, config.WASSER_ILI_MODEL_FR)
# utils.create_ili_schema(config.ABWASSER_SCHEMA, config.ABWASSER_ILI_MODEL_FR)
# utils.import_xtf_data(config.ABWASSER_SCHEMA, os.path.join(config.DATA_FOLDER, 'test_without_abwasserbauwerkref.xtf'))

# Generate matching spreadsheets (to be used in https://docs.google.com/spreadsheets/d/1I7ccjidbh4dyRLp-tYRBU-Oc1KX8SqU0EUZm_jcv5HQ/edit#gid=530687807)
# from . import match_maker
# match_maker.make_file()


qwat_generator.generate()
# qgep_generator.generate()
qwat.export()
# qgep.export()
# utils.export_xtf_data(config.WASSER_SCHEMA, config.WASSER_ILI_MODEL_NAME)
# utils.export_xtf_data(config.ABWASSER_SCHEMA, config.ABWASSER_ILI_MODEL_NAME)
