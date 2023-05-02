from  nltk import word_tokenize
import json
import random
import pickle
import numpy as np
from nltk.stem.lancaster import LancasterStemmer 
from tensorflow.keras.models import load_model
import sys
sys.path.insert(1, '.')

from FinalModel.config import TRAINING_DATA_PATH, TRAINED_MODEL_PATH, INTENT_FILE_PATH, MODEL_ERROR_THRESHOLD


STEMMER = LancasterStemmer()
DATA = pickle.load(open(TRAINING_DATA_PATH, 'rb'))
WORDS = DATA['words']
CLASSES = DATA['classes']
TRAIN_X = DATA['train_x']
TRAIN_Y = DATA['train_y']

MODEL = load_model(TRAINED_MODEL_PATH, compile= False)
MODEL.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy']) 

with open(INTENT_FILE_PATH) as file:
    INTENTS = json.load(file)


def clean_up_sentence(sentence):
    sentence_words = word_tokenize(sentence)
    sentence_words = []
    for word in sentence_words:
        sentence_words.append(
           STEMMER.stem( word.lower() )
        )
    return sentence_words


def generate_bag_of_words(message, words = WORDS, show_details = False):
    message_words = clean_up_sentence(message)
    bag = [0] * len(words)
    for word in message_words:
        for index, character in enumerate(words):
            if character == word:
                bag[index] = 1
                if show_details:
                    print("Found in bag: %s"% character)
    return(np.array(bag))



def chat(input_message):
  while True:
    response_array = generate_bag_of_words( input_message ).reshape(1,-1)
    results = MODEL.predict(response_array)
    results_index = np.argmax(results)
    
    if(
       results[0][results_index] < MODEL_ERROR_THRESHOLD
    ):
      return "I don't understand. can you rephrase please"
    
    tag = CLASSES[results_index]
    
    for tags in INTENTS["intents"]:
      if tags["tag"] == tag:
        responses=tags["responses"]
        return random.choice(responses)