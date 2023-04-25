import math


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




if __name__ == '__main__':
    main()