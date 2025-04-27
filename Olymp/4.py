import struct


def parse_c(data, offset):
    c1, c2, c3, c4, c5 = struct.unpack_from('>ifhQH', data, offset)
    return {'C1': c1, 'C2': c2, 'C3': c3, 'C4': c4, 'C5': c5}


def parse_e(data, offset):
    size1, addr1 = struct.unpack_from('>IH', data, offset)
    arr1 = list(struct.unpack_from(f'>{size1}B', data, addr1))
    e2, e3 = struct.unpack_from('>dd', data, offset + 6)
    offset2 = offset + 6 + 16
    size2, addr2 = struct.unpack_from('>HH', data, offset2)
    arr2 = list(struct.unpack_from(f'>{size2}I', data, addr2))
    e5, = struct.unpack_from('>d', data, offset2 + 4)
    return {'E1': arr1, 'E2': e2, 'E3': e3, 'E4': arr2, 'E5': e5}


def parse_d(data, offset):
    d1, addr_e = struct.unpack_from('>HI', data, offset)
    return {'D1': d1, 'D2': parse_e(data, addr_e)}


def parse_b(data, offset):
    addr_c, b2 = struct.unpack_from('>Hq', data, offset)
    size3, addr3 = struct.unpack_from('>II', data, offset + 10)
    b4, = struct.unpack_from('>f', data, offset + 18)
    c = parse_c(data, addr_c)
    addr_list = struct.unpack_from(f'>{size3}I', data, addr3)
    b3 = [parse_d(data, a) for a in addr_list]
    return {'B1': c, 'B2': b2, 'B3': b3, 'B4': b4}


def parse_a(data):
    a1, addr_b = struct.unpack_from('>hI', data, 4)
    size3, addr3 = struct.unpack_from('>HH', data, 10)
    a2 = parse_b(data, addr_b)
    a3 = list(struct.unpack_from(f'>{size3}f', data, addr3))
    return {'A1': a1, 'A2': a2, 'A3': a3}


def main(data):
    if data[:4] != b'\x56\x54\x44\x80':
        print("Кто-то где-то накосячил")
    return parse_a(data)
