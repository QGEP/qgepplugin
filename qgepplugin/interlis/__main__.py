from . import utils
from . import config
from . import qwat_ili_generator

# Generate stub models from ILI file
# qwat_ili_generator.generate(config.BASE_ILI_MODEL, config.BASE_ILI_MODEL_FR)
# qwat_ili_generator.generate(config.BASE_SIA_ILI_MODEL, config.BASE_SIA_ILI_MODEL_FR)
# qwat_ili_generator.generate(config.WASSER_ILI_MODEL, config.WASSER_ILI_MODEL_FR)
qwat_ili_generator.generate(config.BASE_ILI_MODEL_FR, config.BASE_ILI_MODEL)
qwat_ili_generator.generate(config.BASE_SIA_ILI_MODEL_FR, config.BASE_SIA_ILI_MODEL)
qwat_ili_generator.generate(config.WASSER_ILI_MODEL_FR, config.WASSER_ILI_MODEL)
# exit(0)

# Create the database and import the ILI model
utils.setup_test_db()
# utils.create_ili_schema(config.WASSER_SCHEMA, config.WASSER_ILI_MODEL, smart=0)
# utils.create_ili_schema(config.ABWASSER_SCHEMA, config.ABWASSER_ILI_MODEL, smart=0)
utils.create_ili_schema(config.WASSER_SCHEMA, config.WASSER_ILI_MODEL_FR, smart=0)
utils.create_ili_schema(config.ABWASSER_SCHEMA, config.ABWASSER_ILI_MODEL_FR, smart=0)

# Generate matching spreadsheets (to be used in https://docs.google.com/spreadsheets/d/1I7ccjidbh4dyRLp-tYRBU-Oc1KX8SqU0EUZm_jcv5HQ/edit#gid=530687807)
# from . import match_maker
# match_maker.make_file()

from . import qwat
from . import qwat_generator

qwat_generator.generate()
qwat.export()