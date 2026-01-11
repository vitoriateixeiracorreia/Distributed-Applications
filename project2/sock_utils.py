import socket as s

def create_tcp_server_socket(address='localhost', port=9999, queue_size=1):
    sock = s.socket(s.AF_INET, s.SOCK_STREAM)
    sock.bind((address, port))
    sock.listen(queue_size)
    return sock

def create_tcp_client_socket(address='localhost', port=9999):
    try:
        sock = s.socket(s.AF_INET, s.SOCK_STREAM)
        sock.connect((address, port))
        return sock
    except s.error as err:
        print("ERRO: ", err)
        exit(1)

def receive_all(s, resp_size):
    data = b''
    while len(data) < resp_size:
        segment = s.recv(resp_size - len(data))
        if not segment:  # Handle case where connection is closed
            raise ConnectionError("Socket connection closed before receiving all data")
        data += segment
    return data
