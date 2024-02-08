from src.protocol.updater import Connection, Request

BUILD = "main2"
HOST = ("192.168.1.220", 8080)


if __name__ == "__main__":
    client = Connection.connect(HOST)

    #Request.update(client, BUILD)
    Request.shell(client)
