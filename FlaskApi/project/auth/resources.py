import logging
from flask import jsonify, Blueprint, request
from flask_jwt_extended import (create_access_token, jwt_required, get_raw_jwt)
from . import models
import csv

logger = logging.getLogger(__name__)

# Registering blueprint of this module
bp = Blueprint("user", __name__, url_prefix="/api/v1")
access_token_key = "access_token"
message = 'message'
status_code = 'status code'


@bp.route("/signup", methods=['POST'])
def signup():
    data = request.get_json()
    user = models.UserModel.query.filter_by(username=data.get('username')).first()
    if user:
        return jsonify({message: 'User {} already exists'.format(data.get('username'))}), 200

    else:
        new_user = models.UserModel(
            username=data.get('username'),
            password=models.UserModel.generate_hash(data.get('password')),
            name=data.get('name'),
            surname=data.get('surname'),
            email=data.get('email'),
        )

        try:
            new_user.add()
            access_token = create_access_token(identity=data.get('username'))
            return jsonify({
                message: 'User {} was created'.format(data.get('username')),
                access_token_key: access_token}), 200
        except Exception as e:
            logger.error("Error in signup(): {}".format(e))
            return jsonify({message: 'Something went wrong'}), 500

@bp.route("/signin", methods=['POST'])
def signin():
    data = request.get_json()
    current_user = models.UserModel.query.filter_by(username=data.get('username')).first()

    if not current_user:
        return jsonify({message: 'User {} doesn\'t exist'.format(data.get('username'))}), 404

    if (data.get("username")==current_user.username or data.get("email")==current_user.email) and models.UserModel.verify_hash(data.get('password'), current_user.password):
        access_token = create_access_token(identity=data.get('username'))
        return jsonify({
            message: 'Logged in as {}'.format(current_user.username),
            access_token_key: access_token}),200

    else:
        return jsonify({'message': 'Wrong credentials'}), 401

@bp.route("/logout", methods=['POST'])
@jwt_required
def signout():
    jti = get_raw_jwt()['jti']
    try:
        revoked_token = models.RevokedTokenModel(jti=jti)
        revoked_token.add()
        return jsonify({message: 'Access token has been revoked'}), 200
    except Exception as e:
        logger.error("Error in logout(): {}".format(e))
        return jsonify({message: 'Something went wrong: {}'.format(e)}), 500

@bp.route("/upload", methods=['POST'])
@jwt_required
def UploadCSVFile():
    data = request.get_json()
    csv_file = data.get("csv_file")
    with open(csv_file) as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')  # todo es más sencillo con pandas.
        for row in csv_reader:
            username, password, name, surname, email = row
            user = models.UserModel(username=username, password=password, name=name, surname=surname, email=email)
            if models.UserModel.query.filter_by(username=username).first():
                return jsonify({message: 'User {} already exists'.format(username)}), 200

            else:

                try:
                    user.add()
                    access_token = create_access_token(identity=username)
                    return jsonify({
                        message: 'User {} was created'.format(username),
                        access_token_key: access_token}), 200

                except Exception as e:
                    logger.error("Error in uploadCSVFile(): {}".format(e))
                    return jsonify({message: 'Something went wrong: {}'.format(e)}), 500