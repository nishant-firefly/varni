from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Department(Base):
    __tablename__ = 'departments'
    department_id = Column(Integer, primary_key=True)
    department_name = Column(String(255), nullable=False)
    parent_department_id = Column(Integer, ForeignKey('departments.department_id'), nullable=True)
    children = relationship("Department", backref='parent', remote_side=[department_id])

class Role(Base):
    __tablename__ = 'roles'
    role_id = Column(Integer, primary_key=True)
    role_name = Column(String(255), nullable=False, unique=True)

class Entity(Base):
    __tablename__ = 'entities'
    entity_id = Column(Integer, primary_key=True)
    entity_name = Column(String(255), nullable=False, unique=True)

class ColumnDefinition(Base):
    __tablename__ = 'columns'
    column_id = Column(Integer, primary_key=True)
    entity_id = Column(Integer, ForeignKey('entities.entity_id'), nullable=False)
    column_name = Column(String(255), nullable=False)
    data_type = Column(String(50), nullable=False)
    size = Column(Integer, nullable=True)
    is_primary_key = Column(Boolean, default=False)
    is_unique = Column(Boolean, default=False)
    is_nullable = Column(Boolean, default=True)

class ForeignKeyDefinition(Base):
    __tablename__ = 'foreign_keys'
    foreign_key_id = Column(Integer, primary_key=True)
    column_id = Column(Integer, ForeignKey('columns.column_id'), nullable=False)
    referenced_entity_id = Column(Integer, ForeignKey('entities.entity_id'), nullable=False)
    referenced_column_id = Column(Integer, ForeignKey('columns.column_id'), nullable=False)

class DepartmentRole(Base):
    __tablename__ = 'department_role'
    department_role_id = Column(Integer, primary_key=True)
    department_id = Column(Integer, ForeignKey('departments.department_id'), nullable=False)
    role_id = Column(Integer, ForeignKey('roles.role_id'), nullable=False)

class Permission(Base):
    __tablename__ = 'permissions'
    permission_id = Column(Integer, primary_key=True)
    department_role_id = Column(Integer, ForeignKey('department_role.department_role_id'), nullable=False)
    entity_id = Column(Integer, ForeignKey('entities.entity_id'), nullable=False)
    can_create = Column(Boolean, default=False)
    can_read = Column(Boolean, default=True)
    can_update = Column(Boolean, default=False)
    can_delete = Column(Boolean, default=False)

class EntityRelationship(Base):
    __tablename__ = 'entity_relationships'
    relationship_id = Column(Integer, primary_key=True)
    entity_id = Column(Integer, ForeignKey('entities.entity_id'), nullable=False)
    related_entity_id = Column(Integer, ForeignKey('entities.entity_id'), nullable=False)
    relationship_type = Column(String(50), nullable=False)
