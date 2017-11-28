def read_input():
    choice = int(input("Enter 0 to read in your own message, or 1 to read a file: "))
    if choice == 0:
        message_input = input("Please input your string to be decoded via LZW: \n")
        message_input += "#"
        list_message = list(message_input)
        return list_message, choice
    elif choice == 1:
        name = input("Please enter the file name to be decoded via LZW: \n")
        return name, choice
    else:
        quit()


def get_norm_encoding(inp_message):
    reg_encoding = []
    for letter in inp_message:
        reg_encoding.append(ord(letter) - ord('a'))
    return reg_encoding


def get_analytics(inp_message, norm_encoding, my_encoding):
    message_length = float(len(inp_message))
    norm_length = float(len(norm_encoding))
    my_length = float(len(my_encoding))
    print("The length reduction was %.2f%% from the original message. \n" % (((message_length-my_length)/message_length)*100))
    print("The length reduction was %.2f%% from the normal encoding." % (((norm_length - my_length) / norm_length)*100))


def decode(dictionary, encodedfile_name):
    with open(encodedfile_name, "r") as f:
        with open('decodedfile.txt', "a") as g:
            while f.read(f.seek(0, 1)) != "":
                output = ""
                while f.read(f.seek(0, 1)) != ",":
                    output += f.read(1)
                    f.seek(1, 1)
                if output in dictionary.items():
                    text = dictionary[output]
                    g.write(text)
                else:
                    print("An exception occurred with the value %s" % output)
                f.seek(1, 1)
    f.close()
    g.close()

input_1, input_2 = read_input()

if input_2 == 0:
    message_list = input_1
    i = 0
    initDict = {}

    for char in message_list:
        if char not in initDict.values():
            initDict[i] = char
            i += 1

    inv_dict = {}
    if initDict:
        inv_dict = {v: k for k, v in initDict.items()}

    encoding = []
    char = 0
    current_str = message_list[char]

    while message_list[char+1] != "#":
        char += 1
        if current_str+message_list[char] in initDict.values():
            current_str += message_list[char]
        else:
            encoding.append(inv_dict[current_str])
            initDict[i] = current_str+message_list[char]
            inv_dict[current_str+message_list[char]] = i
            i += 1
            current_str = message_list[char]

    encoding.append(inv_dict[current_str])

    print(encoding)
    regular_encoding = get_norm_encoding(message_list)
    print(regular_encoding)
    get_analytics(message_list, regular_encoding, encoding)

elif input_2 == 1:
    with open(input_1, "r") as file:
        with open("encodedfile.txt", "a") as file2:
            message = file.read()
            message += '#'
            message_list = list(message)

            i = 0
            initDict = {}

            for char in message_list:
                if char not in initDict.values():
                    initDict[i] = char
                    i += 1

            inv_dict = {}
            if initDict:
                inv_dict = {v: k for k, v in initDict.items()}

            encoding = []
            char = 0
            current_str = message_list[char]

            while message_list[char + 1] != "#":
                char += 1
                if current_str + message_list[char] in initDict.values():
                    current_str += message_list[char]
                else:
                    file2.write(str(inv_dict[current_str]))
                    file2.write("\n")
                    initDict[i] = current_str + message_list[char]
                    inv_dict[current_str + message_list[char]] = i
                    i += 1
                    current_str = message_list[char]

            file2.write(str(inv_dict[current_str]))

        #regular_encoding = get_norm_encoding(message_list)
        #get_analytics(message_list, regular_encoding, encoding)
        print("Compression has finished.")
    file.close()
    creation = input("Would you like to create a decoded file? Enter 1 if yes, 0 otherwise: ")
    if creation == 1:
        decode(initDict, "encodedfile.txt")
    else:
        file2.close()
