import json
import socket


def check_sum(str1, GenXString):
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


def get_checksum(frame, GenXString):
    info_cyc = str(frame, 'utf8')[8:-8]
    remainder = check_sum(info_cyc, GenXString)
    # remainder = CRCCCITT.CRCCCITT().calculate(str(int(info_cyc, 2)))
    if remainder == '0' * 16:
        print('CRC Correct')
        return True
    else:
        print('CRC Err')
        return False


def main():
    f = open('lab3.json', encoding='utf-8')
    config = json.load(f)

    UDPPort = config['UDPPort']
    Frame_head = config['Frame_head']
    Frame_tail = config['Frame_tail']
    GenXString = config['GenXString']

    ip_port = ('127.0.0.1', UDPPort)
    sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sk.bind(ip_port)
    frame_expected = 0
    combine_frame = ''
    frame, addr = sk.recvfrom(1024)
    loop = int(frame.decode('utf8'))

    while loop:
        print('Frame Expected: ', frame_expected)
        frame, addr = sk.recvfrom(1024)

        seq_get = int(str(frame, 'utf8')[8])
        # 接收后去0处理 frame{bytes}
        frame_get = str(frame, 'utf-8')[0:8] + str(frame, 'utf-8')[8:-8].replace('111110', '11111') + str(frame,
                                                                                                          'utf-8')[-8:]


        if (seq_get == frame_expected) and get_checksum(bytes(frame_get, 'utf8'), GenXString):
            ack = Frame_head + str(frame_expected) + Frame_tail
            sk.sendto(bytes(ack, 'utf8'), addr)
            print('Sending ACK: %d' % frame_expected)
            frame_expected = 1 - frame_expected
            combine_frame += frame_get[9:-24]
            loop -= 1

        else:
            if seq_get != frame_expected:
                print('Get unexpected frame')
            else:
                pass

    file_get = open('file_get.txt', 'w')
    file_get.write(combine_frame)


if __name__ == '__main__':
    main()
