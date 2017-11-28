import struct


def lzw(input_file, output_file):

    dict_size = 256
    dictionary = {chr(i): i for i in range(dict_size)}
    old_str = ""

    with open(input_file, "r") as file:
        with open(output_file, "wb") as file2:

            message = file.read()

            for c in message:
                new_str = old_str + c
                if new_str in dictionary:
                    old_str = new_str
                else:
                    file2.write(struct.pack('1I', dictionary[old_str]))
                    #file2.write(bytes("\n"))
                    dictionary[new_str] = dict_size
                    dict_size += 1
                    old_str = c
            if old_str:
                file2.write(struct.pack('1I', dictionary[old_str]))

            return

to_encode = input("Enter in the .txt file you'd like to compress: ")
lzw(to_encode, 'encoded.txt')
print("Compression has terminated.")
