import psycopg2
import subprocess
import time
import collections

from .. import config


def exec_(command, check=True, silent=False):
    print(f"EXECUTING: {command}")
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
            print(e.output)
            raise Exception(f"Command errored ! See logs for more info.")
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

    print("SETTING UP QGEP/QWAT DATABASE...")
    r = exec_("docker inspect -f '{{.State.Running}}' qgepqwat", check=False, silent=True)
    if r != 0:
        print("Test container not running, we create it")

        exec_(
            f"docker run -d --rm -p 5432:5432 --name qgepqwat -e POSTGRES_PASSWORD={config.PGPASS} -e POSTGRES_DB={config.PGDATABASE} postgis/postgis"
        )
        exec_("docker exec qgepqwat apt-get update")
        exec_("docker exec qgepqwat apt-get install -y wget")

        # Getting data
        exec_(
            "docker exec qgepqwat wget https://github.com/QGEP/datamodel/releases/download/1.5.4/qgep_1.5.4_structure_and_demo_data.backup"
        )
        exec_(
            "docker exec qgepqwat wget https://github.com/QGEP/datamodel/releases/download/1.5.4/qgep_1.5.4_structure_with_value_lists.sql"
        )
        exec_(
            "docker exec qgepqwat wget https://github.com/qwat/qwat-data-model/releases/download/1.3.5/qwat_v1.3.5_data_and_structure_sample.backup"
        )
        exec_(
            "docker exec qgepqwat wget https://github.com/qwat/qwat-data-model/releases/download/1.3.5/qwat_v1.3.5_structure_only.sql"
        )
        exec_(
            "docker exec qgepqwat wget https://github.com/qwat/qwat-data-model/releases/download/1.3.5/qwat_v1.3.5_value_list_data_only.sql"
        )

        # Wait for PG
        while exec_("docker exec qgepqwat pg_isready", check=False, silent=True) != 0:
            print("Postgres not ready... we wait...")
            time.sleep(1)

        # Creating the template DB with empty structure
        exec_(
            f"docker exec qgepqwat psql -f qgep_1.5.4_structure_with_value_lists.sql {config.PGDATABASE} {config.PGUSER}"
        )
        exec_(f"docker exec qgepqwat psql -f qwat_v1.3.5_structure_only.sql {config.PGDATABASE} {config.PGUSER}")
        exec_(f"docker exec qgepqwat psql -f qwat_v1.3.5_value_list_data_only.sql {config.PGDATABASE} {config.PGUSER}")
        exec_(f"docker exec qgepqwat createdb -U {config.PGUSER} --template={config.PGDATABASE} tpl_empty")

        # Creating the template DB with full data
        exec_(
            f'docker exec qgepqwat psql -U postgres -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE pid<>pg_backend_pid();"'
        )
        exec_(f"docker exec qgepqwat dropdb -U {config.PGUSER} {config.PGDATABASE}")
        exec_(f"docker exec qgepqwat createdb -U {config.PGUSER} {config.PGDATABASE}")
        exec_(
            f"docker exec qgepqwat pg_restore -U {config.PGUSER} --dbname {config.PGDATABASE} --verbose --no-privileges --exit-on-error qgep_1.5.4_structure_and_demo_data.backup"
        )
        exec_(
            f"docker exec qgepqwat pg_restore -U {config.PGUSER} --dbname {config.PGDATABASE} --verbose --no-privileges --exit-on-error qwat_v1.3.5_data_and_structure_sample.backup"
        )
        exec_(f"docker exec qgepqwat createdb -U {config.PGUSER} --template={config.PGDATABASE} tpl_full")

        # Creating the template DB with subset data
        connection = psycopg2.connect(
            f"host={config.PGHOST} dbname={config.PGDATABASE} user={config.PGUSER} password={config.PGPASS}"
        )
        connection.set_session(autocommit=True)
        cursor = connection.cursor()
        for schema in ["qgep_od", "qwat_od"]:
            cursor.execute("SELECT qgep_sys.drop_symbology_triggers();")
            cursor.execute(
                f"""SELECT c.table_name, c.column_name
                            FROM information_schema.columns c
                            JOIN information_schema.tables t ON t.table_schema = c.table_schema AND t.table_name = c.table_name AND t.table_type = 'BASE TABLE'
                            JOIN pg_type typ ON c.udt_name = typ.typname
                            WHERE c.table_schema = '{schema}' AND typname = 'geometry';"""
            )
            for row in cursor.fetchall():
                table, column = row
                print(f"KEEPING ONLY A SUBSET OF {schema}.{table} (this can take a while)...")
                print(
                    f"DELETE FROM {schema}.{table} WHERE ({column} && ST_MakeEnvelope(2750260.6, 1264318.8, 2750335.0,1264367.7, 2056)) = FALSE;"
                )
                try:
                    cursor.execute(
                        f"DELETE FROM {schema}.{table} WHERE ({column} && ST_MakeEnvelope(2750260.6, 1264318.8, 2750335.0,1264367.7, 2056)) = FALSE;"
                    )
                except psycopg2.errors.ForeignKeyViolation as e:
                    print(f"Exception {e} !! we still continue...")
                    pass
            if schema == 'qgep_od':
                # We delete orphaned wastewater_structure
                cursor.execute("DELETE FROM qgep_od.wastewater_structure WHERE fk_main_wastewater_node IS NULL;")
            cursor.execute("SELECT qgep_sys.create_symbology_triggers();")
        exec_(
            f'docker exec qgepqwat psql -U postgres -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE pid<>pg_backend_pid();"'
        )
        exec_(f"docker exec qgepqwat createdb -U {config.PGUSER} --template={config.PGDATABASE} tpl_subset")

        # # add our QWAT migrations
        # exec_(r'docker cp C:\Users\Olivier\Code\QWAT\data-model\update\delta\delta_1.3.6_add_vl_for_SIA_export.sql qgepqwatbuilder:/delta_1.3.6_add_vl_for_SIA_export.sql')
        # exec_(f'docker exec qgepqwatbuilder psql -U postgres -d qgep_prod -f /delta_1.3.6_add_vl_for_SIA_export.sql')

    exec_(
        f'docker exec qgepqwat psql -U postgres -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE pid<>pg_backend_pid();"'
    )
    exec_(f"docker exec qgepqwat dropdb -U {config.PGUSER} {config.PGDATABASE}")
    exec_(f"docker exec qgepqwat createdb -U {config.PGUSER} --template=tpl_{template} {config.PGDATABASE}")


def capfirst(s):
    return s[0].upper() + s[1:]


def invert_dict(d):
    return {v: k for k, v in d.items()}

