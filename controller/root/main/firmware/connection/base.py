
EOF = b"\r\n\r\n"
SEP = b"\r\n"


class Connection:

    def start(self):
        raise NotImplementedError

    async def listen(self):
        raise NotImplementedError

class Handler():

    def receive(self):
        raise NotImplementedError
    
    def send(self):
        raise NotImplementedError
    
    def close(self):
        raise NotImplementedError
