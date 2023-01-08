import math


def write_compressed_data(result: [str], code_size: int):
    output = ""
    for m in result:
        output += m.zfill(code_size)
    return bytes(output, "utf-8")


def convert_int_to_bits(number, code_size):
    return bytes((bin(5)[2:]).zfill(code_size), 'utf-8')


def initialize_code_table(color_table_size):
    table_size = int(math.pow(color_table_sizes, 2))
    table = {i: i for i in range(table_size)}
    table[table_size] = table_size
    table_size += 1
    table[table_size] = table_size
    table_size += 1
    return table, table_size


def update_code_size(table_size, code_size):
    if table_size == math.pow(2, code_size) - 1:
        code_size += 1

def encode(data: bytes, color_table_size, code_size):
    """
    the table code look like this:
    ______|_____
      #0  |  0
      #1  |  1
      #2  |  2
      #3  |  3
    """
    string_data = data.decode()
    table, table_size = initialize_code_table(color_table_size)
    update_code_size(table_size, code_size)

    num_of_bits = int(math.pow(code_size, 2) - 1)
    clear_code = table[-2]
    end_of_information_code = table[-1]

    compress_data = b''
    compress_data += convert_int_to_bits(clear_code, code_size)
    prev = None

    for bit in string_data:
        last_and_current = prev + bit
        if last_and_current in table:
            prev = last_and_current
        else:
            output.append(table[prev])
            table[last_and_current] = convert_int_to_bstring(table_size, 0)
            table_size += 1
            prev = bit
    output.append(table[prev])

    code_size = math.ceil(math.log(table_size, 2))
    return write_compressed_data(output, code_size), code_size


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
    com_data, c_s = encode(input_bytes)
    print(com_data, c_s)
    output_bytes = decode(com_data, c_s)
    if output_bytes == input_bytes:
        print("Great you are the best!!!\ninput_bytes = ", input_bytes, "output_bytes = ", output_bytes)
    else:
        print("Error!!!!!!!!!!!!!!")
