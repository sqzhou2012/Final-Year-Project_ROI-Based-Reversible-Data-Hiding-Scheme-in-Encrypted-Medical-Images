from copy import copy

Sbox = (
0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76, 0xCA, 0x82, 0xC9, 0x7D,
0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0, 0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC,
0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15, 0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2,
0xEB, 0x27, 0xB2, 0x75, 0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF, 0xD0, 0xEF, 0xAA, 0xFB,
0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8, 0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5,
0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2, 0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D,
0x64, 0x5D, 0x19, 0x73, 0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79, 0xE7, 0xC8, 0x37, 0x6D,
0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08, 0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6,
0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A, 0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9,
0x86, 0xC1, 0x1D, 0x9E, 0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16)

inv_sbox = [0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb, 0x7c, 0xe3,
            0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb, 0x54, 0x7b, 0x94, 0x32,
            0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e, 0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9,
            0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25, 0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16,
            0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92, 0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15,
            0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84, 0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05,
            0xb8, 0xb3, 0x45, 0x06, 0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13,
            0x8a, 0x6b, 0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73,
            0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e, 0x47, 0xf1,
            0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b, 0xfc, 0x56, 0x3e, 0x4b,
            0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4, 0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07,
            0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f, 0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d,
            0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef, 0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb,
            0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61, 0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63,
            0x55, 0x21, 0x0c, 0x7d]

Rcon = (0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a)


def xor(s1, s2):
    return tuple(a ^ b for a, b in zip(s1, s2))


def xor_str(s1, s2):
    return tuple(int(a, 16) ^ int(b, 16) for a, b in zip(s1, s2))


def xor_str_int(s1, s2):
    return tuple(int(a, 16) ^ b for a, b in zip(s1, s2))


def str_to_hex(st):
    return list(map(lambda x1: int(x1, 16), st))


def str_to_hex_arr(stx):
    return [list(map(lambda x1: int(x1, 16), st)) for st in stx]


def int_to_hex(st):
    return list(map(lambda x1: format(x1, '02x'), st))


def split_string(n, st):
    lst = [""]
    for i1 in str(st):
        l = len(lst) - 1
        if len(lst[l]) < n:
            lst[l] += i1
        else:
            lst += [i1]
    return lst


def left_shift(pos, arr):
    left = arr[pos:]
    right = arr[:pos]
    return left + right


def right_shift(pos, arr):
    return left_shift(len(arr) - pos, arr)


def byte_left_shift(word):
    return left_shift(1, word)


def substitute_sbox(word):
    # hex(Sbox[int("20",16)])
    newS = []
    for byt in word:
        newS.append(hex(Sbox[int(byt, 16)])[2:])
    return newS


def substitute_inv_sbox(word):
    # hex(Sbox[int("20",16)])
    newS = []
    for byt in word:
        newS.append(hex(inv_sbox[int(byt, 16)])[2:])
    return newS


def apply_RoundCONstant(word, i1):
    return int_to_hex(xor_str_int(word, (Rcon[i1], 0, 0, 0)))


def apply_round_key(key, plainT):
    newS = []
    for x1, y in zip(key, plainT):
        newS.append(list(xor_str(x1, y)))
    return newS


def to_matrix(X):
    return [[X[j][i1] for j in range(len(X))] for i1 in range(len(X[0]))]


def to_arr(X):
    return [[X[i1][j] for j in range(len(X))] for i1 in range(len(X[0]))]


def flatten(state):
    newS = []
    for x1 in state:
        for y in x1:
            newS.append(y)
    return newS


def unflatten(state):
    newS = []
    for x1 in range(0, 4):
        newS.append(state[x1 * 4:(x1 + 1) * 4])
    return newS


def shift_rows(arr):
    for x1 in range(0, 4):
        arr[x1] = left_shift(x1, arr[x1])
    return arr


def inv_shift_rows(arr):
    for x1 in range(0, 4):
        arr[x1] = right_shift(x1, arr[x1])
    return arr


def pprint(arr):
    for x1 in arr:
        print(int_to_hex(x1))


# Galois Multiplication
# noinspection PyUnusedLocal
def galoisMult(a, b):
    p = 0
    hiBitSet = 0
    for i1 in range(8):
        if b & 1 == 1:
            p ^= a
        hiBitSet = a & 0x80
        a <<= 1
        if hiBitSet == 0x80:
            a ^= 0x1b
        b >>= 1
    return p % 256


def mixColumn(column):
    temp = copy(column)
    column[0] = galoisMult(temp[0], 2) ^ galoisMult(temp[3], 1) ^ galoisMult(temp[2], 1) ^ galoisMult(temp[1], 3)
    column[1] = galoisMult(temp[1], 2) ^ galoisMult(temp[0], 1) ^ galoisMult(temp[3], 1) ^ galoisMult(temp[2], 3)
    column[2] = galoisMult(temp[2], 2) ^ galoisMult(temp[1], 1) ^ galoisMult(temp[0], 1) ^ galoisMult(temp[3], 3)
    column[3] = galoisMult(temp[3], 2) ^ galoisMult(temp[2], 1) ^ galoisMult(temp[1], 1) ^ galoisMult(temp[0], 3)


def mixColumnInv(column):
    temp = copy(column)
    column[0] = galoisMult(temp[0], 14) ^ galoisMult(temp[3], 9) ^ galoisMult(temp[2], 13) ^ galoisMult(temp[1], 11)
    column[1] = galoisMult(temp[1], 14) ^ galoisMult(temp[0], 9) ^ galoisMult(temp[3], 13) ^ galoisMult(temp[2], 11)
    column[2] = galoisMult(temp[2], 14) ^ galoisMult(temp[1], 9) ^ galoisMult(temp[0], 13) ^ galoisMult(temp[3], 11)
    column[3] = galoisMult(temp[3], 14) ^ galoisMult(temp[2], 9) ^ galoisMult(temp[1], 13) ^ galoisMult(temp[0], 11)


def mixColumns(state):
    for i1 in range(4):
        column = []
        # create the column by taking the same item out of each "virtual" row
        for j in range(4):
            column.append(state[j * 4 + i1])
        # apply mixColumn on our virtual column
        mixColumn(column)
        # transfer the new values back into the state table
        for j in range(4):
            state[j * 4 + i1] = column[j]
    return state


def mixColumnsInv(state):
    for i1 in range(4):
        column = []
        # create the column by taking the same item out of each "virtual" row
        for j in range(4):
            column.append(state[j * 4 + i1])
        mixColumnInv(column)
        for j in range(4):
            state[j * 4 + i1] = column[j]
        return state


input_key = "21a8617473206d79204b756e6720c671"
input_key = input_key.rstrip().replace(" ", "")
words = split_string(8, input_key)
words = [split_string(2, word) for word in words]
input_plain = ""
input_plain = input_plain.rstrip().replace(" ", "").lower()
plain = split_string(8, input_plain)
plain = [split_string(2, word) for word in plain]


def key_expansion_core(word, i1):
    leftShift = byte_left_shift(word)
    applied_sbox = substitute_sbox(leftShift)
    applied_roundConstant = apply_RoundCONstant(applied_sbox, i1)
    return applied_roundConstant


key_round = 0
for i in range(4, 48):
    if i % 4 != 0:
        generated_word = xor_str(words[i - 4], words[i - 1])
        words.append(int_to_hex(generated_word))
    else:
        generated_word = xor_str(words[i - 4], key_expansion_core(words[i - 1], key_round + 1))
        words.append(int_to_hex(generated_word))
        key_round += 1
new = []
keys = []
for x in range(len(words)):
    if x == 0 or x % 4 == 0:
        count = 0
        # print(new)
        if len(new):
            keys.append(new)
            final = [''.join(x) for x in new]
            final = ''.join(final)
            spaced = split_string(2, final)
            final = ' '.join(spaced)
        new = []
    new.append(words[x])


def aes_round(state, roundKey):
    state = substitute_sbox(int_to_hex(flatten(state)))
    state = shift_rows(to_matrix(unflatten(state)))
    state = str_to_hex_arr(state)
    state = mixColumns(flatten(state))
    state = unflatten(int_to_hex(state))
    state = apply_round_key(roundKey, state)
    return state


def inverse_aes_round(state, roundKey):
    state = unflatten(int_to_hex(flatten(state)))
    state = apply_round_key(roundKey, state)
    state = flatten(state)
    state = mixColumns(state)
    state = unflatten(state)
    state = shift_rows(to_matrix(state))
    state = substitute_inv_sbox(int_to_hex(flatten(state)))
    return state
