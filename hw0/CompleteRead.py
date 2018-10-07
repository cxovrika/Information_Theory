import sys

def get_parameters():
    if len(sys.argv) != 3: raise Exception("Should pass exactly 2 parameters, passed: {0}".format(len(sys.argv) - 1))
    return sys.argv[1], sys.argv[2]

def complete_read(input_file_name, output_file_name):
    with open(input_file_name, 'rb') as rfile, open(output_file_name, 'w') as wfile:

        current_token = ''
        while True:
            symbols = rfile.read(1)
            if not symbols: break
            byte = symbols[0]

            for i in reversed(range(8)):
                bit = '1' if (byte & (1<<i)) else '0'
                if (bit == '1'):
                    wfile.write(current_token)
                    current_token = bit
                else:
                    current_token += bit

def main():
    input_file_name, output_file_name = get_parameters()
    complete_read(input_file_name, output_file_name)

if __name__ == "__main__":
    main()
