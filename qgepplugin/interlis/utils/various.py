import psycopg2
import os
import subprocess
import time
import collections
import configparser
import sys
import logging

from .. import config

logger = logging.getLogger(__package__)


class CmdException(BaseException):
    pass

def exec_(command, check=True):
    logger.info(f"EXECUTING: {command}")
    try:
        proc = subprocess.run(
            command,
            check=True,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
    except subprocess.CalledProcessError as e:
        if check:
            logger.exception(e.output.decode('windows-1252' if os.name == 'nt' else 'utf-8'))
            raise CmdException(f"Command errored ! See logs for more info.")
        return e.returncode
    return proc.returncode


def setup_test_db(template="full"):
    """
    As initializing demo data can be a bit slow (esp. if we want only a subset),
    we do these steps in a Docker container then commit it to an image, so we can
    start a clean database relatively quickly.

    We prepare three template databases : full, subset, empty
    And then copy those to config.PGDATABASE when needed to initialize an fresh db
    for testing.
    """

    pgconf = get_pgconf()

    def dexec_(cmd):
        return exec_(f"docker exec qgepqwat {cmd}")

    logger.info("SETTING UP QGEP/QWAT DATABASE...")
    r = exec_("docker inspect -f '{{.State.Running}}' qgepqwat", check=False)
    if r != 0:
        logger.info("Test container not running, we create it")

        exec_(f"docker run -d --rm -v qgepqwat_db:/var/lib/postgresql/data -p 5432:5432 --name qgepqwat -e POSTGRES_PASSWORD={pgconf['password'] or 'postgres'} -e POSTGRES_DB={pgconf['dbname'] or 'qgep_prod'} postgis/postgis")

        # Wait for PG
        while exec_("docker exec qgepqwat pg_isready", check=False) != 0:
            logger.info("Postgres not ready... we wait...")
            time.sleep(1)

        db_dont_exist = (
            dexec_("createdb -U postgres tpl_empty") == 0
            and dexec_("createdb -U postgres tpl_subset") == 0
            and dexec_("createdb -U postgres tpl_full")
        )
        if db_dont_exist:
            logger.info("Test templates don't exist, we create them")

            dexec_(f"dropdb -U postgres tpl_empty")
            dexec_(f"dropdb -U postgres tpl_subset")
            dexec_(f"dropdb -U postgres tpl_full")

            dexec_("apt-get update")
            dexec_("apt-get install -y wget")

            # Getting data
            dexec_("wget https://github.com/QGEP/datamodel/releases/download/1.5.4/qgep_1.5.4_structure_and_demo_data.backup")
            dexec_("wget https://github.com/QGEP/datamodel/releases/download/1.5.4/qgep_1.5.4_structure_with_value_lists.sql")
            dexec_("wget https://github.com/qwat/qwat-data-model/releases/download/1.3.5/qwat_v1.3.5_data_and_structure_sample.backup")
            dexec_("wget https://github.com/qwat/qwat-data-model/releases/download/1.3.5/qwat_v1.3.5_structure_only.sql")
            dexec_("wget https://github.com/qwat/qwat-data-model/releases/download/1.3.5/qwat_v1.3.5_value_list_data_only.sql")

            # Creating the template DB with empty structure
            dexec_("psql -f qgep_1.5.4_structure_with_value_lists.sql qgep_prod postgres")
            dexec_("psql -f qwat_v1.3.5_structure_only.sql qgep_prod postgres")
            dexec_("psql -f qwat_v1.3.5_value_list_data_only.sql qgep_prod postgres")
            dexec_("createdb -U postgres --template=qgep_prod tpl_empty")

            # Creating the template DB with full data
            dexec_('psql -U postgres -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE pid<>pg_backend_pid();"')
            dexec_("dropdb -U postgres qgep_prod --if-exists")
            dexec_("createdb -U postgres qgep_prod")
            dexec_("pg_restore -U postgres --dbname qgep_prod --verbose --no-privileges --exit-on-error qgep_1.5.4_structure_and_demo_data.backup")
            dexec_("pg_restore -U postgres --dbname qgep_prod --verbose --no-privileges --exit-on-error qwat_v1.3.5_data_and_structure_sample.backup")
            dexec_("createdb -U postgres --template=qgep_prod tpl_full")

            # Creating the template DB with subset data
            # THIS IS QUITE SLOW, WE DISABLE IT FOR NOW
            # connection = psycopg2.connect(
            #     f"host={pgconf['host']} port={pgconf['port']} dbname={pgconf['dbname']} user={pgconf['user']} password={pgconf['password']}"
            # )
            # connection.set_session(autocommit=True)
            # cursor = connection.cursor()
            # for schema in ["qgep_od", "qwat_od"]:
            #     # For each table that has a geometry column, we keep only features that are in a specific extent.
            #     cursor.execute("SELECT qgep_sys.drop_symbology_triggers();")
            #     cursor.execute(
            #         f"""SELECT c.table_name, c.column_name
            #                     FROM information_schema.columns c
            #                     JOIN information_schema.tables t ON t.table_schema = c.table_schema AND t.table_name = c.table_name AND t.table_type = 'BASE TABLE'
            #                     JOIN pg_type typ ON c.udt_name = typ.typname
            #                     WHERE c.table_schema = '{schema}' AND typname = 'geometry';"""
            #     )
            #     for row in cursor.fetchall():
            #         table, column = row
            #         logger.info(f"KEEPING ONLY A SUBSET OF {schema}.{table} (this can take a while)...")
            #         logger.info(f"DELETE FROM {schema}.{table} WHERE ({column} && ST_MakeEnvelope(2750260.6, 1264318.8, 2750335.0,1264367.7, 2056)) = FALSE;")
            #         try:
            #             cursor.execute(
            #                 f"DELETE FROM {schema}.{table} WHERE ({column} && ST_MakeEnvelope(2750260.6, 1264318.8, 2750335.0,1264367.7, 2056)) = FALSE;"
            #             )
            #         except psycopg2.errors.ForeignKeyViolation as e:
            #             logger.warning(f"Exception {e} !! we still continue...")
            #             pass

            #     if schema == 'qgep_od':
            #         # We delete orphaned wastewater_structure
            #         cursor.execute("DELETE FROM qgep_od.wastewater_structure WHERE fk_main_wastewater_node IS NULL;")

            #     cursor.execute("SELECT qgep_sys.create_symbology_triggers();")
            # cursor.close()
            # dexec_(f'psql -U postgres -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE pid<>pg_backend_pid();"')
            # dexec_(f"createdb -U postgres --template=qgep_prod tpl_subset")

            # # add our QWAT migrations
            # exec_(r'docker cp C:\Users\Olivier\Code\QWAT\data-model\update\delta\delta_1.3.6_add_vl_for_SIA_export.sql qgepqwatbuilder:/delta_1.3.6_add_vl_for_SIA_export.sql')
            # dexec_(f'psql -U postgres -d qgep_prod -f /delta_1.3.6_add_vl_for_SIA_export.sql')

    dexec_(f'psql -U postgres -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE pid<>pg_backend_pid();"')
    dexec_(f"dropdb -U postgres qgep_prod --if-exists")
    dexec_(f"createdb -U postgres --template=tpl_{template} qgep_prod")


def capfirst(s):
    return s[0].upper() + s[1:]


def invert_dict(d):
    return {v: k for k, v in d.items()}


def read_pgservice(service_name):
    """
    Returns a config object from a pg_service name (parsed from PGSERVICEFILE).
    """

    # Path for pg_service.conf
    if os.environ.get('PGSERVICEFILE'):
        PG_CONFIG_PATH = os.environ.get('PGSERVICEFILE')
    elif os.environ.get('PGSYSCONFDIR'):
        PG_CONFIG_PATH = os.path.join(os.environ.get('PGSYSCONFDIR'), 'pg_service.conf')
    else:
        PG_CONFIG_PATH = ' ~/.pg_service.conf'

    config = configparser.ConfigParser()
    if os.path.exists(PG_CONFIG_PATH):
        config.read(PG_CONFIG_PATH)

    return config[service_name] if service_name in config else {}


def get_pgconf():
    """
    Returns the postgres configuration (parsed from the config.PGSERVICE service and overriden by config.PG* settings)
    """

    if config.PGSERVICE:
        pgconf = read_pgservice(config.PGSERVICE)
    else:
        pgconf = {}

    if config.PGHOST:
        pgconf['host'] = config.PGHOST
    if config.PGPORT:
        pgconf['port'] = config.PGPORT
    if config.PGDATABASE:
        pgconf['dbname'] = config.PGDATABASE
    if config.PGUSER:
        pgconf['user'] = config.PGUSER
    if config.PGPASS:
        pgconf['password'] = config.PGPASS

    return collections.defaultdict(str, pgconf)
