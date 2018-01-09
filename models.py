from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, BOOLEAN
from sqlalchemy.orm import relationship
from CatalogApp.database import Base
import datetime


class User(Base):
    """
    User class store user information you can also get catalogs and items
    created by particular user
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(120), unique=True)
    password = Column(String(80), nullable=True)
    password_setup = Column(BOOLEAN, nullable=False)
    catalogs = relationship('Catalog')
    items = relationship('Item')

    def __init__(self, name=None, email=None, password=None, password_setup=False):
        self.name = name
        self.email = email
        self.password = password
        self.password_setup = password_setup

    def __repr__(self):
        return '<Catalog {}>'.format(self.name)


class Catalog(Base):
    """
    store Catalog name and user_id
    """
    __tablename__ = 'catalogs'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('User', back_populates='catalogs')
    items = relationship('Item', backref='Catalog')

    def __init__(self, name=None, user_id=None):
        self.name = name
        self.user_id = user_id

    def __repr__(self):
        return '<User {}>'.format(self.name)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        item_list = []
        for item in self.items:
            d = {'name': item.name,
                 'description': item.description}
            item_list.append(d)
        return {
            'catalog name': self.name,
            'Items': item_list
        }


class Item(Base):
    """
    Items store Item information
    """
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    slug = Column(String(80), nullable=False, unique=True)
    description = Column(String(500), nullable=False)
    created_date = Column(DateTime, nullable=False)
    catalog_id = Column(Integer, ForeignKey('catalogs.id'), nullable=False)
    catalog = relationship('Catalog', back_populates='items')
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('User', back_populates='items')

    def __init__(self, name=None, slug=None, description=None, catalog_id=None, user_id=None):
        self.name = name
        self.slug = slug
        self.description = description
        self.catalog_id = catalog_id
        self.user_id = user_id
        self.created_date = datetime.datetime.utcnow()

    def __repr__(self):
        return '<User {}>'.format(self.name)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'description': self.description,
            'URL slug': self.slug,
            'catalog': self.catalog.name
        }
