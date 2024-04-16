
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Reviews(SqlAlchemyBase):
    __tablename__ = 'reviews'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    img_rew = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    text_rew = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    id_prod = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('products.id'), nullable=False)
    id_user = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), nullable=False)

    user = orm.relationship('User')
    prod = orm.relationship('Product')
