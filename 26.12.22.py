
def lzw_decode(compressed_data):
    # Initialize the dictionary with the entries for all single-byte values
    dictionary = {i: chr(i) for i in range(256)}

    # Initialize the output string and the current entry
    output = ""
    current_entry = compressed_data[0]
    output += current_entry

    # Iterate through the compressed data, one entry at a time
    for i in range(1, len(compressed_data)):
        next_entry = compressed_data[i]

        # If the next entry is a single-byte value, add it to the output string
        if next_entry in dictionary:
            sequence = dictionary[next_entry]
        # Otherwise, use the dictionary to look up the sequence for the current entry
        else:
            sequence = dictionary[current_entry] + current_entry

        output += sequence

        # Add the current entry and the last single-byte value to the dictionary
        dictionary[max(dictionary.keys()) + 1] = dictionary[current_entry] + sequence[0]

        current_entry = next_entry

    return output


if __name__ == '__main__':
    import io

    print(lzw_decode(""))
