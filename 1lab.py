import requests

# URL тестового сервера
url = "https://jsonplaceholder.typicode.com/posts"

# Отправляем GET-запрос на получение всех постов
response = requests.get(url)

# Проверяем успешность запроса
if response.status_code == 200:
    posts = response.json()  # Преобразуем ответ в JSON формат
    print("Посты пользователей с чётными ID:")
    
    # Фильтруем посты пользователей с чётными ID
    for post in posts:
        if post['userId'] % 2 == 0:
            print(f"Post ID: {post['id']}, Title: {post['title']}")
else:
    print(f"Ошибка получения данных: {response.status_code}")
    # URL для создания поста
url = "https://jsonplaceholder.typicode.com/posts"

# Данные нового поста
new_post = {
    "title": "Тестовый пост",
    "body": "Это тестовое содержание поста",
    "userId": 1
}

# Отправляем POST-запрос для создания нового поста
response = requests.post(url, json=new_post)

# Проверяем успешность запроса и выводим ответ
if response.status_code == 201:
    created_post = response.json()
    print("Созданный пост:")
    print(created_post)
else:
    print(f"Ошибка создания поста: {response.status_code}")
# ID поста, который мы только что создали (в реальности его нужно будет получить из ответа предыдущего запроса)
post_id = 101  # Пример ID, так как на этом сервере посты создаются только с ID > 100

# URL для обновления поста
url = f"https://jsonplaceholder.typicode.com/posts/{post_id}"

# Обновлённые данные поста
updated_post = {
    "title": "Обновлённый пост",
    "body": "Обновлённое содержание поста",
    "userId": 1
}

# Отправляем PUT-запрос для обновления поста
response = requests.put(url, json=updated_post)

# Проверяем успешность запроса и выводим обновлённый пост
if response.status_code == 200:
    updated_post_response = response.json()
    print("Обновлённый пост:")
    print(updated_post_response)
else:
    print(f"Ошибка обновления поста: {response.status_code}")
