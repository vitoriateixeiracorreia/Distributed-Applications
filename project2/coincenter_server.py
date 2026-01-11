from coincenter_skel import CoinCenterSkeleton
from net_server import NetServer
import signal
import select
import sys


def handle_shutdown(signum, frame):
    global server
    server.close()
    sys.exit(0)

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 coincenter_server.py server_ip server_port")
        sys.exit(1)

    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])

    net_server = NetServer(server_ip, server_port)
    signal.signal(signal.SIGINT, handle_shutdown)
    skel = CoinCenterSkeleton()

    sockets = [net_server.sock]

    while True:
        try:
            ready_to_read, _, _ = select.select(sockets, [], [])
            for sock in ready_to_read:
                if sock is net_server.sock:
                    client_sock, _ = net_server.accept()
                    sockets.append(client_sock)
                    user_id = net_server.recv(client_sock)
                    print('bem vindo: cliente %s com ip %s e no porto %s' % (user_id,server_ip,server_port))
                else:
                    request = net_server.recv(sock)
                    if request != "":
                        print("RECEBEU", request)
                        response = skel.handle_request(request)
                        print("ENVIOU", response)
                        net_server.send(sock, response)
                    else:
                        print('adeus: cliente %s com ip %s e no porto %s' % (user_id,server_ip,server_port))
                        sockets.remove(sock)
                        sock.close()
                        break
        except Exception as e:
            print(f"An error occurred: {e}")
        except KeyboardInterrupt:
            break
                
if __name__ == "__main__":
    main()



