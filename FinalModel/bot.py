from  nltk import word_tokenize
import json
import random
import pickle
import numpy as np
from nltk.stem.lancaster import LancasterStemmer 
from tensorflow.keras.models import load_model

stemmer = LancasterStemmer()
data = pickle.load(open('FinalModel//traning_data','rb'))
words = data['words']
classes = data['classes']
train_x = data['train_x']
train_y = data['train_y']

model = load_model('FinalModel//model.h5',compile= False)
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy']) 

with open('FinalModel//intents.json') as f:
    intents = json.load(f)
def clean_up_sentence(sentence):
    sentence_words = word_tokenize(sentence)
    sentence_words= [stemmer.stem(word.lower()) for word in sentence_words]

    return sentence_words

def bow(sentence, words, show_details=False):
    
    sentence_words = clean_up_sentence(sentence)
    bag = [0]*len(words)
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s:
                bag[i] = 1
                if show_details:
                    print("Found in bag: %s"% w)
    return(np.array(bag))

error_thresold = 0.39
def chat(inp):
  while True:
    response_arr = bow(inp,words).reshape(1,-1)
    results=model.predict(response_arr)
    results_index=np.argmax(results)
    if(results[0][results_index]<error_thresold):
      return -1
    tag=classes[results_index]
    for tg in intents["intents"]:
      if tg["tag"]==tag:
        responses=tg["responses"]
        return random.choice(responses)
      
# print(chat('csit hod'))      