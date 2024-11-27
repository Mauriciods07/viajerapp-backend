from flask import Blueprint, jsonify
from src.models.ProfileModel import ProfileModel
from src.models.InterestModel import InterestModel

main = Blueprint('profile_blueprint', __name__)


@main.route('/<profile_id>', methods=['GET'])
def get_user_data(profile_id):
    try:
        profile = ProfileModel.get_profile_data(profile_id)
        interests = InterestModel.get_unique_interests(profile_id)
        

        API_URL_TEMPLATE = "https://flagsapi.com/{}/shiny/64.png"

        interests_uniques = []
        for interest in interests:
            url_flag = API_URL_TEMPLATE.format(interest['code_iso2'])
            interest['flag'] = url_flag
            stored_countries = [x['country'] for x in interests_uniques]
            if interest['country'] not in stored_countries:
                interests_uniques.append(interest)

        return jsonify({
            'name': profile['name'],
            'email': profile['email'],
            'profile_photo': profile['profile_photo'],
            'interests': interests_uniques
        })
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500