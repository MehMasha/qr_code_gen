# from gf256 import GF256, GF256LT

# d1 = {}
# d2 = {}
# for i in range(0, 256):
#     a = i
#     b = GF256LT(i)
#     print(a, b, hash(b))
#     d1[a] = b
#     # d2[b] = a

# # print(d1)

# q = list(range(0, 256))

# for i in q:
#     print()


# from pyfinite import ffield

# # Создаем поле Голуа GF(2^8)
# GF = ffield.FField(8)

# # Вычисляем значение альфа в данном поле
# alpha = GF[2]

# # Создаем массив, содержащий все элементы поля
# elements = [GF[i] for i in range(256)]

# # Выводим все элементы поля и их обратные значения
# for element in elements:
#     print(f"Element: {element}, Inverse: {GF.Inverse(element)}")


v = 1
LOG8 = dict()
EXP7 = dict()
for ex in range(256):
    v = ((v<<1)^285) if v>127 else v<<1
    LOG8[v] = ex % 255 + 1
    EXP7[ex%255 + 1] = v

# EXP[0] = 1

# print(LOG8)
# print(EXP7)
