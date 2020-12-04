from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from datetime import datetime, timedelta
from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey, MetaData
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import collections



# # EXAMPLE 1 : simple model

# engine = create_engine('postgresql://postgres:postgres@127.0.0.1:5432/qgep_test_ili')
# Base = declarative_base()

# class ParentTable(Base):
#     __tablename__ = 'parent'
#     id = Column(Integer, primary_key=True)
#     name = Column(String(255), nullable=False)


# class ChildTable(ParentTable):
#     __tablename__ = 'child'
#     id = Column(ForeignKey(ParentTable.id), primary_key=True)
#     surname = Column(String(255), nullable=False)


# class GrandChildTable(ChildTable):
#     __tablename__ = 'grandchild'
#     id = Column(ForeignKey(ChildTable.id), primary_key=True)
#     lastname = Column(String(255), nullable=False)



# EXAMPLE 2 : reflecting existing schema

# engine = create_engine('postgresql://postgres:postgres@127.0.0.1:5432/qgep_test_ili')
# meta = MetaData()
# meta.reflect(bind=engine, schema='testfr')

# TableCouvercle = meta.tables['testfr.couvercle']
# q = TableCouvercle.insert().values(diametre=22)
# print(q)

# EXAMPLE 3 : autoloading existing schema (QGEP)


# qgep_meta = MetaData()
# qgep_meta.reflect(bind=engine, schema='qgep_od', views=True)
# qgep_cover = qgep_meta.tables['qgep_od.cover']

# sia_meta = MetaData()
# sia_meta.reflect(bind=engine, schema='vsa_dss_2015_2_d', views=True)
# sia_cover = sia_meta.tables['vsa_dss_2015_2_d.deckel']

# q = cover.insert().values(diameter=22)
# qgep_session = sessionmaker(bind=engine)()
# qgep_session.execute(q)
# qgep_session.commit()
# print(q)


# TestBase = automap_base()

# class Animals(TestBase):
#     __tablename__ = 'animals'
#     __table_args__ = {'schema' : 'test'}


# class Cats(Animals):
#     __tablename__ = 'cats'
#     __table_args__ = {'schema' : 'test'}


engine = create_engine('postgresql://postgres:postgres@127.0.0.1:5432/qgep_prod')

MAPPING = {
    'wastewater_structure': {
        'accessibility': {
            None: None,
            3444: 'ueberdeckt',
            3447: 'unbekannt',
            3446: 'unzugaenglich',
            3445: 'zugaenglich',
        }
    },
    'manhole': {
        'function': {
            None: None,
            4532: 'Absturzbauwerk',
            5344: 'andere',
            4533: 'Be_Entlueftung',
            3267: 'Dachwasserschacht',
            3266: 'Einlaufschacht',
            3472: 'Entwaesserungsrinne',
            228: 'Geleiseschacht',
            204: 'Kontrollschacht',
            1008: 'Oelabscheider',
            4536: 'Pumpwerk',
            5346: 'Regenueberlauf',
            2742: 'Schlammsammler',
            5347: 'Schwimmstoffabscheider',
            4537: 'Spuelschacht',
            4798: 'Trennbauwerk',
            5345: 'unbekannt',
        },
    },
}

######################################################################
# Example 1 : Plain autoloading (doesn't load inheritance)
# then insert export each table separately, from base to specific
# matching Stefan's script logic
######################################################################


def export_a():

    # Autoload QGEP datamodel
    QGEPBase = automap_base()
    QGEPBase.prepare(engine, reflect=True, schema='qgep_od')

    # Autoload Interlis datamodel
    SIABase = automap_base()
    SIABase.prepare(engine, reflect=True, schema='vsa_dss_2015_2_d')

    # Shortcuts
    QGEP = QGEPBase.classes
    SIA = SIABase.classes

    # Autoincrementing ID
    oid2tid = collections.defaultdict(lambda: len(oid2tid))

    # Actual insert routing
    session = Session(engine, autocommit=True)  # TODO : remove autocommit

    print("Exporting wastewater_networkelement -> baseclass")
    for row in session.query(QGEP.wastewater_networkelement):
        session.add(
            SIA.baseclass(
                t_id=oid2tid[row.obj_id],
                t_type='abwassernetzelement',  # this will be replaced by correct subclass below
                t_ili_tid=row.obj_id,
            )
        )
        print('.', end='')
    print('done !')

    print("Exporting wastewater_networkelement -> sia405_baseclass")
    for row in session.query(QGEP.wastewater_networkelement):
        session.add(
            SIA.sia405_baseclass(
                t_id=oid2tid[row.obj_id],
                obj_id=row.obj_id,
            )
        )
        print('.', end='')
    print('done !')

    print("Exporting wastewater_networkelement -> abwassernetzelement")
    for row in session.query(QGEP.wastewater_networkelement):
        session.add(
            SIA.abwassernetzelement(
                t_id=oid2tid[row.obj_id],
                bezeichnung=row.identifier,
            )
        )
        print('.', end='')
    print('done !')

    print("Exporting wastewater_structure -> baseclass")
    for row in session.query(QGEP.wastewater_structure):
        session.add(
            SIA.baseclass(
                t_id=oid2tid[row.obj_id],
                t_type='abwasserbauwerk',  # this will be replaced by correct subclass below
                t_ili_tid=row.obj_id,
            )
        )
        print('.', end='')
    print('done !')

    print("Exporting wastewater_structure -> sia405_baseclass")
    for row in session.query(QGEP.wastewater_structure):
        session.add(
            SIA.sia405_baseclass(
                t_id=oid2tid[row.obj_id],
                obj_id=row.obj_id,
            )
        )
        print('.', end='')
    print('done !')

    print("Exporting wastewater_structure -> abwasserbauwerk")
    for row in session.query(QGEP.wastewater_structure):
        session.add(
            SIA.abwasserbauwerk(
                t_id=oid2tid[row.obj_id],
                zugaenglichkeit=MAPPING['wastewater_structure']['accessibility'][row.accessibility],
            )
        )
        print('.', end='')
    print('done !')

    print("Exporting manhole -> normschacht")
    for row in session.query(QGEP.manhole):
        session.add(
            SIA.normschacht(
                t_id=oid2tid[row.obj_id],
                dimension1=row.dimension1,
                dimension2=row.dimension2,
                funktion=MAPPING['manhole']['function'][row.function],
            )
        )
        print('.', end='')
    print('done !')

    print("Updating  manhole -> normschacht")
    normschacht_subquery = session.query(SIA.normschacht.t_id)
    session.query(SIA.baseclass).filter(SIA.baseclass.t_id.in_(normschacht_subquery)).update({SIA.baseclass.t_type: "normschacht"}, synchronize_session=False)
    print('done !')


######################################################################
# Example 2 : Plain autoloading (doesn't load inheritance)
# then insert from a joined query, base and specific at once
######################################################################


def export_b():

    # Autoload QGEP datamodel
    QGEPBase = automap_base()
    QGEPBase.prepare(engine, reflect=True, schema='qgep_od')

    # Autoload Interlis datamodel
    SIABase = automap_base()
    SIABase.prepare(engine, reflect=True, schema='vsa_dss_2015_2_d')

    # Shortcuts
    QGEP = QGEPBase.classes
    SIA = SIABase.classes

    # Autoincrementing ID
    oid2tid = collections.defaultdict(lambda: len(oid2tid))

    # Actual insert routing
    session = Session(engine, autocommit=True)  # TODO : remove autocommit

    print("Exporting manhole -> normschacht")
    joined_query = session.query(QGEP.manhole, QGEP.wastewater_structure, QGEP.wastewater_networkelement) \
        .filter(QGEP.manhole.obj_id == QGEP.wastewater_structure.obj_id) \
        .filter(QGEP.wastewater_structure.obj_id == QGEP.wastewater_networkelement.fk_wastewater_structure)
    for row in joined_query:

        # wastewater_networkelement -> baseclass
        session.add(
            SIA.baseclass(
                t_id=oid2tid[row.wastewater_networkelement.obj_id],
                t_type='abwassernetzelement',
                t_ili_tid=row.wastewater_networkelement.obj_id,
            )
        )

        # wastewater_networkelement -> sia405_baseclass
        session.add(
            SIA.sia405_baseclass(
                t_id=oid2tid[row.wastewater_networkelement.obj_id],
                obj_id=row.wastewater_networkelement.obj_id,
            )
        )

        # wastewater_networkelement -> abwassernetzelement
        session.add(
            SIA.abwassernetzelement(
                t_id=oid2tid[row.wastewater_networkelement.obj_id],
                bezeichnung=row.wastewater_networkelement.identifier,
            )
        )

        # manhole -> baseclass
        session.add(
            SIA.baseclass(
                t_id=oid2tid[row.manhole.obj_id],
                t_type='normschacht',
                t_ili_tid=row.manhole.obj_id,
            )
        )

        # manhole -> sia405_baseclass
        session.add(
            SIA.sia405_baseclass(
                t_id=oid2tid[row.manhole.obj_id],
                obj_id=row.manhole.obj_id,
            )
        )

        # wastewater_structure -> abwasserbauwerk
        session.add(
            SIA.abwasserbauwerk(
                t_id=oid2tid[row.wastewater_structure.obj_id],
                zugaenglichkeit=MAPPING['wastewater_structure']['accessibility'][row.wastewater_structure.accessibility],
            )
        )

        # manhole -> normschacht
        session.add(
            SIA.normschacht(
                t_id=oid2tid[row.manhole.obj_id],
                dimension1=row.manhole.dimension1,
                dimension2=row.manhole.dimension2,
                funktion=MAPPING['manhole']['function'][row.manhole.function],
            )
        )
        print('.', end='')

    print('done !')
   
    session.commit()


######################################################################
# Example 3 : Hybrid autoloading (maps inheritance)
# then insert using inheritance !
######################################################################

def export_c():

    # Autoload QGEP datamodel
    QGEPBase = automap_base()

    class WasterwaterNetworkelement(QGEPBase):
        __tablename__ = 'wastewater_networkelement'
        __table_args__ = {'schema': 'qgep_od'}

    class WasterwaterStructure(QGEPBase):
        __tablename__ = 'wastewater_structure'
        __table_args__ = {'schema': 'qgep_od'}

    class Manhole(WasterwaterStructure):
        __tablename__ = 'manhole'
        __table_args__ = {'schema': 'qgep_od'}

    QGEPBase.prepare(engine, reflect=True, schema='qgep_od')

    # Autoload Interlis datamodel
    SIABase = automap_base()

    class BaseClass(SIABase):
        __tablename__ = 'baseclass'
        __table_args__ = {'schema': 'vsa_dss_2015_2_d'}

    class Sia405BaseClass(BaseClass):
        __tablename__ = 'sia405_baseclass'
        __table_args__ = {'schema': 'vsa_dss_2015_2_d'}

    class Abwassernetzelement(Sia405BaseClass):
        __tablename__ = 'abwassernetzelement'
        __table_args__ = {'schema': 'vsa_dss_2015_2_d'}

    class Abwasserbauwerk(Sia405BaseClass):
        __tablename__ = 'abwasserbauwerk'
        __table_args__ = {'schema': 'vsa_dss_2015_2_d'}

    class Normschacht(Abwasserbauwerk):
        __tablename__ = 'normschacht'
        __table_args__ = {'schema': 'vsa_dss_2015_2_d'}

    SIABase.prepare(engine, reflect=True, schema='vsa_dss_2015_2_d')

    # Shortcuts
    QGEP = QGEPBase.classes
    SIA = SIABase.classes
    
    # Autoincrementing ID
    oid2tid = collections.defaultdict(lambda: len(oid2tid))

    # Actual insert routing
    session = Session(engine, autocommit=True)  # TODO : remove autocommit

    print("Exporting WasterwaterNetworkelement -> Abwassernetzelement")
    for row in session.query(QGEP.WasterwaterNetworkelement):

        import pdb
        pdb.set_trace()

        # # wastewater_networkelement -> baseclass        
        # session.add(
        #     SIA.Abwassernetzelement(
        #         t_id=oid2tid[row.wastewater_networkelement.obj_id],
        #         t_type='abwassernetzelement',
        #         t_ili_tid=row.wastewater_networkelement.obj_id,
        #     )
        # )

        # # wastewater_networkelement -> sia405_baseclass
        # session.add(
        #     SIA.sia405_baseclass(
        #         t_id=oid2tid[row.wastewater_networkelement.obj_id],
        #         obj_id=row.wastewater_networkelement.obj_id,
        #     )
        # )

        # # wastewater_networkelement -> abwassernetzelement
        # session.add(
        #     SIA.abwassernetzelement(
        #         t_id=oid2tid[row.wastewater_networkelement.obj_id],
        #         bezeichnung=row.wastewater_networkelement.identifier,
        #     )
        # )

        # # manhole -> baseclass
        # session.add(
        #     SIA.baseclass(
        #         t_id=oid2tid[row.manhole.obj_id],
        #         t_type='normschacht',
        #         t_ili_tid=row.manhole.obj_id,
        #     )
        # )

        # # manhole -> sia405_baseclass
        # session.add(
        #     SIA.sia405_baseclass(
        #         t_id=oid2tid[row.manhole.obj_id],
        #         obj_id=row.manhole.obj_id,
        #     )
        # )

        # # wastewater_structure -> abwasserbauwerk
        # session.add(
        #     SIA.abwasserbauwerk(
        #         t_id=oid2tid[row.wastewater_structure.obj_id],
        #         zugaenglichkeit=MAPPING['wastewater_structure']['accessibility'][row.wastewater_structure.accessibility],
        #     )
        # )

        # # manhole -> normschacht
        # session.add(
        #     SIA.normschacht(
        #         t_id=oid2tid[row.manhole.obj_id],
        #         dimension1=row.manhole.dimension1,
        #         dimension2=row.manhole.dimension2,
        #         funktion=MAPPING['manhole']['function'][row.manhole.function],
        #     )
        # )
        # print('.', end='')

    session.commit()


export_c()