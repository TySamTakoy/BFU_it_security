import socket
import ssl

HOST = '0.0.0.0'
PORT = 8443
CERTFILE = 'server/cert.pem'
KEYFILE = 'server/key.pem'

def handle_connection(connstream):
    try:
        # читаем до перевода строки
        data = b''
        while True:
            chunk = connstream.recv(4096)
            if not chunk:
                break
            data += chunk
            if b'\n' in chunk:
                break
        if not data:
            return
        text = data.decode('utf-8').strip()
        print(f"Получил: {text!r}")

        # парсим числа (разделитель — пробелы/запятые), считаем сумму
        # допускаем целые и дробные
        cleaned = text.replace(',', ' ')
        parts = cleaned.split()
        nums = []
        for p in parts:
            try:
                nums.append(float(p))
            except ValueError:
                # игнорируем нечисла
                pass

        total = sum(nums)
        reply = f"{total}\n"
        connstream.sendall(reply.encode('utf-8'))
        print(f"Отправил: {reply.strip()!r}")
    finally:
        try:
            connstream.shutdown(socket.SHUT_RDWR)
        except Exception:
            pass
        connstream.close()

def main():
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=CERTFILE, keyfile=KEYFILE)

    bindsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    bindsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    bindsock.bind((HOST, PORT))
    bindsock.listen(5)
    print(f"Сервер слушает {HOST}:{PORT} (TLS)")

    try:
        while True:
            newsock, addr = bindsock.accept()
            try:
                connstream = context.wrap_socket(newsock, server_side=True)
                print(f"Подключение из {addr}")
                handle_connection(connstream)
            except ssl.SSLError as e:
                print("SSL ошибка:", e)
                newsock.close()
    except KeyboardInterrupt:
        print("Сервер остановлен.")
    finally:
        bindsock.close()

if __name__ == '__main__':
    main()
