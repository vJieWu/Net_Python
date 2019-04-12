import socket

UDPPort = 8888
FilterError = 10
FilterLost = 10


def filter_frame():
    return


def main():
    ip_port = ('127.0.0.1', UDPPort)
    next_frame_to_send = 0  # seq number of next frame
    sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    loop = 20

    while loop:

        print('next_frame_to_send: %d' % next_frame_to_send)
        sk.sendto(bytes('data_frame', 'utf8'), ip_port)
        try:
            sk.settimeout(1)  # timeout = 1s
            data, addr = sk.recvfrom(1024)
            print(str(data, 'utf8'))
        except OSError:
            print('Receive ACK timeout Err!')

        loop -= 1


if __name__ == '__main__':
    main()
