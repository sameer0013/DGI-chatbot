import json
import numpy as np
import pickle
import tensorflow as tf 
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense,Embedding,GlobalAveragePooling1D
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
import sys
sys.path.insert(1,".")
from EmbeddingModel.config import INTENT_FILE_PATH, TRAINING_DATA_PATH

def main():
  with open(INTENT_FILE_PATH) as file:
    data = json.load(file)

  training_sentences = []
  training_labels = []
  labels = []
  responses = []
  count_responses = 0
  for intent in data['intents']:
    for patterns in intent['patterns']:
        training_sentences.append(patterns)
        training_labels.append(intent['tag'])
    responses.append(intent['responses'])
    count_responses += len(intent['responses'])
    
    if intent['tag'] not in labels:
        labels.append(intent['tag']) 

  print()
  print(len(training_sentences),"sentences")
  print(len(labels),"Labels")  
  print(len(responses)*count_responses,"Total responses")  
  print() 

  encoder= LabelEncoder()
  encoder.fit(training_labels)
  training_labels = encoder.transform(training_labels)

  #vectorize our text data corpus by using the “Tokenizer” class and it allows us to limit our vocabulary size up to some defined number
  vocab_size = 1000
  embedding_dim = 16
  max_len = 20
  oov_token = "<OOV>"

  tokenizer = Tokenizer(num_words=vocab_size, oov_token=oov_token)
  tokenizer.fit_on_texts(training_sentences)
  word_index = tokenizer.word_index
  sequences = tokenizer.texts_to_sequences(training_sentences)
  padded_sequences = pad_sequences(sequences, truncating='post', maxlen=max_len) #“pad_sequences” method is used to make all the training text sequences into the same size..


  #Model training
  num_classes = len(labels)
  model = Sequential()
  model.add(Embedding(vocab_size, embedding_dim, input_length=max_len))
  model.add(GlobalAveragePooling1D())
  model.add(Dense(16, activation='relu'))
  model.add(Dense(16, activation='relu'))
  model.add(Dense(num_classes, activation='softmax'))

  model.compile(loss='sparse_categorical_crossentropy',optimizer='adam', metrics=['accuracy'])

  model.summary()

  epochs = 1000
  history = model.fit(padded_sequences, np.array(training_labels), epochs=epochs)

  print('Model and Data Saving')
  model.save('EmbeddingModel//chat_model') #saving model
  
  with open('EmbeddingModel//tokenizer.pickle','wb') as handle:
    pickle.dump(tokenizer,handle, protocol=pickle.HIGHEST_PROTOCOL)

  with open('EmbeddingModel//label_encoder.pickle','wb') as file:
    pickle.dump(encoder,file,protocol=pickle.HIGHEST_PROTOCOL)   

  print("Model and Data Saved")

  return 
if __name__ == '__main__':
   main()
