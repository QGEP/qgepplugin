import os
import argparse

from . import utils
from . import config


def main(args):
    parser = argparse.ArgumentParser(description='ili2QWAT / ili2QGEP prototype entrypoint')
    parser.add_argument('model', choices=['qgep', 'qwat'], help='datamodel')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--import_xtf', help='input file')
    group.add_argument('--export_xtf', help='output file')
    group.add_argument('--gen_tpl', action='store_true', help='generate code templates')
    parser.add_argument('--force_recreate', action='store_true', help='drops schema and reruns ili2pg importschema')
    args = parser.parse_args(args)

    if args.model == 'qgep':
        utils.create_ili_schema(config.ABWASSER_SCHEMA, config.ABWASSER_ILI_MODEL, force_recreate=args.force_recreate)
        if args.export_xtf:
            from . import qgep
            qgep.export()
            utils.export_xtf_data(config.ABWASSER_SCHEMA, config.ABWASSER_ILI_MODEL_NAME, args.export_xtf)
        elif args.import_xtf:
            utils.import_xtf_data(config.ABWASSER_SCHEMA, args.import_xtf)
            from . import qgep
            qgep.import_()
        elif args.gen_tpl:
            from .datamodels.mapping_qgep import MAPPING
            from .datamodels.qgep import Classes as QGEP
            from .datamodels.abwasser import Classes as ABWASSER
            utils.generate_template("qgep", "abwasser", QGEP, ABWASSER, MAPPING)

    elif args.model == 'qwat':
        utils.create_ili_schema(config.WASSER_SCHEMA, config.WASSER_ILI_MODEL, force_recreate=args.force_recreate)
        if args.export_xtf:
            from . import qwat
            qwat.export()
            utils.export_xtf_data(config.WASSER_SCHEMA, config.WASSER_ILI_MODEL_NAME, args.export_xtf)
        elif args.import_xtf:
            utils.import_xtf_data(config.WASSER_SCHEMA, args.import_xtf)
            from . import qwat
            qwat.import_()
        elif args.gen_tpl:
            from .datamodels.mapping_qwat import MAPPING
            from .datamodels.qwat import Classes as QWAT
            from .datamodels.wasser import Classes as WASSER
            utils.generate_template("qwat", "wasser", QWAT, WASSER, MAPPING)
