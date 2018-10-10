import sys
import collections as COL
import math

characters = ' აბგდევზთიკლმნოპჟრსტუფქღყშჩცძწჭხჯჰ'

def get_parameters():
    if len(sys.argv) != 4: raise Exception("Should pass exactly 3 parameters, passed: {0}".format(len(sys.argv) - 1))
    return sys.argv[1], sys.argv[2], sys.argv[3]

def compress(codes_file, input_file_name, output_file_name):
    with open(codes_file, 'r', encoding='UTF-8') as cfile,\
            open(input_file_name, 'r', encoding='UTF-8') as rfile,\
            open(output_file_name, 'wb') as wfile:

        code_lines = [line.rstrip('\n') for line in cfile]
        codes = {}
        for i in range(len(characters)):
            codes[characters[i]] = code_lines[i]


        whole_code = [b for c in rfile.read() for b in codes[c]]
        # print(whole_code)
        while True:
            byte = 0
            current_size = 0
            for i in reversed(range(8)):
                if len(whole_code) == 0:
                    wfile.write(bytes([byte | (1<<i)]))
                    return
                symbol = whole_code.pop(0)
                if symbol == '1': byte |= (1<<i)

            wfile.write(bytes([byte]))


def main():
    codes_file, input_file_name, output_file_name = get_parameters()
    compress(codes_file, input_file_name, output_file_name)


if __name__ == "__main__":
    main()
