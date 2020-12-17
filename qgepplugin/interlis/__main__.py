from . import utils
from . import qwat
from . import qwat_generator
from . import config

utils.setup_test_db()
utils.create_ili_schema(config.QWAT_ILI_SCHEMA, config.QWAT_ILI_MODEL)

qwat_generator.generate()
# qwat.export()