from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from datetime import datetime, timedelta
from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey, MetaData
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import sessionmaker



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

engine = create_engine('postgresql://postgres:postgres@127.0.0.1:5432/qgep_prod')
meta = MetaData()
meta.reflect(bind=engine, schema='qgep_od', views=True)

cover = meta.tables['qgep_od.cover']
q = cover.insert().values(diameter=22)

Session = sessionmaker(bind=engine)
session = Session()
session.execute(q)
session.commit()

print(q)
