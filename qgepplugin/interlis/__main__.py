import os
import argparse

from . import utils
from . import config

from .ili2py import Ili2Py

parser = argparse.ArgumentParser(description='Interlis<->QWAT/QGEP prototype')
parser.add_argument('model', choices=['QGEP', 'QWAT'])
parser.add_argument('direction', choices=['export', 'import'])
parser.add_argument('xtf_file')
parser.add_argument('--force_recreate', action='store_true', help='Drops and recreate the ili2pg schemas if already existing')
args = parser.parse_args()


# Create the database and import the ILI model
utils.setup_test_db()

if args.model == 'QGEP':
    utils.create_ili_schema(config.ABWASSER_SCHEMA, config.ABWASSER_ILI_MODEL, force_recreate=args.force_recreate)
    from . import qgep
    from . import qgep_generator
    qgep_generator.generate()
    if args.direction == 'export':
        qgep.export()
        utils.export_xtf_data(config.ABWASSER_SCHEMA, config.ABWASSER_ILI_MODEL_NAME, args.xtf_file)
    elif args.direction == 'import':
        utils.import_xtf_data(config.ABWASSER_SCHEMA, args.xtf_file)
        # qgep.import_()

elif args.model == 'QWAT':
    utils.create_ili_schema(config.WASSER_SCHEMA, config.WASSER_ILI_MODEL, force_recreate=args.force_recreate)
    from . import qwat
    from . import qwat_generator
    qwat_generator.generate()
    if args.direction == 'export':
        qwat.export()
        utils.export_xtf_data(config.WASSER_SCHEMA, config.WASSER_ILI_MODEL_NAME, args.xtf_file)
    elif args.direction == 'import':
        utils.import_xtf_data(config.WASSER_SCHEMA, args.xtf_file)
        # qwat.import_()
