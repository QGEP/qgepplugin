from .automap_base import AutomapBase


# ABSTRACT !
class BaseClass(AutomapBase):  # BaseClass(AutomapBase)
    __tablename__ = 'baseclass'
    __table_args__ = {'schema': 'pg2ili_wasser'}

# ABSTRACT !
class TextePos(BaseClass):  # TextPos(BaseClass)
    __tablename__ = 'textepos'
    __table_args__ = {'schema': 'pg2ili_wasser'}

# ABSTRACT !
class SymbolePos(BaseClass):  # SymbolPos(BaseClass)
    __tablename__ = 'symbolepos'
    __table_args__ = {'schema': 'pg2ili_wasser'}

