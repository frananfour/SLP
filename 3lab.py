import sqlite3
import requests

#создаю бд
conn = sqlite3.connect('database.db')
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    title TEXT,
    body TEXT
)
''')
conn.commit()
conn.close()

# получ лданные
url = 'https://jsonplaceholder.typicode.com/posts'
response = requests.get(url)
posts_data = response.json()

# сохраняю данные в бд
conn = sqlite3.connect('database.db')
cursor = conn.cursor()
for post in posts_data:
    cursor.execute('''
    INSERT OR REPLACE INTO posts (id, user_id, title, body)
    VALUES (?, ?, ?, ?)
    ''', (post['id'], post['userId'], post['title'], post['body']))
conn.commit()
conn.close()

# Чтение данных из базы по user_id
def get_posts_by_user(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM posts WHERE user_id = ?', (user_id,))
    posts = cursor.fetchall()
    conn.close()
    return posts

# тест
user_posts = get_posts_by_user(1)
for post in user_posts:
    print(post)
