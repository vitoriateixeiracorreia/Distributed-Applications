from sock_utils import *
import pickle
import struct

class NetServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = create_tcp_server_socket(host, port)
    
    def accept(self):
        client_socket, client_addr = self.sock.accept()
        return client_socket, client_addr
    
    def recv(self, client_socket):

        data = ""
        resp_size_bytes = client_socket.recv(4)
        
        if resp_size_bytes:
            resp_size = struct.unpack('i', resp_size_bytes)[0]
            resp_bytes = receive_all(client_socket, resp_size)

            data = pickle.loads(resp_bytes)
        return data
    
    def send(self, client_socket, data):
        data_bytes = pickle.dumps(data, -1)
        data_size_bytes = struct.pack('i', len(data_bytes))
        
        client_socket.sendall(data_size_bytes)
        client_socket.sendall(data_bytes)
    
    def close(self):
        self.sock.close()