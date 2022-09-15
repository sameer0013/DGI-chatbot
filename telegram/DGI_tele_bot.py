import sys
import database
import requests as r
sys.path.insert(1, ".")
from Model.bot import chat
from bot_config import API_URL, LAST_UPDATE_ID

def message_is_for_chatbot(text):
    if text is None:
        return False
    if text.startswith('/'):
        if text == "/start":
            return True    
        return False
    return True

# send to private
def sendMessage(chat_id, message): 
    json = {
        "chat_id":chat_id, 
        "text": message, 
        "parse_mode": "html",
    }
    return r.get(API_URL + "sendMessage", json = json)

    # return r.get(API_URL + f"sendMessage?chat_id={id}&text={quote(message)}&parse_mode=html")

# send message
def reply_to(chat_id, reply_id, message):
    json = {
        "chat_id":chat_id, 
        "text": message, 
        "parse_mode": "html",
        "reply_to_message_id": reply_id,
    }
    return r.get(API_URL + "sendMessage", data = json)

    # return r.get(API_URL + f"sendMessage?chat_id={chat_id}&text={parse_for_url(message)}&reply_to_message_id={reply_id}&parse_mode=html")

# get updates
def get_updates():
    global LAST_UPDATE_ID
    update = r.get( API_URL + f"getUpdates?offset={LAST_UPDATE_ID+1}&timeout=100")
    update = update.json()["result"]
    if len(update):
        LAST_UPDATE_ID = update[-1]["update_id"]
    return update

# filter received messages
def get_messages():
    update = get_updates()
    new_messages =[]
    for i in update:
        message = i.get("message", None)
        if message and (message["from"]["is_bot"] is False or message.get("text") == "/start") and message_is_for_chatbot(message.get("text")):
            new_messages.append(message)
    return new_messages

def main():
    print("checking for new message...", end='')
    update = get_messages()
    print("", end = "\r")
    for i in update:
        print(i)
        tele_message = i["text"]
        if tele_message == "/start":
            response = "Hi, I am DGI bot. What would you like to know about DGI ?"
        else:
            response = chat(tele_message)
            if response == -1:
                response = "I don't understand. can you rephrase please"
        
        response = str(response)
        
        chat_id = i.get("chat").get("id")
        print("message - ",tele_message, ",response - " response, ",chat_Id - " chat_id)
    
        if i.get("chat").get("type") == "private":
            print(sendMessage(chat_id, response))
    
        else:
            print(reply_to(chat_id, i.get("message_id"), response))
        database.insert(tele_message)

if __name__ == "__main__":
    database.con_table()
    while True:
        main()
