from flask import Flask,render_template,request
import sys
sys.path.insert(1,".")
from Model.bot import chat
import time


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("check.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    response = chat(userText.strip())
    if type(response) == dict:
        response = response.get("web", response)
    
    return response

if __name__ == "__main__":
  app.run()