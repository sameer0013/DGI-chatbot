from flask import Flask,render_template,request,jsonify
import sys
sys.path.insert(1,".")
from Model.bot import chat
import time


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    time.sleep(1)
    return str(chat(userText))
# def predict():
#    text = request.get_json().get('msg')
#    # TODO : check if text is valid
#    response = str(chat(text))
#    message = {"answer": response}
#    return jsonify(message)

if __name__ == "__main__":
  app.run()