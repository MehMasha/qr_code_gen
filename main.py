import math
# from gf256 import GF256
from pprint import pprint
from utils import EXP7, LOG8
import numpy as np


def num_to_doub(n):
    string = str(n)
    res_str = ''

    for i in range(0, len(string), 3):
        slice = string[i:i+3]
        doub = bin(int(slice))[2:]
        if len(slice) == 3:
            res_str += '0' * (10 - len(doub)) + doub
        elif len(slice) == 2:
            res_str += '0' * (7 - len(doub)) + doub
        elif len(slice) == 1:
            res_str += '0' * (4 - len(doub)) + doub
    return res_str

def encoding_string(n, res):
    # 0001 для цифрового кодирования


	# Версия 1-9	Версия 10-26	Версия 27-40
    # Цифровое	10 бит	12 бит	14 бит
    # Буквенно-цифровое	9 бит	11 бит	13 бит
    # Побайтовое	8 бит	16 бит	16 бит
    if len(res) > 152:
        raise NotImplementedError('Слишком большое число!!!')
    
    bytes_bin = bin(len(str(n)))[2:]
    if len(bytes_bin) < 10:
        bytes_bin = '0' * (10 - len(bytes_bin)) + bytes_bin

    str_to_code = '0001' + bytes_bin + res

    if len(str_to_code) % 8:
        str_to_code += '0' * (8 - len(str_to_code) % 8)
    return str_to_code


def add_padding_bytes(string):
    # 11101100 и 00010001
    b1 = '11101100'
    b2 = '00010001'

    for i in range(152 // 8 - len(string) // 8):
        if i % 2:
            string += b2
        else:
            string += b1
    return string


def add_corr_bytes(string):
    mnog = [87, 229, 146, 149, 238, 102, 21]
    # 7	            87, 229, 146, 149, 238, 102, 21
    arr = []
    arr1 = []
    for i in range(0, len(string), 8):
        s = string[i:i+8]
        num = int(s, 2)
        arr.append(num)
        arr1.append(s)
    # print(arr)

    for j in range(19):
        a = arr[0]
        arr = arr[1:] + [0]
        if a == 0:
            continue
        b = LOG8[a]
        for i in range(7):
            c = mnog[i] + b
            if c > 254:
                c = c % 255
            d = EXP7[c]
            e = d ^ arr[i]
            arr[i] = e

    arr_corr = ["{0:08b}".format(a) for a in arr[:7]] 

    print(arr)
    return arr1, arr_corr

            

def fixed_patterns(qr):
    n = 21
    for i in range(1, n + 1):
        qr[6][i - 1] = i % 2
        qr[i - 1][6] = i % 2
    # print(*qr, sep='\n')
# □ и ■
    sq1 = np.array([
            [1, 1, 1, 1, 1, 1, 1, 0, 0],
            [1, 0, 0, 0, 0, 0, 1, 0, 0],
            [1, 0, 1, 1, 1, 0, 1, 0, 0],
            [1, 0, 1, 1, 1, 0, 1, 0, 0],
            [1, 0, 1, 1, 1, 0, 1, 0, 0],
            [1, 0, 0, 0, 0, 0, 1, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 0, 0],
    ])
    sq2 = np.array([
            [0, 1, 1, 1, 1, 1, 1, 1],
            [0, 1, 0, 0, 0, 0, 0, 1],
            [0, 1, 0, 1, 1, 1, 0, 1],
            [0, 1, 0, 1, 1, 1, 0, 1],
            [0, 1, 0, 1, 1, 1, 0, 1],
            [0, 1, 0, 0, 0, 0, 0, 1],
            [0, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
    ])
    sq3 = np.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 0, 0],
            [1, 0, 0, 0, 0, 0, 1, 0, 0],
            [1, 0, 1, 1, 1, 0, 1, 0, 0],
            [1, 0, 1, 1, 1, 0, 1, 0, 0],
            [1, 0, 1, 1, 1, 0, 1, 0, 0],
            [1, 0, 0, 0, 0, 0, 1, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 0, 0],
    ])
    qr
    qr1 = np.array(qr)
    qr1[:9, :9] = sq1
    qr1[:9, -8:] = sq2
    qr1[-8:, :9] = sq3
    qr = [list(a) for a in list(qr1)]
    return list(qr)



def draw_qr(qr, string):
    count = 0
    n = 21
    col = n - 1

    # last two zigzags
    for i in range(2):
        for j in range(n - 1, 8, -1):
            qr[j][col] = int(string[count])
            count += 1
            qr[j][col - 1] = int(string[count])
            count += 1
        col -= 2
        for j in range(9, n):
            qr[j][col] = int(string[count])
            count += 1
            qr[j][col - 1] = int(string[count])
            count += 1
        col -= 2
    

    # central zigzag
    for j in range(n - 1, -1, -1):
        if j == 6:
            continue
        qr[j][col] = int(string[count])
        count += 1
        qr[j][col - 1] = int(string[count])
        count += 1
    col -= 2
    for j in range(0, n):
        if j == 6:
            continue
        qr[j][col] = int(string[count])
        count += 1
        qr[j][col - 1] = int(string[count])
        count += 1
    col -= 2
    # print(*qr, sep='\n')


    # first two
    for i in range(2):
        for j in range(n - 9, 8, -1):
            qr[j][col] = int(string[count])
            count += 1
            qr[j][col - 1] = int(string[count])
            count += 1
        col -= 2
        if col == 6:
            col -= 1
        for j in range(9, n - 8):
            qr[j][col] = int(string[count])
            count += 1
            qr[j][col - 1] = int(string[count])
            count += 1
        col -= 2

    # for row in qr:
    #     for s in row:
    #         if s == 0:
    #             print('██', end='')
    #         else:
    #             print('  ', end='')
    #     print()

    return qr


def draw_qr_mask0(qr):
    count = 0
    n = 21
    col = n - 1

    # last two zigzags
    for i in range(2):
        for j in range(n - 1, 8, -1):
            qr[j][col] = qr[j][col] ^ (1 - ((j + col) % 2))
            count += 1
            qr[j][col - 1] = qr[j][col - 1] ^ (1 - ((j + col - 1) % 2))
            count += 1
        col -= 2
        for j in range(9, n):
            qr[j][col] = qr[j][col] ^ (1 - ((j + col) % 2))
            count += 1
            qr[j][col - 1] = qr[j][col - 1] ^ (1 - ((j + col - 1) % 2))
            count += 1
        col -= 2
    

    # central zigzag
    for j in range(n - 1, -1, -1):
        if j == 6:
            continue
        qr[j][col] = qr[j][col] ^ (1 - ((j + col) % 2))
        count += 1
        qr[j][col - 1] = qr[j][col - 1] ^ (1 - ((j + col - 1) % 2))
        count += 1
    col -= 2
    for j in range(0, n):
        if j == 6:
            continue
        qr[j][col] = qr[j][col] ^ (1 - ((j + col) % 2))
        count += 1
        qr[j][col - 1] = qr[j][col - 1] ^ (1 - ((j + col - 1) % 2))
        count += 1
    col -= 2
    # print(*qr, sep='\n')


    # first two
    for i in range(2):
        for j in range(n - 9, 8, -1):
            qr[j][col] = qr[j][col] ^ (1 - ((j + col) % 2))
            count += 1
            qr[j][col - 1] = qr[j][col - 1] ^ (1 - ((j + col - 1) % 2))
            count += 1
        col -= 2
        if col == 6:
            col -= 1
        for j in range(9, n - 8):
            qr[j][col] = qr[j][col] ^ (1 - ((j + col) % 2))
            count += 1
            qr[j][col - 1] = qr[j][col - 1] ^ (1 - ((j + col - 1) % 2))
            count += 1
        col -= 2

# 111011111000100

    # s2 = ''

    qr = np.array(qr)
    s1 = '1110111'
    qr[20:13:-1, 8] = np.array(list(s1))
    qr[8, :6] = np.array(list(s1[:6]))
    s2 = '11000100'
    qr[8, 13:21] = np.array(list(s2))
    qr[:6, 8] = np.array(list(s2[2:][::-1]))
    qr[7:9, 7:9] = np.array([[0, 1], [1, 1]])

    qr = [list(a) for a in qr]
    return qr



def check_qr(qr):
    n = len(qr)

    count = 0
    b_count = 0
    w_count = 0

    for row in qr:
        cur_line = 0
        for i in range(1, n):
            if row[i] == row[i - 1]:
                cur_line += 1
            else:
                if cur_line >= 4:
                    count += cur_line - 1
                    # if row[i - 1] == 1:
                    #     b_count += 1
                    # else:
                    #     w_count += 1
                cur_line = 0
        if cur_line >= 4:
            count += cur_line - 1
            # if row[i - 1] == 1:
            #     b_count += 1
            # else:
            #     w_count += 1
    print(count, b_count, w_count)


    count1 = 0
    b_count1 = 0
    w_count1 = 0

    for j in range(n):
        cur_line = 0
        for i in range(1, n):
            if qr[i][j] == qr[i - 1][j]:
                cur_line += 1
            else:
                if cur_line >= 4:
                    count1 += cur_line - 1
                    # if qr[i - 1][j] == 1:
                    #     b_count1 += 1
                    # else:
                    #     w_count1 += 1
                cur_line = 0
        if cur_line >= 4:
            count1 += cur_line - 1
            # if qr[i - 1][j] == 1:
            #     b_count1 += 1
            # else:
            #     w_count1 += 1
    print(count1, b_count1, w_count1)

    count2 = 0
    b_count2 = 0
    w_count2 = 0

    for i in range(n - 1):
        for j in range(n - 1):
            if qr[i][j] == qr[i + 1][j] == qr[i + 1][j + 1] == qr[i][j + 1]:
                # if qr[i][j]:
                #     b_count2 += 1
                # else:
                #     w_count2 += 1
                count2 += 3

    print(count2, b_count2, w_count2)


    a1 = [1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0]
    a2 = [0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1]
    # a3 = [0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0]
    count3 = 0
    for row in qr:
        for i in range(n - 11):
            if row[i:i+11] == a1:
                count3 += 120
            if row[i:i+11] == a2:
                count3 += 120
    print(count3)

    qr = np.array(qr)
    qr = qr.transpose()
    qr = [list(a) for a in qr]

    count4 = 0
    for row in qr:
        for i in range(n - 11):
            if row[i:i+11] == a1:
                count4 += 120
            if row[i:i+11] == a2:
                count4 += 120
    print(count4)

    print('Всего:', count + count1 + count2 + count3 + count4)
    # print('Белые сегменты:', b_count + b_count1 + b_count2)
    # print('Черные сегменты:', w_count + w_count1 + w_count2)
    b_count = 0
    w_count = 0
    for row in qr:
        b_count += row.count(1)
        w_count += row.count(0)

    pr = int(abs((b_count / 441) * 100 - 50)) * 2

    itog = count + count1 + count2 + count3 + count4 + pr

    return itog




    




    # print(count, b_count, w_count)
        





def print_in_console(qr):
    print('██'* 23)
    for row in qr:
        print('██', end='')
        for s in row:
            if s == 0:
                print('██', end='')
            else:
                print('  ', end='')
        print('██', end='')
        print()
    print('██'* 23)



def main():
    
    try:
        n = int(input())
        print(f'Вы ввели число {n}')
    except:
        raise Exception('Вы не ввели число!!!')
    
    # assert num_to_doub(1234) == '00011110110100', 'Что-то не то с функцией цифрового кодирования'
    res = num_to_doub(n)
    print(res)

    # assert encoding_string('00011110110100') == '00010000000100000111101101000000', 'Не так подготавливается строка'
    str_to_code = encoding_string(n, res)
    print(str_to_code)

    str_with_pad = add_padding_bytes(str_to_code)
    print(str_with_pad)

    arr_old, arr_corr = add_corr_bytes(str_with_pad)
    print(arr_old)
    print(arr_corr)

    string = ''.join(arr_old + arr_corr)


    qr = [[0] * 21 for _ in range(21)]
    qr = fixed_patterns(qr)

    qr = draw_qr(qr, string)

    qr = draw_qr_mask0(qr)

    print_in_console(qr)
    check_qr(qr)





if __name__ == '__main__':
    main()