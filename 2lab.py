import socket
import threading
import time

# Флаг для завершения серверов
running = True

# Функция для TCP-сервера
def tcp_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(1)
    print("TCP-сервер запущен. Ожидание подключения...")

    while running:
        try:
            client_socket, address = server_socket.accept()
            print(f"Подключен клиент: {address}")

            message = client_socket.recv(1024).decode('utf-8')
            print(f"Получено сообщение: {message}")

            client_socket.sendall(message.encode('utf-8'))
            client_socket.close()
            print("Соединение закрыто.")
        except OSError:
            break  # Прерывание сервера при завершении

    server_socket.close()
    print("TCP-сервер остановлен.")

# Функция для TCP-клиента
def tcp_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))
    message = "Привет, сервер!"
    client_socket.sendall(message.encode('utf-8'))
    
    response = client_socket.recv(1024).decode('utf-8')
    print(f"Ответ от сервера: {response}")
    
    client_socket.close()

# Функция для UDP-сервера
def udp_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('localhost', 12346))  # Изменён порт на 12346
    print("UDP-сервер запущен. Ожидание данных...")

    while running:
        try:
            data, address = server_socket.recvfrom(1024)
            print(f"Получены данные от {address}: {data.decode('utf-8')}")
            server_socket.sendto(data, address)
        except OSError:
            break  # Прерывание сервера при завершении

    server_socket.close()
    print("UDP-сервер остановлен.")

# Функция для UDP-клиента
def udp_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    message = "Привет, UDP-сервер!"
    client_socket.sendto(message.encode('utf-8'), ('localhost', 12346))  # Изменён порт на 12346
    
    data, server = client_socket.recvfrom(1024)
    print(f"Ответ от сервера: {data.decode('utf-8')}")
    
    client_socket.close()

if __name__ == "__main__":
    # Запуск TCP-сервера в отдельном потоке
    tcp_server_thread = threading.Thread(target=tcp_server)
    tcp_server_thread.start()

    # Даем серверу время для запуска
    time.sleep(1)

    # Запуск TCP-клиента
    tcp_client()

    # Запуск UDP-сервера в отдельном потоке
    udp_server_thread = threading.Thread(target=udp_server)
    udp_server_thread.start()

    # Даем серверу время для запуска
    time.sleep(1)

    # Запуск UDP-клиента
    udp_client()

    # Завершение работы серверов
    running = False
    tcp_server_thread.join()
    udp_server_thread.join()

    print("Программа завершена.")
