import random
import socket

from PyCRC import CRCCCITT

# CRCCCIT.CRCCCITT().calculate(input)
UDPPort = 8888
FilterError = 10
FilterLost = 10
Frame_head = '01111110'
Frame_tail = '01111110'
InfoString = '11111010101010101010101010101111'

ip_port = ('127.0.0.1', UDPPort)
sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def get_frame(frame_to_send):
    crc = bin(CRCCCITT.CRCCCITT().calculate(int(InfoString, 2)))[1:]
    frame = Frame_head + frame_to_send + InfoString + crc + Frame_tail

    return frame


def filter_frame(frame):
    if random.randint(1, FilterLost) == 1:
        print('Frame Lost')
    else:
        if random.randint(1, FilterError) == 1:
            print('Frame Err')

            if frame[9] == '0':
                frame = frame[:9] + '1' + frame[10:]
            else:
                frame = frame[:9] + '0' + frame[10:]

        else:
            print('Frame Sent Successfully')

        sk.sendto(bytes(str(frame), 'utf8'), ip_port)


def main():
    loop = 20
    next_frame_to_send = 0  # seq number of next frame

    while loop:
        print('current_send_frame: %d' % next_frame_to_send)

        try:

            filter_frame(get_frame(str(next_frame_to_send)))
            sk.settimeout(5)
            print('Expected ACK: %d' % next_frame_to_send)  # timeout = 1s
            info, addr = sk.recvfrom(1024)

            if str(info, 'utf8')[8] == next_frame_to_send:  ################

                print('Receive ACK: ' + str(info, 'utf8')[8])  # 接受正确的ack，输出相关信息

                next_frame_to_send = 1 - next_frame_to_send
                print('next_frame_to_send: %d' % next_frame_to_send)
                loop -= 1
            else:
                print('Receive unexpected ACK')

        except OSError:
            print('Receive ACK timeout Err!')


if __name__ == '__main__':
    main()
