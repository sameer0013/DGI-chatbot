import requests as r
# from main import chat
from urllib.parse import quote_plus as quote
from bot_config import API_URL, LAST_UPDATE_ID

def message_is_for_chatbot(text):
    if text is None:
        return False
    if text.startswith('/'):    
        return False
    return True

# send to private
def sendMessage(id, message): 
    return r.get(API_URL + f"sendMessage?chat_id={id}&text={quote(message)}")

# send message
def reply_to(chat_id, reply_id, message):
    return r.get(API_URL + f"sendMessage?chat_id={chat_id}&text={quote(message)}&reply_to_message_id={reply_id}")

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
        if message and message["from"]["is_bot"] is False and message_is_for_chatbot(message.get("text")):
            new_messages.append(message)
    return new_messages

def main():
    print("checking for new message...", end='')
    update = get_messages()
    print("", end = "\r")
    for i in update:
        print(i)
        send_this_to_chatbot = i["text"]
        # chatbot_returned = str(chat(send_this_to_chatbot))
        chat_id = i.get("chat").get("id")
        # print(send_this_to_chatbot, chatbot_returned, chat_id)
    
        # if i.get("chat").get("type") == "private":
            # print(sendMessage(chat_id, chatbot_returned))
    
        # else:
            # print(reply_to(chat_id, i.get("message_id"), chatbot_returned))

if __name__ == "__main__":
    while True:
        main()

