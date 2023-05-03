from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model
import pickle
import json
import numpy as np
import sys
sys.path.insert(1,".")
from EmbeddingModel.config import TRAINING_DATA_PATH, TRAINED_MODEL_PATH, INTENT_FILE_PATH, MODEL_ERROR_THRESHOLD

DATA = pickle.load(open(TRAINING_DATA_PATH,"rb"))
MODEL = load_model(TRAINED_MODEL_PATH,compile= False)
MODEL.compile(loss='sparse_categorical_crossentropy',optimizer='adam', metrics=['accuracy'])


with open(INTENT_FILE_PATH) as file:
   INTENT = json.load(file)

def padding_up_sentence(sentence):
  tokenizer = DATA['tokenizer']
  max_len = DATA['max_len']
  tokenized_sentence = tokenizer.texts_to_sequences([sentence])

  padded_sequence = pad_sequences(tokenized_sentence,truncating='post', maxlen=max_len)
  return padded_sequence

def chat(input_sentence):
  encoder = DATA['encoder']
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