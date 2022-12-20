import math


def write_compressed_data(result: [str], code_size: int):
    output = ""
    for m in result:
        output += m.zfill(code_size)
    return bytes(output, "utf-8")


def convert_int_to_bstring(number: int, code_size: int) -> str:
    return str((bin(number))[2:]).zfill(code_size)


def encode(data: bytes):
    # for Hex
    # string_data = ''.join('{:08b}'.format(b) for b in data)
    # for Binary
    string_data = data.decode()
    table = {"0": "0", "1": "1"}
    prev = ""
    output = []
    table_size = 2
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
    return write_compressed_data(output, code_size) , code_size

def decode(data: bytes, code_size: int):
    string_data = data.decode()

    zero_table = "0".zfill(code_size)
    one_table = "1".zfill(code_size)

    table = {zero_table: "0", one_table: "1"}


    decompressed_data = ""
    table_size = 2
    compressed_data = [string_data[i:i + code_size] for i in range(0, len(string_data), code_size)]

    length=len(compressed_data)-1
    for i in range(length):
        curr_item = table[compressed_data[i]]

        if not(compressed_data[i + 1] in table):
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
    input= b'111111010000000000000111111'
    com_data, c_s =encode(input)
    print(com_data, c_s)
    output = decode(com_data,c_s)
    if output == input:
        print("O.k you r th best!!!\ninput = ", input, "output = ", output)
    else:
        print("Error!!!!!!!!!!!!!!")

