from sock_utils import *
import pickle
import struct

class NetClient:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = create_tcp_client_socket(host, port)
     
    def send(self, data):
        data_bytes = pickle.dumps(data, -1)
        data_size_bytes = struct.pack('i', len(data_bytes))

        self.sock.sendall(data_size_bytes)
        self.sock.sendall(data_bytes)

    def recv(self):
        self.sock.settimeout(5)
        data = ''
        try:
            resp_size_bytes = self.sock.recv(4) #recv em vez de receive_all porque resp_size_bytes pode ser menor que 4
            resp_size = struct.unpack('i',resp_size_bytes)[0]
            resp_bytes = receive_all(self.sock, resp_size)
        except self.sock.timeout as st:
            self.sock.settimeout(None)
            raise RuntimeError("Sem dados:", st)    
        data = pickle.loads(resp_bytes)
        return data

    def close(self):
        self.sock.close()