from encode import Encoder
from command import pack_command
from handler import send_command


def update_request(build: str, auth: str):
    try:
        command = b"UPLOAD"
        content = Encoder.encode_files(build)

        command = pack_command(command, content, auth)
        client = send_command(command)

        response = client.recv(4096)
        print("Respuesta recibida:", response.decode())

    finally:
        client.close()

if __name__ == '__main__':
    build = "main2"
    key = input("Ingrese la clave: ")

    update_request(build, key)
