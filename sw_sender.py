import random
import socket

UDPPort = 8888
FilterError = 10
FilterLost = 10
Frame_head = '01111110'
Frame_tail = '01111110'
InfoString = '11111010101010101010101010101111'
GenXString = '10001000000100001'  # 第一位必须为1
ip_port = ('127.0.0.1', UDPPort)
sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


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


def gen_frame(frame_to_send):
    crc = get_checksum(frame_to_send + InfoString + '0' * 16, GenXString)
    # crc = bin(CRCCCITT.CRCCCITT().calculate(str(int(frame_to_send + InfoString, 2))))[2:]
    if len(crc) < 16:
        crc = '0' * (16 - len(crc)) + crc
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

        sk.sendto(bytes(frame, 'utf8'), ip_port)
        print('Expected ACK: ' + frame[8])


def main():
    loop = 20
    next_frame_to_send = 0  # seq number of next frame

    while loop:
        print('current_send_frame: %d' % next_frame_to_send)

        try:

            filter_frame(gen_frame(str(next_frame_to_send)))
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
