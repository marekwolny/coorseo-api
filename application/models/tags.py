from flask_marshmallow.fields import Hyperlinks, URLFor
from marshmallow import fields, Schema
from sqlalchemy import create_engine, Column, Integer, String, DateTime, \
    ForeignKey, func, Boolean, JSON
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID

from passlib.hash import sha256_crypt
import uuid


from application.shared.models import db_session, model, engine


class Tags(model):
    query = db_session.query_property()

    __tablename__ = 'tags'

    id = Column('tag_id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    name = Column(String(200), unique=True, nullable=False)
    description = Column(String(2000), nullable=True)

    created_on = Column(DateTime, server_default=func.now())
    updated_on = Column(DateTime, server_default=func.now(), server_onupdate=func.now())

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    def to_json(self):
        return dict(name=self.name, description=self.description)

    def __eq__(self, other):
        return type(self) is type(other) and self.id == other.id

    def __ne__(self, other):
        return not self.__eq__(other)