import sys
import numpy as np


def get_parameters():
    if len(sys.argv) != 4: raise Exception("Should pass exactly 3 parameters, passed: {0}".format(len(sys.argv) - 1))
    return sys.argv[1], sys.argv[2], sys.argv[3]


def encode(matrix_file_name, input_file_name, output_file_name):
    with open(matrix_file_name, 'r') as mfile, open(input_file_name, 'rb') as rfile, open(output_file_name, 'wb') as wfile:
        lines = [line.rstrip('\n') for line in mfile]
        params = lines[0].split(' ')
        lines = lines[1:]
        n = int(params[0])
        k = int(params[1])

        matrix = np.array([ np.array([int(c) for c in line]) for line in lines])


        current_token = ''
        file_data = ''
        while True:
            symbols = rfile.read(1)
            if not symbols: break
            byte = symbols[0]

            for i in reversed(range(8)):
                bit = '1' if (byte & (1<<i)) else '0'
                file_data += bit

        new_data = ''
        for i in range(int(len(file_data) / k)):
            part = file_data[i*k : (i+1) * k]
            vec = np.array([int(c) for c in part])
            vec = vec.dot(matrix) % 2
            res = ''.join([str(v) for v in vec])
            new_data += res

        pos = 0
        while True:
            byte = 0
            current_size = 0
            for i in reversed(range(8)):
                symbol = new_data[pos] if pos < len(new_data) else None
                pos += 1
                if not symbol:
                    wfile.write(bytes([byte | (1<<i)]))
                    return
                if symbol == '1': byte |= (1<<i)

            wfile.write(bytes([byte]))


def main():
    matrix_file_name, input_file_name, output_file_name = get_parameters()
    encode(matrix_file_name, input_file_name, output_file_name)


if __name__ == "__main__":
    main()
