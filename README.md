# DGI-chatbot
An Deep Learning  and NLP based chatbot for answering general questions about [Dronacharya Group of Institutions](https://gnindia.dronacharya.info/). Chat directly to the bot on telegram or add it to a group/channel. Ask it about the courses, faculty, facilities, location, bus routes, etc. Almost all the queries are answered based on the model and any unanswered query is stored in a database to process and improve the bot.

DGI-chatbot is currently available for telegram only.

> To use DGI-chatbot on telegram [click here](https://t.me/DGI_tele_bot)

## Prerequisites
- Python
- numpy
- nltk
- tensorflow
- tflearn
- keras
- h5py

## Setup | How to use
1. install from github and open:
```
git clone https://github.com/sameer0013/DGI-chatbot.git
cd Chatbot
```
2. Install ther required files as per `requirements.txt` or use
``` 
pip install requirements.txt
```
3. Run `DGI_tele_bot.py` in telegram folder to run a locally hosted instance of the bot.

4. Search `@DGI_tele_bot` on telegram and start chatting.

## To Do
Add web browser based UI to interect with DGI-chatbot

## Train your own model
Use train_model.py to train the model for your own. The default parameters are the best for our system, and were used to train model. you will need to adjust them accordingly 
## Contributors
[Sameer](https://github.com/sameer0013/)

[Pranjal](https://github.com/pran-jal)
