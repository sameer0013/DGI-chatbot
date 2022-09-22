import sqlite3

def con_table():
    con = sqlite3.connect('telegram\\telegram_database.db')
    cur = con.cursor()
    if len(cur.execute("SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'messages'").fetchall()):
        return
    cur.execute("CREATE TABLE messages(id INTEGER PRIMARY KEY AUTOINCREMENT, message varchar(50) NOT NULL)")
    con.commit()
    con.close()

def insert(message):
    con = sqlite3.connect('telegram\\telegram_database.db')
    cur = con.cursor()
    cur.execute("INSERT INTO messages(message) VALUES(?)", (message,))
    con.commit()
    con.close()
    return f"{message} inserted to database"

def get_messages():
    con = sqlite3.connect('telegram\\telegram_database.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM messages")
    messages = cur.fetchall()
    con.close()
    return messages

def show_messages():
    messages = get_messages()
    for message in messages:
        print(message)

def save_message():
    messages = get_messages()
    with open("messages.txt", 'w') as f:
        f.write('\n'.join(messages))
        f.close()
    print("Messages exported to messages.txt")

if __name__ == "__main__":
    show_messages()