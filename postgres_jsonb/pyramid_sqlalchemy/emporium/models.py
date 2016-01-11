from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    relationship,
    scoped_session,
    sessionmaker,
)

from sqlalchemy import (
    Column,
    Numeric,
    Integer,
    String,
    Unicode,
    ForeignKey,
    Index,
)

from sqlalchemy.dialects.postgresql.json import JSONB

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class Supplier(Base):
    __tablename__ = 'suppliers'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(50), nullable=False)
    tax_id = Column(String(10), nullable=False)
    bargains = relationship("Bargain", backref='supplier')


class Bargain(Base):
    __tablename__ = 'bargains'
    id = Column(Integer, primary_key=True)
    sku = Column(String(20), nullable=False)
    price = Column(Numeric, nullable=False)
    supplier_id = Column(Integer, ForeignKey('suppliers.id'), nullable=False,
                         index=True)
    info = Column(JSONB)

    @property
    def description(self):
        return self.info.get('description', '')

    @property
    def sale_price(self):
        return self.info.get('sale_price', '')

    @property
    def acquire_cost(self):
        return self.info.get('acquire_cost', '')

    @property
    def color(self):
        return self.info.get('color', '')

# GIN operator class used to create index
Index('ix_bargains_info', Bargain.info, postgresql_using='gin')
