from flask_marshmallow.fields import Hyperlinks, URLFor
from flask_marshmallow.sqla import SQLAlchemySchema, auto_field, HyperlinkRelated
from marshmallow import fields, pre_load, Schema
from marshmallow.fields import List
from marshmallow_sqlalchemy import ModelSchema
from marshmallow_sqlalchemy.fields import Nested
from sqlalchemy import create_engine, Column, Integer, String, DateTime, \
    ForeignKey, func
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgresql+psycopg2://user:password@localhost:5432/coorseo',
                       convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))


def init_db():
    Model.metadata.create_all(bind=engine)


Model = declarative_base(name='Model')


class Users(Model):
    query = db_session.query_property()

    __tablename__ = 'users'

    id = Column('user_id', Integer, primary_key=True)

    email = Column(String(200), unique=True, nullable=False)
    name = Column(String(200), unique=True, nullable=False)
    first_name = Column(String(200))
    last_name = Column(String(200))

    def __init__(self, email, name):
        self.email = email
        self.name = name

    def __eq__(self, other):
        return type(self) is type(other) and self.id == other.id

    def __ne__(self, other):
        return not self.__eq__(other)


class UsersSchema(Schema):
    id = fields.Integer()
    email = fields.String()
    name = fields.String()
    first_name = fields.String()
    last_name = fields.String()
    _links = Hyperlinks(
        {"self": URLFor("courses.get", id="<id>"), "collection": URLFor("courses.get_all")}
    )


class Courses(Model):
    query = db_session.query_property()

    __tablename__ = 'courses'

    id = Column('course_id', Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    created_on = Column(DateTime, server_default=func.now())
    updated_on = Column(DateTime, server_default=func.now(), server_onupdate=func.now())

    platform_id = Column(Integer, ForeignKey('platforms.platform_id'), nullable=False)
    platform = relationship("Platforms", backref=backref("courses", lazy="dynamic"))

    publisher_id = Column(Integer, ForeignKey('publishers.publisher_id'), nullable=False)
    publisher = relationship("Publishers", backref=backref("courses", lazy="dynamic"))

    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return type(self) is type(other) and self.id == other.id

    def __ne__(self, other):
        return not self.__eq__(other)


class CoursesSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    created_on = fields.DateTime()
    updated_on = fields.DateTime()
    platform = fields.Nested('PlatformsSchema')
    publisher = fields.Nested('PublishersSchema')
    _links = Hyperlinks(
        {"self": URLFor("courses.get", id="<id>"), "collection": URLFor("courses.get_all")}
    )


class Platforms(Model):
    query = db_session.query_property()

    __tablename__ = 'platforms'

    id = Column('platform_id', Integer, primary_key=True)

    name = Column(String(200), unique=True, nullable=False)
    created_on = Column(DateTime, server_default=func.now())
    updated_on = Column(DateTime, server_default=func.now(), server_onupdate=func.now())

    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return type(self) is type(other) and self.id == other.id

    def __ne__(self, other):
        return not self.__eq__(other)


class PlatformsSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    created_on = fields.DateTime()
    updated_on = fields.DateTime()

    _links = Hyperlinks(
        {"self": URLFor("platforms.get", id="<id>"), "collection": URLFor("platforms.get_all")}
    )


class Publishers(Model):
    query = db_session.query_property()

    __tablename__ = 'publishers'

    id = Column('publisher_id', Integer, primary_key=True)

    name = Column(String(200), unique=True, nullable=False)
    created_on = Column(DateTime, server_default=func.now())
    updated_on = Column(DateTime, server_default=func.now(), server_onupdate=func.now())

    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return type(self) is type(other) and self.id == other.id

    def __ne__(self, other):
        return not self.__eq__(other)


class PublishersSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    created_on = fields.DateTime()
    updated_on = fields.DateTime()

    _links = Hyperlinks(
        {"self": URLFor("publishers.get", id="<id>"), "collection": URLFor("publishers.get_all")}
    )


class Ratings(Model):
    query = db_session.query_property()

    __tablename__ = 'ratings'

    id = Column('rating_id', Integer, primary_key=True)

    points = Column(Integer, nullable=False)
    created_on = Column(DateTime, server_default=func.now())
    updated_on = Column(DateTime, server_default=func.now(), server_onupdate=func.now())

    course_id = Column(Integer, ForeignKey('courses.course_id'), nullable=False)
    course = relationship('Courses', backref='ratings', lazy=True)

    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    user = relationship('Users', backref="ratings", lazy=True)

    def __init__(self, user: Users, points: int):
        self.user = user
        self.points = points

    def to_json(self):
        return dict(name=self.points)

    def __eq__(self, other):
        return type(self) is type(other) and self.id == other.id

    def __ne__(self, other):
        return not self.__eq__(other)


class RatingsSchema(Schema):
    id = fields.Integer()
    points = fields.Integer()
    created_on = fields.DateTime()
    updated_on = fields.DateTime()

    _links = Hyperlinks(
        {"self": URLFor("ratings.get", id="<id>"), "collection": URLFor("ratings.get_all")}
    )


class Reviews(Model):
    query = db_session.query_property()

    __tablename__ = 'reviews'

    id = Column('review_id', Integer, primary_key=True)

    description = Column(String(200), unique=True, nullable=False)
    created_on = Column(DateTime, server_default=func.now())
    updated_on = Column(DateTime, server_default=func.now(), server_onupdate=func.now())

    course_id = Column(Integer, ForeignKey('courses.course_id'), nullable=False)
    course = relationship('Courses', backref='reviews', lazy=True)

    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    user = relationship('Users', backref="reviews", lazy=True)

    def __init__(self, user: Users, description: str):
        self.user = user
        self.description = description

    def to_json(self):
        return dict(name=self.description)

    def __eq__(self, other):
        return type(self) is type(other) and self.id == other.id

    def __ne__(self, other):
        return not self.__eq__(other)


class ReviewsSchema(Schema):
    id = fields.Integer()
    description = fields.String()
    created_on = fields.DateTime()
    updated_on = fields.DateTime()

    _links = Hyperlinks(
        {"self": URLFor("reviews.get", id="<id>"), "collection": URLFor("reviews.get_all")}
    )


if __name__ == '__main__':
    init_db()