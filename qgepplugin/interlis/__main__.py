from . import utils
from . import config

utils.setup_test_db()
utils.create_ili_schema(config.WASSER_SCHEMA, config.WASSER_ILI_MODEL, smart=0)
utils.create_ili_schema(config.WASSER_SCHEMA+'_smart1', config.WASSER_ILI_MODEL, smart=1)
utils.create_ili_schema(config.WASSER_SCHEMA+'_smart2', config.WASSER_ILI_MODEL, smart=2)

from . import qwat
from . import qwat_generator

qwat_generator.generate()
qwat.export()