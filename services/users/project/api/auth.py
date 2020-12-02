# services/users/project/api/auth.py

from flask import Blueprint, jsonify, request
from flask_restful import Resource, Api
# from sqlalchemy import exc, or_

from project.api.models import User
from project import db, bcrypt


auth_blueprint = Blueprint('auth', __name__)
api = Api(auth_blueprint)


class Auth(Resource):
    """
    User Registration Resource
    """
    def post(self):
        # get the post data
        post_data = request.get_json()
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        if not post_data.get('username'):
            return response_object, 400
        if not post_data.get('email'):
            return response_object, 400
        if not post_data.get('password'):
            return response_object, 400

        # check if user already exists
        user = User.query.filter_by(email=post_data.get('email')).first()
        un = User.query.filter_by(username=post_data.get('username')).first()
        if not user and not un:
            try:
                user = User(
                    username=post_data.get('username'),
                    email=post_data.get('email'),
                    password=post_data.get('password')
                )
                # insert the user
                db.session.add(user)
                db.session.commit()
                # generate the auth token
                auth_token = user.encode_auth_token(user.id)
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully registered.',
                    'auth_token': auth_token.decode()
                }
                return responseObject, 201
            except ValueError:
                responseObject = {
                    'status': 'fail',
                    'message': 'Some error occurred. Please try again.'
                }
                return responseObject, 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'Sorry. That user already exists.',
            }
            return responseObject, 400


@auth_blueprint.route('/auth/login', methods=['POST'])
def login_user():
    # get post data
    post_data = request.get_json()
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload.'
    }
    if not post_data:
        return jsonify(response_object), 400
    email = post_data.get('email')
    password = post_data.get('password')
    try:
        # fetch the user data
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            auth_token = user.encode_auth_token(user.id)
            if auth_token:
                response_object['status'] = 'success'
                response_object['message'] = 'Successfully logged in.'
                response_object['auth_token'] = auth_token.decode()
                return jsonify(response_object), 200
        else:
            response_object['message'] = 'User does not exist.'
            return jsonify(response_object), 404
    except Exception:
        response_object['message'] = 'Try again.'
        return jsonify(response_object), 500


@auth_blueprint.route('/auth/logout', methods=['GET'])
def logout_user():
    # get auth token
    auth_header = request.headers.get('Authorization')
    response_object = {
        'status': 'fail',
        'message': 'Provide a valid auth token.'
    }
    if auth_header:
        auth_token = auth_header.split(' ')[1]
        resp = User.decode_auth_token(auth_token)
        if not isinstance(resp, str):
            response_object['status'] = 'success'
            response_object['message'] = 'Successfully logged out.'
            return jsonify(response_object), 200
        else:
            response_object['message'] = resp
            return jsonify(response_object), 401
    else:
        return jsonify(response_object), 403


@auth_blueprint.route('/auth/status', methods=['GET'])
def get_user_status():
    # get auth token
    auth_header = request.headers.get('Authorization')
    response_object = {
        'status': 'fail',
        'message': 'Provide a valid auth token.'
    }
    if auth_header:
        auth_token = auth_header.split(' ')[1]
        resp = User.decode_auth_token(auth_token)
        if not isinstance(resp, str):
            user = User.query.filter_by(id=resp).first()
            response_object['status'] = 'success'
            response_object['message'] = 'Success.'
            response_object['data'] = user.to_json()
            return jsonify(response_object), 200
        response_object['message'] = resp
        return jsonify(response_object), 401
    else:
        return jsonify(response_object), 401


api.add_resource(Auth, '/auth/register')
