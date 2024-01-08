
SEP = b"\r\n"


def pack_command(command: bytes, content: bytes, auth: str):
    key = auth.encode() + b"\r\n"
    header = command + SEP
    
    return key + header + content
