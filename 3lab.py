import sqlite3
import requests

# Шаг 1. Создание базы данных и таблицы
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

# Шаг 2. Получение данных с сервера
url = 'https://jsonplaceholder.typicode.com/posts'
response = requests.get(url)
posts_data = response.json()

# Шаг 3. Сохранение данных в базу данных
conn = sqlite3.connect('database.db')
cursor = conn.cursor()
for post in posts_data:
    cursor.execute('''
    INSERT OR REPLACE INTO posts (id, user_id, title, body)
    VALUES (?, ?, ?, ?)
    ''', (post['id'], post['userId'], post['title'], post['body']))
conn.commit()
conn.close()

# Шаг 4. Чтение данных из базы по user_id
def get_posts_by_user(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM posts WHERE user_id = ?', (user_id,))
    posts = cursor.fetchall()
    conn.close()
    return posts

# Тестируем чтение данных для пользователя с user_id = 1
user_posts = get_posts_by_user(1)
for post in user_posts:
    print(post)
