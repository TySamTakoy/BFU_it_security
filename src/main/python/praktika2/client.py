import socket
import ssl

HOST = 'localhost'
PORT = 8443
CA_FILE = 'server/cert.pem'  # проверяем серверный сертификат

def send_numbers_and_receive(numbers_string):
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.check_hostname = False
    context.load_verify_locations(CA_FILE)

    with socket.create_connection((HOST, PORT)) as sock:
        with context.wrap_socket(sock, server_hostname='localhost') as ssock:

            # отправляем строку (оканчиваем переводом строки)
            payload = numbers_string.strip() + '\n'
            ssock.sendall(payload.encode('utf-8'))

            # читаем ответ до перевода строки
            data = b''
            while True:
                chunk = ssock.recv(4096)
                if not chunk:
                    break
                data += chunk
                if b'\n' in chunk:
                    break
            if not data:
                print("Нет ответа от сервера.")
                return
            print("Сервер ответил:", data.decode('utf-8').strip())

if __name__ == '__main__':
    numbers = input("Введите числа через пробел: ")
    send_numbers_and_receive(numbers)
