import sys

def get_parameters():
    if len(sys.argv) != 3: raise Exception("Should pass exactly 2 parameters, passed: {0}".format(len(sys.argv) - 1))
    return sys.argv[1], sys.argv[2]

def simple_write(input_file_name, output_file_name):
    with open(input_file_name, 'r') as rfile, open(output_file_name, 'wb') as wfile:
        while True:
            byte = 0
            current_size = 0
            for i in reversed(range(8)):
                symbol = rfile.read(1)
                if not symbol:
                    wfile.write(bytes([byte | (1<<i)]))
                    return
                if symbol == '1': byte |= (1<<i)

            wfile.write(bytes([byte]))

def main():
    input_file_name, output_file_name = get_parameters()
    simple_write(input_file_name, output_file_name)

if __name__ == "__main__":
    main()
