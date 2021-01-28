import argparse

from . import utils
from . import config


def main(args):
    parser = argparse.ArgumentParser(description="ili2QWAT / ili2QGEP prototype entrypoint")
    parser.add_argument("model", choices=["qgep", "qwat"], help="datamodel")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--import_xtf", help="input file")
    group.add_argument("--export_xtf", help="output file")
    group.add_argument("--gen_tpl", action="store_true", help="generate code templates")
    parser.add_argument("--recreate_schema", action="store_true", help="drops schema and reruns ili2pg importschema")
    args = parser.parse_args(args)

    if args.model == "qgep":
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
        elif args.gen_tpl:
            utils.templates.generate_template("qgep", "abwasser", QGEP, ABWASSER, MAPPING)

    elif args.model == "qwat":
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
        elif args.gen_tpl:
            utils.templates.generate_template("qwat", "wasser", QWAT, WASSER, MAPPING)
