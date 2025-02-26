def manual_utf16le_decode(b: bytes) -> str:
    """
    Ручное декодирование UTF-16LE: каждые два байта объединяются,
    при этом первый байт – младший, второй – старший.
    """
    if len(b) % 2 != 0:
        raise ValueError("Длина байтовой последовательности должна быть чётной.")
    result = []
    for i in range(0, len(b), 2):
        low = b[i]
        high = b[i+1]
        code = (high << 8) | low
        result.append(chr(code))
    return "".join(result)


def tea_decrypt(v, k):
    v0, v1 = v[0], v[1]
    delta = 0x9E3779B9
    sum_val = 0xC6EF3720  # delta * 32
    mask = 0xFFFFFFFF

    for _ in range(32):
        v1 = (v1 - (((v0 << 4) + k[2]) ^ (v0 + sum_val) ^ ((v0 >> 5) + k[3]))) & mask
        v0 = (v0 - (((v1 << 4) + k[0]) ^ (v1 + sum_val) ^ ((v1 >> 5) + k[1]))) & mask
        sum_val = (sum_val - delta) & mask

    return [v0, v1]

def hex_to_int_list(hex_string):
    return [int(token, 16) for token in hex_string.split()]

encrypted_hex = """
E3238557 6204A1F8 E6537611 174E5747
5D954DA8 8C2DFE97 2911CB4C 2CB7C66B
E7F185A0 C7E3FA40 42419867 374044DF
2519F07D 5A0C24D4 F4A960C5 31159418
F2768EC7 AEAF14CF 071B2C95 C9F22699
FFB06F41 2AC90051 A53F035D 830601A7
EB475702 183BAA6F 12626744 9B75A72F
8DBFBFEC 73C1A46E FFB06F41 2AC90051
97C5E4E9 B1C26A21 DD4A3463 6B71162F
8C075668 7975D565 6D95A700 7272E637
"""

# Преобразуем hex-строку в список 32-битных чисел
encrypted_ints = hex_to_int_list(encrypted_hex)
key = [0, 4, 5, 1]

decrypted_bytes = bytearray()
for i in range(0, len(encrypted_ints), 2):
    block = encrypted_ints[i:i+2]
    dec_block = tea_decrypt(block, key)
    # Здесь используем little-endian – вероятнее всего, именно так хранятся числа в памяти C-программы
    decrypted_bytes.extend(dec_block[0].to_bytes(4, byteorder='little'))
    decrypted_bytes.extend(dec_block[1].to_bytes(4, byteorder='little'))

# Ручное декодирование как UTF-16LE (без автоматической смены кодировки)
decrypted_text = manual_utf16le_decode(decrypted_bytes)
decrypted_text = decrypted_text[::2]
print(decrypted_text)
