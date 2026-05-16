import sqlite3

conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
user_id INTEGER PRIMARY KEY,
status TEXT,
words TEXT
)
""")

conn.commit()


def get_all_users():
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()


def get_user(user_id):
    cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    return cursor.fetchone()


def create_user(user_id):
    cursor.execute("INSERT OR REPLACE INTO users VALUES(?,?,?)",
                   (user_id, "playing", ""))
    conn.commit()


def update_words(user_id, words):
    cursor.execute("UPDATE users SET words=? WHERE user_id=?",
                   (",".join(words), user_id))
    conn.commit()


def finish_user(user_id):
    cursor.execute("UPDATE users SET status='finished' WHERE user_id=?",
                   (user_id,))
    conn.commit()


def stats():
    cursor.execute("SELECT COUNT(*) FROM users")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM users WHERE status='finished'")
    finished = cursor.fetchone()[0]

    return total, finished
