from dataclasses import dataclass
from app import db
from app.models.audit_mixin import AuditMixin
from app.models.soft_delete import SoftDeleteMixin

@dataclass(init=False, repr=True, eq=True)
class UserData(SoftDeleteMixin, db.Model):
    __tablename__ = 'users_data'
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname: str = db.Column(db.String(80), nullable=False)
    lastname: str = db.Column(db.String(80), nullable=False)
    phone: str = db.Column(db.String(120), nullable=False)
    address: str = db.Column(db.String(120), nullable=False)
    city: str   = db.Column(db.String(120), nullable=False)
    country: str = db.Column(db.String(120), nullable=False)
    # Relación con la tabla 'users' (usuarios), establecida a través de la columna 'user_id'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship(
        "User", back_populates="data", foreign_keys=[user_id], uselist=False
    )
    
    # Relación Muchos a Uno bidireccional con Profile
    profile_id = db.Column(db.Integer, db.ForeignKey("profiles.id"), nullable=True)
    profile = db.relationship(
        "Profile", back_populates="data", foreign_keys=[profile_id]
    )
    
    def __init__(self, firstname: str = None, lastname: str = None, phone: str = None, address: str = None, city: str = None, country: str = None, profile = None):
        self.firstname = firstname
        self.lastname = lastname
        self.phone = phone
        self.address = address
        self.city = city
        self.country = country
        self.profile = profile