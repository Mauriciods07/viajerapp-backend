import bcrypt
from flask import Blueprint, jsonify, request
from src.models.UserModel import UsersModel
from src.models.entities.multimedia import Multimedia
from src.models.MultimediaModel import MultimediaModel
import uuid
from decouple import config
from src.utils.AmazonS3 import \
                            upload_file_to_s3, \
                            delete_file_from_s3

main = Blueprint('user_blueprint', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def hash_password(password):
    # Generar un salt aleatorio y hashear la contraseña con el salt
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

@main.route('/update',  methods = ['PATCH'])
def update_users_data():
    try:
        profile_id = request.form['profile_id']
        email = request.form['email']

        if 'profile_photo' in request.files:
            file = request.files['profile_photo']
            if file and allowed_file(file.filename):
                multimedia = MultimediaModel.get_multimedia(profile_id, 'PROFILE')
                if len(multimedia) != 0:
                    for archive in multimedia:
                        file_name = archive['archive_url'].split("/")[-1]
                        delete_file_from_s3(file_name)
                    MultimediaModel.delete_multimedia(profile_id, 'PROFILE')
                new_name = uuid.uuid4().hex + '.' + file.filename.rsplit('.',1)[1].lower()
                upload_file_to_s3(file,new_name)
                profile_photo = 'https://{}.s3.{}.amazonaws.com/{}'.format(config('AWS_BUCKET_NAME'),config('REGION_NAME'),new_name)
                multimedia = Multimedia(profile_id,profile_id, 'PROFILE', profile_photo, profile_photo.rsplit('.',1)[1].lower())
                MultimediaModel.create_multimedia(multimedia)
                UsersModel.update_data_photo_user(profile_id,email,profile_photo)
                return jsonify({
                    'message': 'OK',
                    'profile_photo': profile_photo
                })
        else:
            UsersModel.update_user(profile_id,email)
            return jsonify({
                'message': 'OK'
            })
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('/<profile_id>', )
def get_user_data(profile_id):
    try:
        user = UsersModel.get_user_data(profile_id)
        return jsonify(user)
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500

@main.route('/password', methods = ['PATCH'])
def update_password():
    try:
        profileId = request.json['profileId']
        pre_password = request.json['password']
        password = hash_password(pre_password)
        affected_row = UsersModel.update_password(password,profileId)
        if affected_row == 1:
            return {
                'message': 'OK'
            }
        else:
            return jsonify({'message': "User not found"}), 500
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500