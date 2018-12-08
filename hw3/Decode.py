import sys
import numpy as np
import itertools

def get_parameters():
    if len(sys.argv) != 4: raise Exception("Should pass exactly 3 parameters, passed: {0}".format(len(sys.argv) - 1))
    return sys.argv[1], sys.argv[2], sys.argv[3]


def decode(cx_file_name, input_file_name, output_file_name):
    with open(cx_file_name, 'r') as cxfile, open(input_file_name, 'rb') as rfile, open(output_file_name, 'wb') as wfile:
        lines = [line.rstrip('\n') for line in cxfile]
        params = lines[0].split(' ')
        lines = lines[1:]
        n = int(params[0])
        k = int(params[1])


        matrix = np.array([ np.array([int(c) for c in line]) for line in lines[:k]])
        lines = lines[k:]
        dict = {}
        for line in lines:
            parts = line.split(':')
            syn, code = parts[0], parts[1]
            dict[syn] = code


        file_data = ''
        current_token = ''
        while True:
            symbols = rfile.read(1)
            if not symbols: break
            byte = symbols[0]

            for i in reversed(range(8)):
                bit = '1' if (byte & (1<<i)) else '0'
                if (bit == '1'):
                    file_data += current_token
                    current_token = bit
                else:
                    current_token += bit

        new_data = ''
        for i in range(int(len(file_data) / n)):
            part = file_data[i*n : (i+1)*n]
            vec = np.array([int(c) for c in part]).reshape((-1, 1))
            res = matrix.dot(vec) % 2
            syn = ''.join([str(c[0]) for c in res])

            if not syn in dict:
                pass
                # print("syn not in dict, smth wrong")
            else:
                code = dict[syn]
                arr = np.array([int(c) for c in code]).reshape((-1, 1))
                vec = (vec - arr) % 2
                res = ''.join([str(v[0]) for v in vec])
                new_data +=  res


        print(new_data)
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
    cx_file_name, input_file_name, output_file_name = get_parameters()
    decode(cx_file_name, input_file_name, output_file_name)


if __name__ == "__main__":
    main()
