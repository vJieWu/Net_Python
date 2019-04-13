import socket

UDPPort = 8888
FilterError = 10
FilterLost = 10
Frame_head = '01111110'
Frame_tail = '01111110'
GenXString = '10001000000100001'


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


def get_checksum(frame):
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
    loop = 20
    ip_port = ('127.0.0.1', UDPPort)
    sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sk.bind(ip_port)
    frame_expected = 0

    while loop:
        print('Frame Expected: ', frame_expected)
        frame, addr = sk.recvfrom(1024)
        seq_get = int(str(frame, 'utf8')[8])
        # 接收后去0处理 frame{bytes}
        if seq_get == frame_expected and get_checksum(frame):
            ack = Frame_head + str(frame_expected) + Frame_tail
            sk.sendto(bytes(ack, 'utf8'), addr)

            print('Sending ACK: %d' % frame_expected)
            frame_expected = 1 - frame_expected

            loop -= 1
        else:
            print('Get unexpected frame')


if __name__ == '__main__':
    main()
