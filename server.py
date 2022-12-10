import socket

sock = socket.socket()  # создание сокета
sock.bind(('', 9090))  # хост и порт для нашего сервера
sock.listen(1)  # Если кто-то, явно лишний, пытается еще подстроится сзади, то его пошлют
conn, addr = sock.accept()  # принятие подключение с помощью метода accept

print ('connected:', addr)

while True:
    data = conn.recv(1024)
    if not data:
        break
    conn.send(data.upper())

conn.close()