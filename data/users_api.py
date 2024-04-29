import flask

from . import db_session
from .users import User
from flask import jsonify, make_response, request
from werkzeug.security import generate_password_hash

blueprint = flask.Blueprint(
    'users_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/users')
def get_users():
    db_sess = db_session.create_session()
    jobs = db_sess.query(User).all()
    return jsonify(
        {
            'users':
                [item.to_dict(only=('name', 'surname', 'email')) for item in jobs]
        }
    )


@blueprint.route('/api/users/<int:user_id>', methods=['GET'])
def get_s_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(
        {
            'user': user.to_dict(only=('name', 'surname', 'email'))
        }
    )