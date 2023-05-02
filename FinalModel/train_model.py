from nltk import word_tokenize
import nltk
import json
import pickle
import random
import numpy as np
import tensorflow as tf
from nltk.stem.lancaster import LancasterStemmer
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

def main():
    nltk.download('punkt')

    stemmer = LancasterStemmer()
    with open('intents.json') as json_file:
        intents = json.load(json_file)

    words =[]
    documents =[]
    classes =[]
    ignore =["?"]

    for intent in intents["intents"]:
        for pattern in intent['patterns']:
            w = word_tokenize(pattern)
            words.extend(w)
            documents.append((w,intent['tag']))
            if intent['tag'] not in classes:
                classes.append(intent['tag'])

    words = [ stemmer.stem(word.lower()) for word in words if word not in ignore]
    words = sorted(list(set(words)))

    classes = sorted(list(set(classes)))

    print(len(documents)," documents \n")
    print(len(words)," words \n")
    print(len(classes)," classes \n")

    traning = []
    output = []
    output_empty = [0]*len(classes)

    training =[] ####X
    output=[] 
    output_empty =[0]*len(classes)

    for doc in documents:
        bag =[] 

        pattern_words = doc[0]

        pattern_words = [stemmer.stem(word.lower()) for word in pattern_words]
        for w in words:
          bag.append(1) if w in pattern_words else bag.append(0)

        output_row = list(output_empty)
        output_row[classes.index(doc[1])]=1
        training.append([bag,output_row])  

    random.shuffle(training)
    training = np.array(training)

    train_x = list(training[:,0])
    train_y = list(training[:,1])

    model = Sequential()                                    #Define Sequential model

    model.add(Dense(8, input_dim=len(train_x[0]), activation='relu'))  #Input layer
    model.add(Dense(8, activation='relu'))                  #Hidden layer
    model.add(Dense(len(train_y[0]), activation='softmax')) #Output layer
    
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy']) #Compile model

    #Training Model
    model.fit(train_x, train_y, epochs=100, batch_size=8)

    model.save('model.h5') #Saving the builded model
   
    pickle.dump({'words':words,'classes':classes,'train_x':train_x,'train_y':train_y},open('traning_data','wb'))
   

