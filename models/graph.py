from exts import db
from datetime import datetime
from sqlalchemy_serializer import SerializerMixin

class Graph(db.Model, SerializerMixin):
    __tablename__ = 'graph'
    graphid = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    graphname = db.Column(db.String(50), nullable=False)
    graphdescription = db.Column(db.String(200), nullable=False)
    entitycount = db.Column(db.Integer, nullable=False)
    linkcount = db.Column(db.Integer, nullable=False)
    eventcount = db.Column(db.Integer, nullable=False)
    updatatime = db.Column(db.DateTime, default=datetime.now)

class GraphCount(db.Model, SerializerMixin):
    __tablename__ = 'graphcount'
    gpid = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    gpcount = db.Column(db.Integer, nullable=False)
    entitycount = db.Column(db.Integer, nullable=False)
    linkcount = db.Column(db.Integer, nullable=False)
    eventcount = db.Column(db.Integer, nullable=False)
    updatatime = db.Column(db.DateTime, default=datetime.now)

class DataSet(db.Model, SerializerMixin):

    __tablename__ = 'dataset'
    dataid = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    dataname = db.Column(db.String(20), nullable=False)
    datadescription = db.Column(db.String(200), nullable=False)
    createtime = db.Column(db.DateTime, default=datetime.now)
    datacount = db.Column(db.Integer, nullable=False)
    userid = db.Column(db.Integer, db.ForeignKey('user.userid'))

    author = db.relationship("User", backref=db.backref("datasets"))
