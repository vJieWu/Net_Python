import socket

UDPPort = 8888
FilterError = 10
FilterLost = 10


def main():
    ip_port = ('127.0.0.1', UDPPort)
    next_frame_to_send = 0  # seq number of next frame
    sk = socket.socket()
    sk.connect(ip_port)
    sk.sendall(bytes('data_frame', 'utf8'))
    server_reply = sk.recv(1024)
    print(str(server_reply, 'utf8'))
    sk.close()


if __name__ == '__main__':
    main()
