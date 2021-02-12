import argparse

from . import utils
from . import config

from .qgep.export import qgep_export
from .qgep.import_ import qgep_import
from .qwat.export import qwat_export
from .qwat.import_ import qwat_import
from .qwat.mapping import get_qwat_mapping
from .qgep.mapping import get_qgep_mapping
from .qwat.model_qwat import Base as BaseQwat
from .qwat.model_wasser import Base as BaseWasser
from .qgep.model_qgep import Base as BaseQgep
from .qgep.model_abwasser import Base as BaseAbwasser


def main(args):

    parser = argparse.ArgumentParser(description="ili2QWAT / ili2QGEP prototype entrypoint")
    subparsers = parser.add_subparsers(title='subcommands')

    parser_io = subparsers.add_parser('io', help='import/export XTF files')
    parser_io.set_defaults(parser='io')
    parser_io.add_argument("--recreate_schema", action="store_true", help="drops schema and reruns ili2pg importschema")
    parser_io.add_argument("model", choices=["qgep", "qwat"], help="datamodel")
    group = parser_io.add_mutually_exclusive_group()
    group.add_argument("--import_xtf", help="input file")
    group.add_argument("--export_xtf", help="output file")

    parser_tpl = subparsers.add_parser('tpl', help='generate code templates')
    parser_tpl.set_defaults(parser='tpl')
    parser_setupdb = subparsers.add_parser('setupdb', help='setup test db')
    parser_setupdb.set_defaults(parser='setupdb')
    parser_setupdb.add_argument("type", choices=["empty", "full", "subset"], help="type")

    args = parser.parse_args(args)

    if args.parser == 'io' and args.model == "qgep":
        utils.ili2db.create_ili_schema(config.ABWASSER_SCHEMA, config.ABWASSER_ILI_MODEL, recreate_schema=args.recreate_schema)

        if args.export_xtf:
            qgep_export()
            utils.ili2db.export_xtf_data(config.ABWASSER_SCHEMA, config.ABWASSER_ILI_MODEL_NAME, args.export_xtf)
        elif args.import_xtf:
            utils.ili2db.import_xtf_data(config.ABWASSER_SCHEMA, args.import_xtf)
            qgep_import()

    elif args.parser == 'io' and args.model == "qwat":
        utils.ili2db.create_ili_schema(config.WASSER_SCHEMA, config.WASSER_ILI_MODEL, recreate_schema=args.recreate_schema)

        if args.export_xtf:
            qwat_export()
            utils.ili2db.export_xtf_data(config.WASSER_SCHEMA, config.WASSER_ILI_MODEL_NAME, args.export_xtf)
        elif args.import_xtf:
            utils.ili2db.import_xtf_data(config.WASSER_SCHEMA, args.import_xtf)
            qwat_import()

    elif args.parser == 'tpl':
        utils.ili2db.create_ili_schema(config.WASSER_SCHEMA, config.WASSER_ILI_MODEL, recreate_schema=True)
        utils.ili2db.create_ili_schema(config.ABWASSER_SCHEMA, config.ABWASSER_ILI_MODEL, recreate_schema=True)

        QWATMAPPING = get_qwat_mapping()
        QGEPMAPPING = get_qgep_mapping()

        utils.templates.generate_template("qgep", "abwasser", BaseQgep, BaseAbwasser, QGEPMAPPING)
        utils.templates.generate_template("qwat", "wasser", BaseQwat, BaseWasser, QWATMAPPING)

    elif args.parser == 'setupdb':
        utils.various.setup_test_db(args.type)
