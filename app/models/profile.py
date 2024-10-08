from dataclasses import dataclass
from app import db
from app.models.audit_mixin import AuditMixin
from app.models.soft_delete import SoftDeleteMixin


@dataclass(init=False, repr=True, eq=True)
class Profile(SoftDeleteMixin, AuditMixin, db.Model):
    __tablename__ = 'profiles'
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(50), nullable=False)
    updated_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    updated_by = db.relationship('User', foreign_keys=[updated_by_id])
    #Relación Uno a Muchos bidireccional con UserData
    data = db.relationship('UserData', back_populates='profile')