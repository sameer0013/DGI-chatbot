import requests as r
from bot_config import TOKEN, API_URL, LAST_MESSAGE_ID
from main import chat

def message_is_for_chatbot(text):
    if text is None:
        return False
    if text.startswith('/'):    
        return False
    return True

# send to private
def sendMessage(id, message): 
    return r.get(API_URL + f"sendMessage?chat_id={id}&text={message}")

# send message
def reply_to(chat_id, reply_id, message):
    return r.get(API_URL + f"sendMessage?chat_id={chat_id}&text={message}&reply_to_message_id={reply_id}")

#receive message
def receive():
    update = r.get(API_URL+"getUpdates").json()["result"]
    new_messages =[]
    for i in update:
        message = i.get("message", {})
        if message.get("message_id", -1) > LAST_MESSAGE_ID and message["from"]["is_bot"] is False and message_is_for_chatbot(message.get("text")):
            new_messages.append(i.get("message"))
    return new_messages

def main():
    update = receive()
    for i in update:
        print(i)
        # pass
        # call chatbot here
        send_this_to_chatbot = i["text"]

        # what chat bot rerurned
        # chatbot_returned = from_bot(send_this_to_chatbot)
        chatbot_returned = str(chat(send_this_to_chatbot))
        chat_id = i.get("chat").get("id")
        if i.get("chat").get("type") == "private":
            sendMessage(chat_id, chatbot_returned)
        else:
            reply_to(chat_id, i.get("message_id"), chatbot_returned)
        LAST_MESSAGE_ID = i.get("message_id")
        print(LAST_MESSAGE_ID)

if __name__ == "__main__":
    main()
    # print(r.get(API_URL+ "getMe").json())
