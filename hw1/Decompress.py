import sys
import collections as COL
import math

characters = ' აბგდევზთიკლმნოპჟრსტუფქღყშჩცძწჭხჯჰ'

def get_parameters():
    if len(sys.argv) != 4: raise Exception("Should pass exactly 3 parameters, passed: {0}".format(len(sys.argv) - 1))
    return sys.argv[1], sys.argv[2], sys.argv[3]

def compress(codes_file, input_file_name, output_file_name):
    with open(codes_file, 'r', encoding='UTF-8') as cfile,\
            open(input_file_name, 'rb') as rfile,\
            open(output_file_name, 'w', encoding='UTF-8') as wfile:

        code_lines = [line.rstrip('\n') for line in cfile]
        decodes = {}
        for i in range(len(characters)):
            decodes[code_lines[i]] = characters[i]

        current_token = ''
        whole_bits = []
        while True:
            symbols = rfile.read(1)
            if not symbols: break
            byte = symbols[0]

            for i in reversed(range(8)):
                bit = '1' if (byte & (1<<i)) else '0'
                if (bit == '1'):
                    whole_bits += list(current_token)
                    current_token = bit
                else:
                    current_token += bit

        current_token = ''
        for b in whole_bits:
            current_token += b
            if current_token in decodes:
                wfile.write(decodes[current_token])
                current_token = ''


def main():
    codes_file, input_file_name, output_file_name = get_parameters()
    compress(codes_file, input_file_name, output_file_name)


if __name__ == "__main__":
    main()
