from .automap_base import AutomapBase
from . import Base_f_LV95


# ABSTRACT !
class SIA405_BaseClass(Base_f_LV95.BaseClass):  # SIA405_BaseClass(Base_LV95.BaseClass)
    __tablename__ = 'sia405_baseclass'
    __table_args__ = {'schema': 'pg2ili_wasser'}

# ABSTRACT !
class SIA405_TextePos(Base_f_LV95.TextePos):  # SIA405_TextPos(Base_LV95.TextPos)
    __tablename__ = 'sia405_textepos'
    __table_args__ = {'schema': 'pg2ili_wasser'}

# ABSTRACT !
class SIA405_SymbolePos(Base_f_LV95.SymbolePos):  # SIA405_SymbolPos(Base_LV95.SymbolPos)
    __tablename__ = 'sia405_symbolepos'
    __table_args__ = {'schema': 'pg2ili_wasser'}

