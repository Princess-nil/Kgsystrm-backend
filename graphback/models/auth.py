from exts import db
from datetime import datetime
from sqlalchemy_serializer import SerializerMixin

class User(db.Model, SerializerMixin):
    serialize_only = ("userid", "username")
    __tablename__ = 'user'
    userid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False)
    userpwd = db.Column(db.String(50), nullable=False)

