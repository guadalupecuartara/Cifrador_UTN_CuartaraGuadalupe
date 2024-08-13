from dataclasses import dataclass
from typing import List
from app import db
from app.models.audit_mixin import AuditMixin
from app.models.relations import users_roles
from app.models.soft_delete import SoftDeleteMixin
from .user_data import UserData

@dataclass(init=False, repr=True, eq=True)
class User(SoftDeleteMixin, AuditMixin, db.Model):
    __tablename__ = 'users'
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username: str = db.Column(db.String(80), unique=True, nullable=False)
    password: str = db.Column('password', db.String(255), nullable=False)
    email: str = db.Column(db.String(120), unique=True, nullable=False) 
    role_id: int = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=True)
    #Relacion Uno a Uno bidireccional con UserData
    data = db.relationship('UserData', uselist=False, back_populates='user', cascade="all, delete-orphan") # type: ignore

    #Relacion Muchos a Muchos bidireccional con Role
    #Flask Web Development Capitulo: Database Relationships Revisited Pag 49,149 
    roles = db.relationship("Role", secondary=users_roles, back_populates='users')

    # * Relación con la tabla 'Text' (texto), establecida a través de la propiedad 'user' en la clase Text
    users_rs = db.relationship("Text", backref="user", lazy=True)
    # * Relación con la tabla 'UserData' (datos de usuario), establecida a través de la propiedad 'user' en la clase UserData

    ##########esto andaba a las 2:36
    #def __init__(self, username, password, email, user_data: UserData = None):
     #   self.username = username
      #  self.password = password
       # self.email = email
        #self.data = user_data

    def __init__(self, username: str = None, password: str = None, email: str = None, data: UserData = None):
        self.data = data
        self.username = username
        self.password = password
        self.email = email
    
    #TODO: Implementar metodos para agregar, eliminar y listar roles
    def add_role(self, role):
        if role not in self.roles:
            self.roles.append(role)

    def remove_role(self, role):
        if role in self.roles:
            self.roles.remove(role)