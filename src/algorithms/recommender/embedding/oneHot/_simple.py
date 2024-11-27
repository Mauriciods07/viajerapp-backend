from typing import List, Tuple, Dict
from copy import copy

def getVectorFromOneHot(categories:List, elements:List, info:Tuple) -> Dict:
    one_hot_vector = [0] * len(categories)
    
    oneHotEncoders = []
    
    for element in elements:
        one_hot = copy(one_hot_vector)
        
        for word in element:
            if word in categories:
                index = categories.index(word)
                one_hot[index] = 1

        oneHotEncoders.append(one_hot)

    vectors = {}
    for i in range(len(elements)):
        interests = sum(oneHotEncoders[i])
        id_ = info[i][0]
        price = info[i][1]
        segments = info[i][2]
        vector = [evaluateValue(interests), evaluateValue(price), evaluateValue(segments)]
        vectors[id_] = vector
    
    return vectors

def simpleVectorRecomm(interests_list:List):
    return [len(interests_list), 1, 1]

def evaluateValue(value: int) -> int:
    if (value == 0):
        return 0

    return 1 / value

def getLowestMaxFromDict(interest_recommendation: List, type_: str) -> str:
    similarity = 0
    if (type_ == "MAX"):
        similarity = max(interest_recommendation, key=lambda x:x['similarity'])
    elif (type_ == "MIN"):
        similarity = min(interest_recommendation, key=lambda x:x['similarity'])

    offer_index = next((index for (index, d) in enumerate(interest_recommendation) if d['offer'] == similarity['offer']), None)
    interest_recommendation.pop(offer_index)

    return interest_recommendation, similarity['offer']
