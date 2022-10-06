import os
import sys
import logging
import database
import requests as r
sys.path.insert(1, ".")
from Model.bot import chat
from bot_config import API_URL, LAST_UPDATE_ID

if not os.path.exists('logs'):
    os.mkdir("logs")
logging.basicConfig( handlers=[ logging.FileHandler('logs/DGI_tele_bot.log') ], format='%(asctime)s - %(name)s - %(message)s', level=logging.INFO)

def message_is_for_chatbot(message):
    if message.get("chat").get("type") == "private" or message.get("text").startswith('/'):
            return True    
    return False

# send message to private chat and reply to group chat
def sendMessage(chat_id, message, reply_id = None): 
    json = {
        "chat_id":chat_id, 
        "text": message, 
        "parse_mode": "html",
    }
    if reply_id:
        json["reply_to_message_id"] = reply_id
    
    return r.get(API_URL + "sendMessage", json = json)
    # return r.get(API_URL + f"sendMessage?chat_id={id}&text={quote(message)}&parse_mode=html")
    # return r.get(API_URL + f"sendMessage?chat_id={chat_id}&text={parse_for_url(message)}&reply_to_message_id={reply_id}&parse_mode=html")

# get updates
def get_updates():
    global LAST_UPDATE_ID
    update = r.get( API_URL + f"getUpdates?offset={LAST_UPDATE_ID+1}&timeout=100")
    update = update.json()["result"]
    if len(update):
        LAST_UPDATE_ID = update[-1]["update_id"]
        logging.info(f"{len(update)} Updates fetched with LAST_UPDATE_ID = {LAST_UPDATE_ID}")
    return update

# filter received messages
def get_messages():
    update = get_updates()
    new_messages =[]
    for i in update:
        message = i.get("message", i.get("channel_post", None))
        if message and message_is_for_chatbot(message):
                new_messages.append(message)
    return new_messages

def main():
    print("checking for new message...", end='')
    
    logging.info("checking for new message")
    update = get_messages()
    print("", end = "\r")
    
    for i in update:
        
        logging.info(f"responding to - {i}")
        
        tele_message = i["text"]
        if tele_message == "/start":
            response = "Hi, I am DGI bot. How can I help you ?"
        else:
            response = chat(tele_message.replace('/', '').strip())
            if response == -1:
                response = "I don't understand. can you rephrase please"
        
        response = str(response)
        
        chat_id = i.get("chat").get("id")
        print(tele_message, "|", response, "|", chat_id)
    
        reply_to = None
        if i.get("chat").get("type") != "private":
            reply_to = i.get("message_id")
        res = sendMessage(chat_id, response, reply_to).json()
        logging.info(f"response callback -{res}")
        
        if res.get("ok"):
            print("messege sending success")
        else:
            print("message sending Failed")
        
        database.insert(tele_message)

if __name__ == "__main__":
    database.con_table()
    while True:
        main()
