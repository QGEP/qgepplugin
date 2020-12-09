"""
SET PATH=%PATH%;C:\OSGeo4W64\bin
"""

import psycopg2
import os
import sys
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from datetime import datetime, timedelta
from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey, MetaData
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import sessionmaker


PGHOST = '127.0.0.1'
PGDATABASE = 'qgep_prod'
PGUSER = 'postgres'
PGPASS = 'postgres'
PSQL = r'C:\OSGeo4W64\bin\psql'
ILI_MODEL = r'C:\Users\Olivier\Code\QGEP\qgepplugin\qgepplugin\sql\export\interlis\ili\SIA405_Abwasser_2015_2_d-20180417.ili'
ILI2PG = r'C:\Users\Olivier\Code\QGEP\qgepplugin\qgepplugin\sql\ili2pg-3.12.2\ili2pg-3.12.2.jar'
TEMP_SCHEMA = 'vsa_dss_2015_2_d'
SCRIPTS = [
    r'C:\Users\Olivier\Code\QGEP\qgepplugin\qgepplugin\sql\export\interlis\01_vsa_dss_2015_2_d_tid_generate.sql',
    r'C:\Users\Olivier\Code\QGEP\qgepplugin\qgepplugin\sql\export\interlis\02_vsa_dss_2015_2_d_tid_lookup.sql',
    r'C:\Users\Olivier\Code\QGEP\qgepplugin\qgepplugin\sql\export\interlis\021_vsa_dss_2015_2_d_create_seq_ili2db.sql',
    r'C:\Users\Olivier\Code\QGEP\qgepplugin\qgepplugin\sql\export\interlis\022_vsa_dss_2015_2_d_basket_update.sql',
    r'C:\Users\Olivier\Code\QGEP\qgepplugin\qgepplugin\sql\export\interlis\046_vsa_dss_2015_2_d_t_key_object_insert_metadata.sql',
    r'C:\Users\Olivier\Code\QGEP\qgepplugin\qgepplugin\sql\export\interlis\051_vsa_dss_2015_2_d_interlisexport2.sql',
    # r'C:\Users\Olivier\Code\QGEP\qgepplugin\qgepplugin\sql\export\interlis\052a_vsa_dss_2015_2_d_interlisexport2.sql',
]

print("CONNECTING TO DATABASE...")
connection = psycopg2.connect(f"host={PGHOST} dbname={PGDATABASE} user={PGUSER} password={PGPASS}")
connection.set_session(autocommit=True)
cursor = connection.cursor()

print("CREATING THE SCHEMA...")
cursor.execute(f"DROP SCHEMA IF EXISTS {TEMP_SCHEMA} CASCADE ;")
cursor.execute(f"CREATE SCHEMA {TEMP_SCHEMA};")
connection.commit()

print("CREATE ILIDB...")
os.system(f"java -jar {ILI2PG} --createEnumTxtCol --schemaimport --importTid --sqlEnableNull --createEnumTabs --createFk  --noSmartMapping --dbdatabase {PGDATABASE} --dbschema {TEMP_SCHEMA} --dbusr {PGUSER} --dbpwd {PGPASS}  --log createschema_VSA_DSS_2015_2_d.log {ILI_MODEL}")

print("RUNNING SQLS")
os.environ["PGPASSWORD"] = PGPASS
os.environ["PATH"] += r';C:\OSGeo4W64\bin'
for script in SCRIPTS:
    print(f"Running {script}")
    os.system(f"psql -h {PGHOST} -U {PGUSER} -d {PGDATABASE} -f {script}")
    # contents = open(script, "r").read()
    # line = 0
    # for statement in contents.split(';'):
    #     cursor.execute(statement)
    #     connection.commit()
    #     line += len(statement.splitlines())
    #     print('.', end='')
    # print("done !")
    # cursor.execute(contents)
# connection.commit()