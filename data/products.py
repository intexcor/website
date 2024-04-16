import datetime
import sqlalchemy
from flask_wtf.file import FileAllowed, FileField
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
prod = orm.relationship("Products", back_populates='user')


class Product(SqlAlchemyBase):
    __tablename__ = 'products'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    img_prod = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    price = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)


