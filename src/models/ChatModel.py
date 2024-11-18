from src.algorithms.chatbot.process_message import ProcessMessage
import numpy
import random
import keras
import json

class ChatModel:
    def __init__(self) -> None:
        self.model = keras.models.load_model('src/resources/models/viajerapp_chatbot_model.keras')

        with open('src/resources/files/intents_viajerapp.json', encoding='utf-8') as file:
            data = json.load(file)

        labels = []
        texts = []
        for intent in data['intents']:
            for pattern in intent['patterns']:
                texts.append(pattern)  

            if intent['tag'] not in labels:
                labels.append(intent['tag'])

        self.data = data
        self.labels = labels
        self.process_message = ProcessMessage(texts)

    def get_response(self, message: str) -> str:
        msg_instance = self.process_message.instancer(message)
        results = self.model.predict(msg_instance)
        results_index = numpy.argmax(results)
        tag = self.labels[results_index]
        maxscore = numpy.max(results)

        for tg in self.data["intents"]:
            if tg['tag'] == tag:
                responses = tg['responses']

        weak = self.process_message.get_weak_grammars(message)

        if maxscore > 0.5:
            return random.choice(responses)
        else:
            if weak[1] == 0:
                return '\nLo siento, pero no comprendí, ¿Me puedes preguntar de otra forma?\n'
            
            return weak[0]