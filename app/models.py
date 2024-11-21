from flask_security import UserMixin, RoleMixin, AsaList
from sqlalchemy.orm import relationship, backref
from flask_security.models import fsqla_v3 as fsqla
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import Boolean, DateTime, Column, Integer, \
                    String, ForeignKey, UnicodeText

from . import  db #app, db

fsqla.FsModels.set_db_info(db)

class Role(db.Model, RoleMixin): #fsqla.FsRoleMixin):
    __tablename__ = 'role'
    id              = db.Column(db.Integer(), primary_key=True)
    name            = db.Column(db.String(80), unique=True)
    description     = db.Column(db.String(255))
    permissions     = Column(UnicodeText)#db.Column(MutableList.as_mutable(AsaList()), nullable=True)

class User(db.Model, UserMixin): #fsqla.FsUserMixin):
    __tablename__ = 'user'
    id              = db.Column(db.Integer, primary_key=True)
    email           = db.Column(db.String(255), unique=True)
    username        = db.Column(db.String(255), unique=True, nullable=True)
    password        = db.Column(db.String(255), nullable=False)
    last_login_at   = db.Column(db.DateTime())
    current_login_at    = db.Column(db.DateTime())
    last_login_ip       = db.Column(db.String(100))
    current_login_ip    = db.Column(db.String(100))
    login_count         = db.Column(db.Integer)
    active              = db.Column(db.Boolean())
    is_valid_client     = db.Column(db.Boolean())
    fs_uniquifier       = db.Column(db.String(64), unique=True, nullable=False)
    confirmed_at        = db.Column(db.DateTime())
    roles               = relationship('Role', secondary='roles_users',
                         backref=backref('users', lazy='dynamic'))
    
    