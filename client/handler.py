import socket

HOST = "192.168.100.220"
PORT = 8080


def send_command(data):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    client.send(data)
    return client
