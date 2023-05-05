from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model
import pickle
import json
import numpy as np
import sys
sys.path.insert(1,".")
from EmbeddingModel.config import ENCODER_FILE_PATH, TRAINED_MODEL_PATH, TOKENIZER_FILE_PATH, MODEL_ERROR_THRESHOLD,INTENT_FILE_PATH

#Loading Chat Model for prediction 
MODEL = load_model(TRAINED_MODEL_PATH,compile= False)
MODEL.compile(loss='sparse_categorical_crossentropy',optimizer='adam', metrics=['accuracy'])


with open(INTENT_FILE_PATH) as file:
   INTENT = json.load(file)

def padding_up_sentence(sentence):
  # Loading Tokenizer for reducing vocabulary size
  with open(TOKENIZER_FILE_PATH,'rb') as token:
    tokenizer = pickle.load(token)
  max_len = 20
  tokenized_sentence = tokenizer.texts_to_sequences([sentence])

  padded_sequence = pad_sequences(tokenized_sentence,truncating='post', maxlen=max_len)
  return padded_sequence

def chat(input_sentence):
  #Loading LabelEncoder model
  with open(ENCODER_FILE_PATH,'rb') as enc:
    encoder = pickle.load(enc)

  padded_sentence = padding_up_sentence(input_sentence)
  result = MODEL.predict(padded_sentence)
  result_index = np.argmax(result)
  print(result[0][result_index])
  tag = encoder.inverse_transform([result_index])

  if(
       result[0][result_index] < MODEL_ERROR_THRESHOLD
    ):
      return "I don't understand. can you rephrase please"
  
  for intent in INTENT['intents']:
      if intent['tag'] == tag:
          return(np.random.choice(intent['responses']))