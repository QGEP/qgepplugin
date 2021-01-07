from . import utils
from . import config


# Create the database and import the ILI model
utils.setup_test_db()
# utils.create_ili_schema(config.WASSER_SCHEMA, config.WASSER_ILI_MODEL, smart=0)
# utils.create_ili_schema(config.ABWASSER_SCHEMA, config.ABWASSER_ILI_MODEL, smart=0)
utils.create_ili_schema(config.WASSER_SCHEMA, config.WASSER_ILI_MODEL_FR, smart=0)
utils.create_ili_schema(config.ABWASSER_SCHEMA, config.ABWASSER_ILI_MODEL_FR, smart=0)

# Generate matching spreadsheets (to be used in https://docs.google.com/spreadsheets/d/1I7ccjidbh4dyRLp-tYRBU-Oc1KX8SqU0EUZm_jcv5HQ/edit#gid=530687807)
# from . import match_maker
# match_maker.make_file()

# from . import qwat
# from . import qwat_generator

# qwat_generator.generate()
# qwat.export()

# utils.export_ili_schema(config.WASSER_SCHEMA, config.WASSER_ILI_MODEL_NAME_FR, smart=0, lang='fr')


from . import qgep
from . import qgep_generator

qgep_generator.generate()
qgep.export()