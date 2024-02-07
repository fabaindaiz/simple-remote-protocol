from getpass import getpass

from src.protocol.updater import connection, update_request

BUILD = "main2"
HOST = ("192.168.1.220", 8080)


password = getpass()
client = connection(HOST, password)
update_request(client, BUILD)
