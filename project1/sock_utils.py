"""
Aplicações Distribuídas - Projeto 1 - sock_utils.py
Número de aluno: 62211
"""
import socket as s

def create_tcp_server_socket(address='localhost', port=9999, queue_size=1):
    sock = s.socket(s.AF_INET, s.SOCK_STREAM)
    sock.bind((address, port))
    sock.listen(queue_size)
    return sock

def create_tcp_client_socket(address='localhost', port=9999):
    sock = s.socket(s.AF_INET, s.SOCK_STREAM)
    sock.connect((address, port))
    return sock