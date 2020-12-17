from . import utils

utils.setup_test_db()

from . import qwat
from . import qwat_generator
from . import config


utils.create_ili_schema(config.WASSER_SCHEMA, config.WASSER_ILI_MODEL)
utils.create_ili_schema(config.WASSER_SCHEMA+'_dumb', config.WASSER_ILI_MODEL, smart=False)

qwat_generator.generate()
qwat.export()