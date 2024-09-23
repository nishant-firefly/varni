# D:\workspace\varni\lcnc_ashma\lcnc_ashma\models.py

from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, create_engine, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

# Create a declarative base instance
Base = declarative_base()

# Association table for many-to-many relationship between Role and User
role_user_mapping = Table(
    'role_user_mapping', Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id', ondelete='CASCADE')),
    Column('role_id', Integer, ForeignKey('role.id', ondelete='CASCADE'))
)

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    is_email_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    # Many-to-many relationship with Role
    roles = relationship('Role', secondary=role_user_mapping, back_populates='users')

class Role(Base):
    __tablename__ = 'role'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)

    # Many-to-many relationship with User
    users = relationship('User', secondary=role_user_mapping, back_populates='roles')

class Company(Base):
    __tablename__ = 'company'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    code = Column(String(50), nullable=True)
    address = Column(Text, nullable=True)
    contact_number = Column(String(20), nullable=True)
    contact_email = Column(String(100), nullable=True)

class Entity(Base):
    __tablename__ = 'entity'

    id = Column(Integer, primary_key=True, autoincrement=True)
    entity_label = Column(String(100), nullable=False)
    url = Column(String(100), nullable=False)
    dashboard_url = Column(String(100), nullable=True)

class EntityRolePermission(Base):
    __tablename__ = 'entity_role_permission'

    id = Column(Integer, primary_key=True, autoincrement=True)
    role_id = Column(Integer, ForeignKey('role.id', ondelete='CASCADE'))
    entity_id = Column(Integer, ForeignKey('entity.id', ondelete='CASCADE'))
    create = Column(Boolean, default=False)
    read = Column(Boolean, default=False)
    update = Column(Boolean, default=False)
    delete = Column(Boolean, default=False)

    # Relationships with Role and Entity
    role = relationship('Role', backref='entity_permissions')
    entity = relationship('Entity', backref='role_permissions')

# Create an engine and bind it to the Base
engine = create_engine('postgresql://nishant:nishant@localhost/lcnc_ashma')

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
