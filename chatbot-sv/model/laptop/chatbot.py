import random
import nltk
import pickle
import numpy as np
import json
from nltk.stem import WordNetLemmatizer
import pandas as pd
from tensorflow.python.keras.models import load_model
#nltk.download('punkt')
#nltk.download('wordnet')
#nltk.download('omw-1.4')


lematizer = WordNetLemmatizer()
with open('../model/laptop/intents.json', encoding="utf8") as json_data:
    intents = json.load(json_data)


words = pickle.load(open('../model/laptop/words.pkl', 'rb'))
classes = pickle.load(open('../model/laptop/classes.pkl', 'rb'))
model = load_model('../model/laptop/laptop-consulting-model.h5')

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lematizer.lemmatize(word) for word in sentence_words]
    return sentence_words


def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)


def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list


def get_response(intents_list, intents_json):
    if len(intents_list) == 0:
        return "mình không hiểu đâu, chúng ta nói chuyện khác nhé"

    tag = intents_list[0]['intent']
    list_of_intent = intents_json['intents']
    for i in list_of_intent:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result


def answer(message):
    ints = predict_class(message)
    res = get_response(ints, intents)
    return res
