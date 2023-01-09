import math

from bitstring import ConstBitStream


def write_compressed_data(result: [str], code_size: int):
    output = ""
    for m in result:
        output += m.zfill(code_size)
    return bytes(output, "utf-8")


def convert_int_to_bits(number, code_size):
    return bytes((bin(number)[2:]).zfill(code_size), 'utf-8')


def initialize_code_table(color_table_size):
    table_size = color_table_size
    table = {str(i): i for i in range(color_table_size)}
    table[str(table_size)] = table_size
    table_size += 1
    table[str(table_size)] = table_size
    table_size += 1
    return table


def update_writing_size(table_size, writing_size):
    if table_size == int(math.pow(2, writing_size)) + 1:
        return writing_size + 1
    return writing_size

def flip_data(compress_data):
    ordered_data = b''
    length = len(compress_data)/8
    for i in range(int(length)):
        ordered_data += compress_data[-8:]
        compress_data = compress_data[:-8]
    return ordered_data

def encode(data: bytes, color_table_size):
    """
    the table code look like this:
    ______|_____
      #0  |  0
      #1  |  1
      #2  |  2
      #3  |  3
    """
    # line 1 = 001001001001001010010010010010001001001001001010010010010010001001001001001010010010010010001001001000000000000010010010001001001000000000000010010010010010010000000000000001001001010010010000000000000001001001010010010010010001001001001001010010010010010001001001001001010010010010010001001001001001

    stream = ConstBitStream('0x24929248924A492249292489200092248002492400049490001252491249492449252491249')
    reading_size = math.ceil(math.log(color_table_size + 1)) + 1
    writing_size = reading_size
    table = initialize_code_table(color_table_size)
    update_writing_size(len(table), writing_size)

    clear_code = table[str(len(table)-2)]
    end_of_information_code = table[str(len(table)-1)]

    compress_data = b''
    compress_data += convert_int_to_bits(clear_code, reading_size)

    # pos = stream.length - reading_size + 1
    # stream.pos = pos
    length = stream.length
    curr_el = stream.read('bin' + str(reading_size))
    curr_el = str(int(curr_el, 2))

    # pos = pos - reading_size
    print(length)
    while stream.pos != (length):
        print(stream.pos)
        # stream.pos = pos
        next_el = stream.read('bin' + str(reading_size))
        next_el = str(int(next_el, 2))
        current_and_next = next_el + "," + curr_el

        if current_and_next in table:
            curr_el = current_and_next
        else:
            compress_data = convert_int_to_bits(table[curr_el], writing_size) + compress_data
            table[current_and_next] = len(table)
            writing_size = update_writing_size(len(table), writing_size)
            curr_el = next_el

    compress_data = convert_int_to_bits(table[curr_el], writing_size) + compress_data
    compress_data = convert_int_to_bits(end_of_information_code, writing_size) + compress_data
    if zero_fill := len(compress_data) % 8:
        compress_data = convert_int_to_bits(0, zero_fill) + compress_data

    return_data = flip_data(compress_data)

    return return_data


def decode(data: bytes, code_size: int):
    string_data = data.decode()

    zero_table = "0".zfill(code_size)
    one_table = "1".zfill(code_size)

    table = {zero_table: "0", one_table: "1"}

    decompressed_data = ""
    table_size = 2
    compressed_data = [string_data[i:i + code_size] for i in range(0, len(string_data), code_size)]

    length = len(compressed_data) - 1
    for i in range(length):
        curr_item = table[compressed_data[i]]

        if not (compressed_data[i + 1] in table):
            table[convert_int_to_bstring(table_size, code_size)] = curr_item + curr_item[0]
        else:
            next_item = table[compressed_data[i + 1]][0]
            table[convert_int_to_bstring(table_size, code_size)] = curr_item + next_item
        table_size += 1
        decompressed_data += curr_item
    decompressed_data += table[compressed_data[length]]
    return bytes(decompressed_data, "utf-8")


if __name__ == '__main__':
    import io

    # Open the file in binary mod
    input_bytes = b'1110101111010000001100000000101001011010100101010001011111111'
    com_data = encode(input_bytes, 4)

    # output_bytes = decode(com_data, c_s)
    # if output_bytes == input_bytes:
    #     print("Great you are the best!!!\ninput_bytes = ", input_bytes, "output_bytes = ", output_bytes)
    # else:
    #     print("Error!!!!!!!!!!!!!!")
