# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import math
import struct
import sys


def decimalToBinary(n):
    return "{0:b}".format(int(n))


def write_compressed_data(result, code_size):
    output = ""
    for m in result:
        # convert to binary
        binary_representation = decimalToBinary(m)
        # paddings zero and add to output
        output += binary_representation.zfill(code_size)
    return "".join(output)


def encode(input):
    string = ""
    result = []

    table_size = 256

    table = {chr(i): i for i in range(table_size)}

    for item in input:
        string_and_item = string + item
        if string_and_item in table:
            string = string_and_item
        else:
            result.append(table[string])
            table[string_and_item] = table_size
            table_size += 1
            string = item
    result.append(table[string])

    code_size = math.ceil(math.log(table_size, 2))

    return write_compressed_data(result, code_size), code_size


def devide_compressed_data(input, code_size):
    return [input[i:i + code_size] for i in range(0, len(input), code_size)]


def decode(input, code_size):
    compressed_data = [int(input[i:i + code_size], 2) for i in range(0, len(input), code_size)]
    decompressed_data = ""
    table_size = 256

    table = {i: chr(i) for i in range(table_size)}

    for i in range(len(compressed_data) - 1):
        next_item = table[compressed_data[i + 1]][0]
        decompressed_data += table[compressed_data[i]]
        table[table_size] = table[compressed_data[i]] + next_item
        table_size += 1
    decompressed_data += table[compressed_data[-1]]
    return decompressed_data


def print_information(compressed_data, code_size):
    print("original bytes:", ("".join([bin(ord(c))[2:] for c in string])))
    print("number of original bytes:", len(bin(int.from_bytes(bytes(string, "utf-8"), "big"))))
    print("compressed bytes:", compressed_data)
    print("number of compressed bytes:", len(compressed_data))
    print("after decode:", decode(compressed_data, code_size))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    string = "he installer will first create a customized cygwin environment and then set up opam and OCaml inside this environment. The setup should be easy and fast this way. However, the installer wont allow you to set custom options: proxy configuration, select the initial OCaml version to install, etc. (If possible, the 64-bit version of cygwin is installed. The 32-bit version is no longer recommended)he installer will first create a customized cygwin environment and then set up opam and OCaml inside this environment. The setup should be easy and fast this way. However, the installer wont allow you to set custom options: proxy configuration, select the initial OCaml version to install, etc. (If possible, the 64-bit version of cygwin is installed. The 32-bit version is no longer recommended)he installer will first create a customized cygwin environment and then set up opam and OCaml inside this environment. The setup should be easy and fast this way. However, the installer wont allow you to set custom options: proxy configuration, select the initial OCaml version to install, etc. (If possible, the 64-bit version of cygwin is installed. The 32-bit version is no longer recommended)he installer will first create a customized cygwin environment and then set up opam and OCaml inside this environment. The setup should be easy and fast this way. However, the installer wont allow you to set custom options: proxy configuration, select the initial OCaml version to install, etc. (If possible, the 64-bit version of cygwin is installed. The 32-bit version is no longer recommended)"
    # string ="ththdht"
    compressed_data, code_size = encode(string)
    print_information(compressed_data, code_size)
