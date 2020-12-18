from . import utils
from . import config
from . import ili_generator

ili_generator.generate(config.BASE_ILI_MODEL, config.BASE_ILI_MODEL_FR)
ili_generator.generate(config.BASE_SIA_ILI_MODEL, config.BASE_SIA_ILI_MODEL_FR)
ili_generator.generate(config.WASSER_ILI_MODEL, config.WASSER_ILI_MODEL_FR)

exit(0)


utils.setup_test_db()
utils.create_ili_schema(config.WASSER_SCHEMA, config.WASSER_ILI_MODEL, smart=0, lang="fr")
# utils.create_ili_schema(config.WASSER_SCHEMA+'_smart1', config.WASSER_ILI_MODEL, smart=1)
# utils.create_ili_schema(config.WASSER_SCHEMA+'_smart2', config.WASSER_ILI_MODEL, smart=2)
utils.create_ili_schema(config.ABWASSER_SCHEMA, config.ABWASSER_ILI_MODEL, smart=0, lang="fr")

from . import match_maker
match_maker.make_file()

from . import qwat
from . import qwat_generator

qwat_generator.generate()
qwat.export()