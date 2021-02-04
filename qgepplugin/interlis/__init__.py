import argparse

from . import utils
from . import config


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

        from .qgep.export import export
        from .qgep.import_ import import_
        from .qgep.mapping import MAPPING
        from .qgep.model_qgep import QGEP
        from .qgep.model_abwasser import ABWASSER

        if args.export_xtf:
            export()
            utils.ili2db.export_xtf_data(config.ABWASSER_SCHEMA, config.ABWASSER_ILI_MODEL_NAME, args.export_xtf)
        elif args.import_xtf:
            utils.ili2db.import_xtf_data(config.ABWASSER_SCHEMA, args.import_xtf)
            import_()

    elif args.parser == 'io' and args.model == "qwat":
        utils.ili2db.create_ili_schema(config.WASSER_SCHEMA, config.WASSER_ILI_MODEL, recreate_schema=args.recreate_schema)

        from .qwat.export import export
        from .qwat.import_ import import_
        from .qwat.mapping import MAPPING
        from .qwat.model_qwat import QWAT
        from .qwat.model_wasser import WASSER

        if args.export_xtf:
            export()
            utils.ili2db.export_xtf_data(config.WASSER_SCHEMA, config.WASSER_ILI_MODEL_NAME, args.export_xtf)
        elif args.import_xtf:
            utils.ili2db.import_xtf_data(config.WASSER_SCHEMA, args.import_xtf)
            import_()

    elif args.parser == 'tpl':
        utils.ili2db.create_ili_schema(config.WASSER_SCHEMA, config.WASSER_ILI_MODEL, recreate_schema=True)
        utils.ili2db.create_ili_schema(config.ABWASSER_SCHEMA, config.ABWASSER_ILI_MODEL, recreate_schema=True)

        from .qwat.export import export
        from .qwat.import_ import import_
        from .qwat.mapping import MAPPING as QWATMAPPING
        from .qwat.model_qwat import QWAT
        from .qwat.model_wasser import WASSER

        from .qgep.export import export
        from .qgep.import_ import import_
        from .qgep.mapping import MAPPING as QGEPMAPPING
        from .qgep.model_qgep import QGEP
        from .qgep.model_abwasser import ABWASSER

        utils.templates.generate_template("qgep", "abwasser", QGEP, ABWASSER, QGEPMAPPING)
        utils.templates.generate_template("qwat", "wasser", QWAT, WASSER, QWATMAPPING)

    elif args.parser == 'setupdb':
        utils.various.setup_test_db(args.type)
