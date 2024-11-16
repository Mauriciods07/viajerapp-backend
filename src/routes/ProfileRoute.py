from flask import Blueprint, jsonify
from src.models.ProfileModel import ProfileModel

main = Blueprint('profile_blueprint', __name__)


@main.route('/<profile_id>', )
def get_user_data(profile_id):
    try:
        profile = ProfileModel.get_profile_data(profile_id)
        return jsonify(profile)
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500