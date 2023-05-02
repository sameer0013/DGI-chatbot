from flask import render_template,Flask, request,json
import sys
sys.path.insert(1,".")
from Model.bot import chat


app = Flask(__name__)

@app.get("/")
def index_get():
    return render_template("base.html")

@app.post("/predict")
def predict():
    text = request.get_json().get('message')
    # TODO : check if text is valid
    response = str(chat(text))
    message = {"answer":response}
    return json.jsonify(message)

if __name__ == "__main__":
    app.run(debug=True)



