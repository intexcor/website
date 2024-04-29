import flask

from . import db_session
from flask import jsonify, make_response, request
from .products import Product


blueprint = flask.Blueprint(
    'products_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/products')
def get_products():
    db_sess = db_session.create_session()
    prods = db_sess.query(Product).all()
    return jsonify(
        {
            'products':
                [item.to_dict(only=('name', 'description', 'price'))
                 for item in prods]
        }
    )


@blueprint.route('/api/products/<int:prod_id>', methods=['GET'])
def get_s_prod(prod_id):
    db_sess = db_session.create_session()
    prods = db_sess.query(Product).get(prod_id)
    if not prods:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(
        {
            'products': prods.to_dict(only=(
                'name', 'description', 'price'))
        }
    )