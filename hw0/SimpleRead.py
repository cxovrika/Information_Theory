import sys
import struct

def get_parameters():
    if len(sys.argv) != 3: raise Exception("Should pass exactly 2 parameters, passed: {0}".format(len(sys.argv) - 1))
    return sys.argv[1], sys.argv[2]

def simple_read(input_file_name, output_file_name):
    with open(input_file_name, 'rb') as rfile, open(output_file_name, 'w') as wfile:
        while True:
            symbol = rfile.read(1)
            if not symbol: break
            byte = ord(symbol)

            for i in reversed(range(8)):
                bit = '1' if (byte & (1<<i)) else '0'
                wfile.write(bit)


def main():
    input_file_name, output_file_name = get_parameters()
    simple_read(input_file_name, output_file_name)

if __name__ == "__main__":
    main()
