import json
import random
import pickle
from numpy import array, argmax
from nltk import word_tokenize
from tensorflow.python.framework import ops
from nltk.stem.lancaster import LancasterStemmer 
from tflearn import input_data, fully_connected, regression, DNN

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
    return(array(bag))

error_thresold = 0.39
def chat(inp):
  while True:
    results=model.predict([bow(inp,words)])
    results_index=argmax(results)
    if(results[0][results_index]<error_thresold):
      return -1
    tag=classes[results_index]
    for tg in intents["intents"]:
      if tg["tag"]==tag:
        responses=tg["responses"]
        return random.choice(responses)

stemmer = LancasterStemmer()
data = pickle.load(open('Model/traning_data','rb'))
words = data['words']
classes = data['classes']
train_x = data['train_x']
train_y = data['train_y']

ops.reset_default_graph()
net = input_data(shape=[None,len(train_x[0])])
net = fully_connected(net,8)
net = fully_connected(net,8)
net = fully_connected(net,len(train_y[0]),activation='softmax')
net = regression(net)
model = DNN(net,tensorboard_dir ='tflearn_logs')
model.load("Model//model.tflearn",weights_only=True)

with open('Model//intents.json') as f:
    intents = json.load(f)
         


