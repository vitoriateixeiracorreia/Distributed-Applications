"""
Aplicações Distribuídas - Projeto 1 - net_client.py
Número de aluno: 62211
"""
from sock_utils import *
import pickle
import struct

class NetClient:

    def __init__(self, id, host, port):
        self.id = id
        self.host = host
        self.port = port
        self.sock = create_tcp_client_socket(host, port)
        self.recv_msg = 0
     
    def send(self, data):
        data_bytes = pickle.dumps(data, -1)
        data_size_bytes = struct.pack('i', len(data_bytes))

        self.sock.sendall(data_size_bytes)
        self.sock.sendall(data_bytes)

    def recv(self):
        resp_size_bytes = self.sock.recv(4)
        resp_size = struct.unpack('i',resp_size_bytes)[0]

        resp_bytes = self.sock.recv(resp_size)
        self.recv_msg = pickle.loads(resp_bytes)

    def close(self):
        self.sock.close()