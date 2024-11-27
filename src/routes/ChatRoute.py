from flask import Blueprint, jsonify, request
from src.models.ChatModel import ChatModel

main = Blueprint('chat_blueprint', __name__)

chatModel = ChatModel()

@main.route('/chat', methods = ['POST'])
def chat():
    try:
        message = request.json['message']
        response = chatModel.get_response(message)

        return jsonify({'response': response})
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500