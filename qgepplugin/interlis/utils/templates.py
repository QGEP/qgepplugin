import os
import collections

from jinja2 import Environment, FileSystemLoader
from sqlalchemy.orm.attributes import InstrumentedAttribute


def generate_template(model_name, ilimodel_name, MODEL, ILIMODEL, mapping):

    def filter_classfields(cls):
        """Jinja filter used in the template"""
        available_fields = collections.defaultdict(list)
        for attr_name, attr in list(cls.__dict__.items()):
            # if attr_name.startswith('__'):
            #     continue
            if not isinstance(attr, InstrumentedAttribute):
                continue
            if not hasattr(attr.property, "columns"):
                key = "_relations_"
            else:
                key = attr.property.columns[0].table.name
            available_fields[key].append(attr_name)
        ordered_tables = ["_relations_"] + list(c.__table__.name for c in cls.__mro__ if hasattr(c, "__table__"))
        return sorted(
            available_fields.items(),
            key=lambda i: ordered_tables.index(i[0]),
            reverse=True,
        )

    def filter_classesnames(classes):
        """Jinja filter used in the template"""
        return ", ".join(c.__name__ for c in classes)

    def filter_qualclassesnames(classes):
        """Jinja filter used in the template"""
        return ", ".join(f"{ilimodel_name.upper()}.{c.__name__}" for c in classes)

    tpl_folder = os.path.join(os.path.dirname(__file__), '..', 'tpl')
    env = Environment(loader=FileSystemLoader(tpl_folder), lstrip_blocks=True, trim_blocks=True)
    env.filters["classfields"] = filter_classfields
    env.filters["classesnames"] = filter_classesnames
    env.filters["qualclassesnames"] = filter_qualclassesnames

    variables = {
        "mapping": mapping,
        "MODEL": MODEL,
        "ILIMODEL": ILIMODEL,
        "model_name": model_name,
        "ilimodel_name": ilimodel_name,
    }

    # Generate code stub for the import script
    template = env.get_template("import_.py.tpl")
    result = template.render(variables)
    path = os.path.join(os.path.dirname(__file__), "..", model_name, "import_.py.tpl")
    open(path, "w", newline="\n").write(result)

    # Generate code stub for the export script
    template = env.get_template("export.py.tpl")
    result = template.render(variables)
    path = os.path.join(os.path.dirname(__file__), "..", model_name, "export.py.tpl")
    open(path, "w", newline="\n").write(result)

    # Generate code stub for the mapping script
    template = env.get_template("mapping.py.tpl")
    result = template.render(variables)
    path = os.path.join(os.path.dirname(__file__), "..", model_name, "mapping.py.tpl")
    open(path, "w", newline="\n").write(result)
