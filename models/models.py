# -*- coding: utf-8 -*-

from datetime import datetime
from extensions import sqlalchemy as db
from flask_login import UserMixin


model_tags = db.Table(
    'model_tags',
    db.Column('tagged_model_id', db.Integer, db.ForeignKey('tagged_models.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True),
    db.Column('value', db.SmallInteger, nullable=False, default=1)
)


class TaggedModel(db.Model):
    __tablename__ = 'tagged_models'
    id = db.Column(db.Integer, primary_key=True)
    model_type = db.Column(db.String(31), nullable=False, index=True)
    tags = db.relationship('Tag', secondary=model_tags, backref=db.backref('tagged_models', lazy='dynamic'))
    __mapper_args__ = {'polymorphic_on': model_type}


class Article(TaggedModel):
    __tablename__ = 'articles'
    __mapper_args__ = {'polymorphic_identity': 'article'}
    id = db.Column(None, db.ForeignKey('tagged_models.id'), primary_key=True)
    slug = db.Column(db.String(255), nullable=False, unique=True, index=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(255), nullable=False)
    creation_date = db.Column(db.DateTime, default=datetime.now)


class Project(TaggedModel):
    __tablename__ = 'projects'
    __mapper_args__ = {'polymorphic_identity': 'project'}
    id = db.Column(None, db.ForeignKey('tagged_models.id'), primary_key=True)
    slug = db.Column(db.String(63), unique=True, nullable=False, index=True)
    priority = db.Column(db.Integer, default=0)
    name = db.Column(db.String(63), nullable=False)
    url = db.Column(db.String(255))
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(255), nullable=False)


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(63), nullable=False, unique=True, index=True)
    password = db.Column(db.String(255), nullable=False)
    salt = db.Column(db.String(255), nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)


class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(63), nullable=False, unique=True, index=True)
    name = db.Column(db.String(63), nullable=False)
    image = db.Column(db.String(255), nullable=False)
