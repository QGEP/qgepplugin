from .automap_base import AutomapBase
from . import Base_f


# ABSTRACT !
class SIA405_BaseClass(Base_f.BaseClass):  # SIA405_BaseClass(Base.BaseClass)
    __tablename__ = 'sia405_baseclass'
    __table_args__ = {'schema': 'pg2ili_wasser'}

# ABSTRACT !
class SIA405_TextePos(Base_f.TextePos):  # SIA405_TextPos(Base.TextPos)
    __tablename__ = 'sia405_textepos'
    __table_args__ = {'schema': 'pg2ili_wasser'}

# ABSTRACT !
class SIA405_SymbolePos(Base_f.SymbolePos):  # SIA405_SymbolPos(Base.SymbolPos)
    __tablename__ = 'sia405_symbolepos'
    __table_args__ = {'schema': 'pg2ili_wasser'}

