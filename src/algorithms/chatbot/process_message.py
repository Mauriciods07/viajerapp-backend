from src.algorithms.chatbot.get_tokenizer import get_tokenizer
from keras.preprocessing.sequence import pad_sequences
import random

class ProcessMessage:
    def __init__(self, texts):
        
        self.tokenizer = get_tokenizer(texts)
        self.maxlen_user = 5

        Saludos_In = ["Hola", "Holi", "Cómo estás", "Que tal", "Cómo te va"]
        Despedidas_In = ["Adios", "Bye", "Hasta luego", "Nos vemos", "Hasta pronto"]
        Gracias_In = ["gracias", "te agradezco", "te doy las gracias"]
        self.InsD = [Saludos_In, Despedidas_In, Gracias_In]

        Saludos_Out = ["Hola ¿Cómo estás?", "Es un gusto saludarte de nuevo", "Me da gusto verte de nuevo"]
        Despedidas_Out = ["Nos vemos, fue un gusto", "Que te vaya muy bien", "Regresa pronto, adios"]
        Gracias_Out = ["Por nada, es un placer", "Me da mucho gusto poder ayudar", "De nada, para eso estoy"]
        self.OutsD = [Saludos_Out, Despedidas_Out, Gracias_Out]

    def instancer(self, inp):
        inp = inp.lower()
        inp = inp.replace("á", "a")
        inp = inp.replace("é", "e")
        inp = inp.replace("í", "i")
        inp = inp.replace("ó", "o")
        inp = inp.replace("ú", "u")
        inp = inp.replace("¿", "")
        inp = inp.replace("?", "")
        txt = [inp]
        seq = self.tokenizer.texts_to_sequences(txt)
        padded = pad_sequences(seq, maxlen=self.maxlen_user)
        return padded

    def get_weak_grammars(self, inp):
        index = 0
        weak_act = 0
        response = ''

        for categoria in self.InsD:
            for gramatica in categoria:
                if inp.lower().count(gramatica.lower()) > 0:
                    weak_act = 1
                    response = random.choice(self.OutsD[index])
            index += 1

        return (response, weak_act)