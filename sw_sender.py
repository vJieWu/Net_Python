import json
import random
import socket


def get_checksum(str1, GenXString):
    r = len(GenXString) - 1  # 多项式的阶
    l = len(str1) - r
    lenofgen = len(GenXString)

    q = []  # 商
    str1 = list(str1)
    for i in range(l):
        if str1[i] == '1':
            q += '1'
            for j in range(lenofgen):
                if (str1[i + j] == GenXString[j]):
                    str1[i + j] = '0'
                else:
                    str1[i + j] = '1'
        else:
            q += '0'
    str1 = ''.join(str1)

    checksum = str1[-r::]
    return checksum


def gen_frame(frame_to_send, InfoString, GenXString, Frame_head, Frame_tail):
    crc = get_checksum(frame_to_send + InfoString + '0' * 16, GenXString)
    # crc = bin(CRCCCITT.CRCCCITT().calculate(str(int(frame_to_send + InfoString, 2))))[2:]
    if len(crc) < 16:
        crc = '0' * (16 - len(crc)) + crc
    frame = Frame_head + frame_to_send + InfoString + crc + Frame_tail

    return frame


def filter_frame(frame, ip_port, sk, FilterLost, FilterError):
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
        # 发送之前0bit填充 frame{str} ################
        sk.sendto(bytes(frame, 'utf8'), ip_port)
        print('Expected ACK: ' + frame[8])


def main():
    f = open('lab3.json', encoding='utf-8')
    config = json.load(f)

    UDPPort = config['UDPPort']
    FilterError = config['FilterError']
    FilterLost = config['FilterLost']
    Frame_head = config['Frame_head']
    Frame_tail = config['Frame_tail']
    InfoString = config['InfoString']
    GenXString = config['GenXString']

    loop = 20
    next_frame_to_send = 0  # seq number of next frame

    ip_port = ('127.0.0.1', UDPPort)
    sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while loop:
        print('current_send_frame: %d' % next_frame_to_send)

        try:

            filter_frame(gen_frame(str(next_frame_to_send), InfoString, GenXString, Frame_head, Frame_tail), ip_port,
                         sk, FilterLost, FilterError)
            sk.settimeout(5)

            info, addr = sk.recvfrom(1024)

            if str(info, 'utf8')[8] == str(next_frame_to_send):  ################

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
