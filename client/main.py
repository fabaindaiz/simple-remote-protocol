from src.protocol.updater import connection, update_request

BUILD = "main2"
HOST = ("192.168.1.220", 8080)

auth = input("Ingrese la clave: ")
client = connection(HOST, auth)

update_request(client, BUILD)
