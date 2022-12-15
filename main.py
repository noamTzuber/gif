# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import math
import struct
import sys

from bitstring import BitArray

#
# def decimalToBinary(n):
#     return "{0:b}".format(int(n))
#


#
# def encode(bytes_input):
#     # gif_bytes = read_gif_image() --input
#     bytes_s = b'10101010'
#     pre_compressed_data = []
#     last_byte = b''
#     table_size = 1
#     table = {b'0': 0}
#
#     for i in bytes_s:
#         current_byte = bytes([i])
#         last_and_current = last_byte + current_byte
#         if last_and_current in table:
#             last_byte = last_and_current
#         else:
#             pre_compressed_data.append(table[last_byte])
#             table[last_and_current] = table_size
#             table_size += 1
#             last_byte = current_byte
#     pre_compressed_data.append(table[last_byte])
#
#     code_size = math.ceil(math.log(table_size, 2))
#
#     compressed = write_compressed_data(pre_compressed_data, code_size), code_size
#     return compressed, code_size
#

# def devide_compressed_data(input, code_size):
#     return [input[i:i + code_size] for i in range(0, len(input), code_size)]

#
# def decode(input_compressed, code_size):
#     compressed_data = [int(input_compressed[i:i + code_size], 2) for i in range(0, len(input_compressed), code_size)]
#     decompressed_data = ""
#     table_size = 256
#
#     table = {i: chr(i) for i in range(table_size)}
#
#     for i in range(len(compressed_data) - 1):
#         next_item = table[compressed_data[i + 1]][0]
#         decompressed_data += table[compressed_data[i]]
#         table[table_size] = table[compressed_data[i]] + next_item
#         table_size += 1
#     decompressed_data += table[compressed_data[-1]]
#     return decompressed_data
#

# def print_information(compressed_data, code_size):
#     print("original bytes:", ("".join([bin(ord(c))[2:] for c in string])))
#     print("number of original bytes:", len(bin(int.from_bytes(bytes(string, "utf-8"), "big"))))
#     print("compressed bytes:", compressed_data)
#     print("number of compressed bytes:", len(compressed_data))
#     print("after decode:", decode(compressed_data, code_size))
#

def write_compressed_data(result, code_size):
    output = ""
    for m in result:
        output += bin(m)[2:].zfill(code_size)
    return bytes(output, "utf-8")


def encode_test(input_bytes: bytes):
    input_b = input_bytes.decode()
    string = ""
    result = []

    table_size = 2
    table = {"0": 0, "1": 1}

    for i in range(len(input_b)):
        string_and_item = string + input_b[i]
        if string_and_item in table:
            string = string_and_item
        else:
            result.append(table[string])
            table[string_and_item] = table_size
            table_size += 1
            string = input_b[i]
    result.append(table[string])

    code_size = math.ceil(math.log(table_size, 2))
    return write_compressed_data(result, code_size), code_size


def convert_int_to_bstring(number: int, code_size: int) -> str:
    return str((bin(number))[2:]).zfill(code_size)


def decode_test1(input_compressed, code_size):
    compressed_string = input_compressed.decode()
    compressed_data = [compressed_string[i:i + code_size] for i in range(0, len(compressed_string), code_size)]
    decompressed_data = ""
    table_size = 2

    zero_table = "0".zfill(code_size)
    one_table = "1".zfill(code_size)

    table = {zero_table: "0", one_table: "1"}

    for i in range(len(compressed_data) - 1):
        next_item = compressed_data[i + 1]
        current_item = compressed_data[i]

        decompressed_data += table[current_item]

        table[convert_int_to_bstring(table_size,code_size)] = table[current_item] + table[next_item]
        table_size += 1
    decompressed_data += table[compressed_data[-1]]
    return bytes(decompressed_data, "utf-8")


def decode_test(input_compressed, code_size):
    compressed_string = input_compressed.decode()
    compressed_data = [compressed_string[i:i + code_size] for i in range(0, len(compressed_string), code_size)]
    decompressed_data = ""
    table_size = 2

    zero_table = "0".zfill(code_size)
    one_table = "1".zfill(code_size)

    table = {zero_table: "0", one_table: "1"}

    for i in range(len(compressed_data) - 1):
        next_item = compressed_data[i + 1]
        current_item = compressed_data[i]
        if next_item not in table:
            table[convert_int_to_bstring(table_size, code_size)] = table[current_item] + table[current_item][:code_size]
            table_size += 1

    decompressed_data += table[compressed_data[-1]]
    return bytes(decompressed_data, "utf-8")
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    c, f = encode_test(b'1000101010')
    print()
    print("bytes =", type(c), "codesize = ", type(f))
    print(decode_test(c, f))
    # compressed_data, code_size = encode(bytes)
    # print_information(compressed_data, code_size)
