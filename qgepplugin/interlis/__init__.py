import os
import argparse

from . import utils
from . import config


def main(args):
    parser = argparse.ArgumentParser(description='ili2QWAT / ili2QGEP prototype entrypoint')
    parser.add_argument('model', choices=['qgep', 'qwat'])
    parser.add_argument('direction', choices=['export', 'import'])
    parser.add_argument('xtf_file')
    parser.add_argument('--force_recreate', action='store_true', help='Drops and recreate the ili2pg schemas if already existing')
    args = parser.parse_args(args)

    # Create the database and import the ILI model
    utils.setup_test_db(keep_only_subset=True)

    if args.model == 'qgep':
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

    elif args.model == 'qwat':
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
