import nltk
import json
import time
import random
import pickle
import tflearn
import numpy as np
import tensorflow as tf
from unicodedata import name
from pickletools import float8
from flask import Flask,render_template,request
from nltk.stem.lancaster import LancasterStemmer 

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
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

def chat(inp):
  while True:
    if inp.lower()=="quit":
      break
    results=model.predict([bow(inp,words)])
    results_index=np.argmax(results)
    tag=classes[results_index]
    for tg in intents["intents"]:
      if tg["tag"]==tag:
        responses=tg["responses"]
        return random.choice(responses)

stemmer = LancasterStemmer()
data = pickle.load(open('traning_data','rb'))
words = data['words']
classes = data['classes']
train_x = data['train_x']
train_y = data['train_y']

app = Flask(__name__)
tf.reset_default_graph()
net = tflearn.input_data(shape=[None,len(train_x[0])])
net = tflearn.fully_connected(net,10)
net = tflearn.dropout(net,0.3)
net = tflearn.fully_connected(net,10)
net = tflearn.fully_connected(net,len(train_y[0]),activation='softmax')
net = tflearn.regression(net)
model = tflearn.DNN(net,tensorboard_dir ='tflearn_logs')
model.load("model.tflearn",weights_only=True)

with open('intents.json') as f:
    intents = json.load(f)

context ={}
error_threshold =0.25           

@app.route("/")
def home():
    return render_template("check.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    time.sleep(1)
    return str(chat(userText))

if __name__ == "__main__":
  app.run()
