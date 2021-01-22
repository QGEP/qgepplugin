import psycopg2
import os
import subprocess
import collections
import functools
import sqlalchemy

from jinja2 import Environment, FileSystemLoader, select_autoescape
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.ext.automap import AutomapBase, automap_base, name_for_collection_relationship, name_for_scalar_relationship, generate_relationship

from . import config


def exec_(command, check=True):
    print("")
    print("!"*80)
    print(f"EXECUTING: {command}")
    if check:
        return subprocess.check_call(command)
    else:
        return subprocess.call(command)


def setup_test_db(keep_only_subset=False):

    print("SETTING UP QGEP/QWAT DATABASE...")
    r = exec_("docker inspect -f '{{.State.Running}}' qgepqwat", check=False)
    if r == 0:
        print("Already running")
        return

    exec_(f'docker run -d --rm -p 5432:5432 --name qgepqwat -e POSTGRES_PASSWORD={config.PGPASS} -e POSTGRES_DB={config.PGDATABASE} postgis/postgis')
    exec_('docker exec qgepqwat apt-get update')
    exec_('docker exec qgepqwat apt-get install -y wget')

    exec_('docker exec qgepqwat wget https://github.com/QGEP/datamodel/releases/download/1.5.3/qgep_1.5.3_structure_and_demo_data.backup')
    exec_(f'docker exec qgepqwat pg_restore -U {config.PGUSER} --dbname {config.PGDATABASE} --verbose --no-privileges --exit-on-error qgep_1.5.3_structure_and_demo_data.backup')

    exec_('docker exec qgepqwat wget https://github.com/qwat/qwat-data-model/releases/download/1.3.5/qwat_v1.3.5_data_and_structure_sample.backup')
    exec_(f'docker exec qgepqwat pg_restore -U {config.PGUSER} --dbname {config.PGDATABASE} --verbose --no-privileges --exit-on-error qwat_v1.3.5_data_and_structure_sample.backup')

    # add our QWAT migrations
    exec_(r'docker cp C:\Users\Olivier\Code\QWAT\data-model\update\delta\delta_1.3.6_add_vl_for_SIA_export.sql qgepqwat:/delta_1.3.6_add_vl_for_SIA_export.sql')
    exec_(f'docker exec qgepqwat psql -U postgres -d qgep_prod -f /delta_1.3.6_add_vl_for_SIA_export.sql')

    if keep_only_subset:
        # delete rows outside of some extent (to make dataset smaller)
        print("CONNECTING TO DATABASE...")
        connection = psycopg2.connect(f"host={config.PGHOST} dbname={config.PGDATABASE} user={config.PGUSER} password={config.PGPASS}")
        connection.set_session(autocommit=True)
        cursor = connection.cursor()
        for schema in ['qgep_od', 'qwat_od']:
            cursor.execute("SELECT qgep_sys.drop_symbology_triggers();")
            cursor.execute(f"""SELECT c.table_name, c.column_name
                            FROM information_schema.columns c
                            JOIN information_schema.tables t ON t.table_schema = c.table_schema AND t.table_name = c.table_name AND t.table_type = 'BASE TABLE'
                            JOIN pg_type typ ON c.udt_name = typ.typname
                            WHERE c.table_schema = '{schema}' AND typname = 'geometry';""")
            for row in cursor.fetchall():
                table, column = row
                print(f"KEEPING ONLY A SUBSET OF {schema}.{table} (this can take a while)...")
                print(f"DELETE FROM {schema}.{table} WHERE ({column} && ST_MakeEnvelope(2750260.6, 1264318.8, 2750335.0,1264367.7, 2056)) = FALSE;")
                # cursor.execute(f"DELETE FROM {schema}.{table} WHERE ({column} && ST_MakeEnvelope(2750260.6, 1264318.8, 2750335.0,1264367.7, 2056)) = FALSE;")
            cursor.execute("SELECT qgep_sys.create_symbology_triggers();")


def create_ili_schema(schema, model, force_recreate=False):
    print("CONNECTING TO DATABASE...")
    connection = psycopg2.connect(f"host={config.PGHOST} dbname={config.PGDATABASE} user={config.PGUSER} password={config.PGPASS}")
    connection.set_session(autocommit=True)
    cursor = connection.cursor()

    if not force_recreate:
        # If the schema already exists, we just truncate all tables
        cursor.execute(f"SELECT schema_name FROM information_schema.schemata WHERE schema_name = '{schema}';");
        if cursor.rowcount > 0:
            print(f"Schema {schema} already exists, we truncate instead")
            cursor.execute(f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{schema}';")
            for row in cursor.fetchall():
                cursor.execute(f"TRUNCATE TABLE {schema}.{row[0]} CASCADE;")
            return

    print(f"CREATING THE SCHEMA {schema}...")
    cursor.execute(f"DROP SCHEMA IF EXISTS {schema} CASCADE ;")
    cursor.execute(f"CREATE SCHEMA {schema};")
    connection.commit()

    print(f"ILIDB SCHEMAIMPORT INTO {schema}...")
    # if "_f-" in model:
    #     lang = f'fr'
    # else:
    #     lang = f'de'
    lang = f'de'

    exec_(
        f"java -jar {config.ILI2PG} --schemaimport --dbhost {config.PGHOST} --dbusr {config.PGUSER} --dbpwd {config.PGPASS} --dbdatabase {config.PGDATABASE} --dbschema {schema} --setupPgExt --createGeomIdx --createFk --createFkIdx --createTidCol --importTid --noSmartMapping --defaultSrsCode 2056 --strokeArcs --log debug-create.txt --nameLang {lang} {model}"
    )


def import_xtf_data(schema, xtf_file):
    print("IMPORTING XTF DATA...")
    exec_(
        f"java -jar {config.ILI2PG} --import --deleteData --dbhost {config.PGHOST} --dbusr {config.PGUSER} --dbpwd {config.PGPASS} --dbdatabase {config.PGDATABASE} --dbschema {schema} --modeldir {config.ILI_FOLDER} --disableValidation --createTidCol --defaultSrsCode 2056 --log debug-import.txt {xtf_file}"
    )


def export_xtf_data(schema, model_name, xtf_file):

    print("EXPORT ILIDB...")

    exec_(
        f"java -jar {config.ILI2PG} --export --models {model_name} --dbhost {config.PGHOST} --dbusr {config.PGUSER} --dbpwd {config.PGPASS} --dbdatabase {config.PGDATABASE} --dbschema {schema} --modeldir {config.ILI_FOLDER} --disableValidation --createTidCol --defaultSrsCode 2056 --log debug-export.txt {xtf_file}"
    )


def create_engine():
    return sqlalchemy.create_engine(f'postgresql://{config.PGUSER}:{config.PGPASS}@{config.PGHOST}:5432/{config.PGDATABASE}')


def custom_name_for_collection_relationship(base, local_cls, referred_cls, constraint):
    # This customizes the name for backwards relation, avoiding clashes for inherited classes.
    # See https://stackoverflow.com/a/48288656/13690651
    if constraint.name:
        return 'BWREL_'+constraint.name.lower()
    # if this didn't work, revert to the default behavior
    return 'BWREL_'+name_for_collection_relationship(base, local_cls, referred_cls, constraint)

def custom_name_for_scalar_relationship(base, local_cls, referred_cls, constraint):
    # This customizes the name for backwards relation, avoiding clashes for inherited classes.
    # See https://stackoverflow.com/a/48288656/13690651
    if len(constraint.columns) == 1:
        return constraint.columns.keys()[0] + "_REL"
    if constraint.name:
        return 'REL_'+constraint.name.lower()
    # if this didn't work, revert to the default behavior
    return 'REL_'+name_for_scalar_relationship(base, local_cls, referred_cls, constraint)

def custom_generate_relationship(base, direction, return_fn, attrname, local_cls, referred_cls, **kw):
    # We skip backwards relations for now as they seem to be undeterministic
    # (probably because of multiple backrefs between same models)
    if attrname.startswith('BWREL'):
        return None
    return generate_relationship(base, direction, return_fn, attrname, local_cls, referred_cls, **kw)

def capfirst(s):
    return s[0].upper()+s[1:]

def invert_dict(d):
    return {v: k for k, v in d.items()}

def generate_template(model_name, ilimodel_name, MODEL, ILIMODEL, mapping):


    def filter_classfields(cls):
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
        ordered_tables = ["_relations_"]+list(c.__table__.name for c in cls.__mro__ if hasattr(c, '__table__'))
        return sorted(available_fields.items(), key=lambda i: ordered_tables.index(i[0]), reverse=True)

    def filter_classesnames(classes):
        return ', '.join(f"{ilimodel_name.upper()}.{c.__name__}" for c in classes)

    env = Environment(
        loader=FileSystemLoader(os.path.dirname(__file__)),
        lstrip_blocks=True,
        trim_blocks=True,
    )

    env.filters['classfields'] = filter_classfields
    env.filters['classesnames'] = filter_classesnames

    # Generate code stub for the import script
    template = env.get_template('template_importexport.py.tpl')
    result = template.render({
        'mapping': mapping,
        'model_name': model_name,
        'ilimodel_name': ilimodel_name,
    })
    open(os.path.join(os.path.dirname(__file__), f'{model_name}.py.tpl'), 'w', newline='\n').write(result)

    # Generate code stub for the mapping
    template = env.get_template('template_mapping.py.tpl')
    result = template.render({
        'mapping': mapping,
        'MODEL': MODEL,
        'ILIMODEL': ILIMODEL,
        'model_name': model_name,
        'ilimodel_name': ilimodel_name,
    })
    open(os.path.join(os.path.dirname(__file__), 'datamodels', f'mapping.{model_name}.py.tpl'), 'w', newline='\n').write(result)

class TidMaker:
    """
    Helper class that creates globally unique integer primary key forili2pg class (t_id)
    from a a QGEP/QWAT id (obj_id or id).
    """

    def __init__(self, id_attribute='id'):
        self._id_attr = id_attribute
        self._autoincrementer = collections.defaultdict(lambda: len(self._autoincrementer))

    def tid_for_row(self, row, for_class=None):
        # tid are globally unique, while ids are only guaranteed unique per table,
        # so include the base table in the key
        # this finds the base class (the first parent class before sqlalchemy.ext.automap.Base)
        class_for_id = row.__class__.__mro__[row.__class__.__mro__.index(AutomapBase) - 2]
        key = (class_for_id, getattr(row, self._id_attr), for_class)
        return self._autoincrementer[key]
