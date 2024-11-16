from flask import Blueprint, jsonify, request
from src.models.InterestModel import InterestModel

main = Blueprint('interest_blueprint', __name__)

@main.route('/list', methods = ['GET'])
def interest_list():
    try:
        interest = InterestModel.get_all()
        return jsonify(interest)
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    
@main.route('/clean_list', methods=['DELETE'])
def clean_interest_list():
    try:
        pass
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    
@main.route('/update', methods = ['POST'])
def update_interest():
    try:
        profile_id = request.json['profile_id']
        interest_list = request.json['interest']

        values = []
        if len(interest_list) > 0:
            for interest_value in interest_list:
                values.append((profile_id, interest_value))
            InterestModel.add_interests(values)

        return jsonify({'success': values})
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500

@main.route('/<profile_id>', methods = ['GET'])
def get_interest(profile_id):
    try:
        interest_profile = InterestModel.get_interests(profile_id)
        return interest_profile
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    
@main.route('/<profile_id>', methods = ['DELETE'])
def clean_interest(profile_id):
    try:
        InterestModel.clean_interests(profile_id)

        return jsonify({'success': "OK"})
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500