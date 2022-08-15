from keras.callbacks import TensorBoard, EarlyStopping
from pickletools import optimize
import nltk
import tensorflow as tf
import numpy as np
import json
import pickle
import tflearn
import random
from nltk.stem.lancaster import LancasterStemmer


nltk.download('punkt')

stemmer = LancasterStemmer()
with open('intents.json') as json_file:
    intents = json.load(json_file)

# print(intents)   

words =[]
documents =[]
classes =[]

ignore =["?"]

for intent in intents["intents"]:
    for pattern in intent['patterns']:
        w = nltk.word_tokenize(pattern)
        words.extend(w)
        documents.append((w,intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

# print(words)
# print(documents)
# print(classes)    

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

# print(training)

train_x = list(training[:,0])
train_y = list(training[:,1])


tf.reset_default_graph() #Reset Underlying Graph data

#Building our own Neural Network

net = tflearn.input_data(shape=[None,len(train_x[0])])
net = tflearn.fully_connected(net,10)
net = tflearn.dropout(net,0.2)
net = tflearn.fully_connected(net,10)
net = tflearn.fully_connected(net,len(train_y[0]),activation='softmax')
net = tflearn.regression(net)
#Defining model and setting up tensorborad
model = tflearn.DNN(net,tensorboard_dir ='tflearn_logs')

#Now we have to setup model, now we need to train that model by fitting data into model.fit()
#n_epoch is the number of times that model will se our data during training
model.fit(train_x,train_y,n_epoch=1000,batch_size=8,show_metric=True)
model.save('model.tflearn') #Saving the builded model


pickle.dump({'words':words,'classes':classes,'train_x':train_x,'train_y':train_y},open('traning_data','wb'))
   
