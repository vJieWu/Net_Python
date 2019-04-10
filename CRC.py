InfoString1 = '11111010101010101010101010101111'  # 第一位不一定为1
InfoString2 = '11111010101010101010101010101111'
GenXString = '10001000000100001'  # 第一位必须为1


def getChecksum(str1, GenXString):
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


def main():
    r = len(GenXString) - 1
    Info_r = InfoString1 + '0' * r  # 补0计算校验和
    CRC_code = getChecksum(Info_r, GenXString)

    print('=================发送方=======================')
    print('待发送数据：%s' % InfoString1)
    print('生成多项式：CRC-CCITT=X^16+X^12+X^5+X^0')
    print('冗余校验码：%s' % CRC_code)
    print('带校验和的发送帧：%s' % (InfoString1 + CRC_code))
    print('==================接收方=======================')
    print('接受的信息数据：%s' % InfoString2)

    Info_get = InfoString1 + CRC_code  # 接收到的字符串
    remainder = getChecksum(Info_get, GenXString)  # 计算余数
    print('余数为：%s' % remainder)

    if (remainder == '0' * r):
        print('传输无错误')
    else:
        print('传输错误')


if __name__ == "__main__":
    main()
