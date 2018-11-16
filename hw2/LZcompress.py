import sys
import math


def get_bits_from_number(num, bitcount = 8):
    bits = []
    for _ in range(bitcount):
        bits.insert(0, str(num % 2))
        num = int(num / 2)
    return bits

def get_file_length_and_bitstream(rfile):
    file_length = 0
    bitstream = []

    while True:
        bytes = rfile.read(1)
        if not bytes: break;

        file_length += 1
        byte = bytes[0]
        bits = get_bits_from_number(byte)
        bitstream.extend(bits)

    return file_length, bitstream

def get_length_bits(file_length):
    binary_length = "{0:b}".format(file_length)
    return ['0'] * (len(binary_length) - 1) + list(binary_length)


def update_data_with_chunk(compressed_bits, lexicon, chunk):
    bitcount = math.ceil(math.log2((len(lexicon))))
    bitarray = get_bits_from_number(lexicon[chunk], bitcount)
    compressed_bits.extend(bitarray)

    lexicon[chunk + '1'] = len(lexicon)
    lexicon[chunk + '0'] = lexicon.pop(chunk)

def get_compressed_bits(bitstream):
    compressed_bits = []
    lexicon = {'0' : 0, '1' : 1}

    cur_chunk = ''
    for bit in bitstream:
        cur_chunk += bit
        if cur_chunk in lexicon:
            update_data_with_chunk(compressed_bits, lexicon, cur_chunk)
            cur_chunk = ''

    if len(cur_chunk) > 0:
        while cur_chunk not in lexicon: cur_chunk += '0'
        update_data_with_chunk(compressed_bits, lexicon, cur_chunk)

    return compressed_bits


def make_bitarray_byte_divisible(bitarray):
    bitarray.append('1')
    k = len(bitarray) % 8
    k = (8 - k) % 8
    bitarray.extend(['0'] * k)

def write_bits_to_file(bitarray, wfile):
    make_bitarray_byte_divisible(bitarray)
    for i in range(int(len(bitarray) / 8)):
        bitstring = ''.join(bitarray[8*i : 8*(i+1)])
        wfile.write(bytes([int(bitstring, 2)]))


def compress(input_file_name, output_file_name):
    with open(input_file_name, 'rb') as rfile, open(output_file_name, 'wb') as wfile:
        file_length, bitstream = get_file_length_and_bitstream(rfile)
        length_bits = get_length_bits(file_length)
        compressed_bits = get_compressed_bits(bitstream)

        write_bits_to_file(length_bits + compressed_bits, wfile)

def get_parameters():
    if len(sys.argv) != 3: raise Exception("Should pass exactly 2 parameters, passed: {0}".format(len(sys.argv) - 1))
    return sys.argv[1], sys.argv[2]

def main():

    input_file_name, output_file_name = get_parameters()
    compress(input_file_name, output_file_name)

if __name__ == "__main__":
    main()
