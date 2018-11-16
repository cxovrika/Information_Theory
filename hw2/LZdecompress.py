import sys
import math

def get_bits_from_number(num, bitcount = 8):
    bits = []
    for _ in range(bitcount):
        bits.insert(0, str(num % 2))
        num = int(num / 2)
    return bits

def get_file_bitstream(rfile):
    bitstream = []

    while True:
        bytes = rfile.read(1)
        if not bytes: break;

        byte = bytes[0]
        bits = get_bits_from_number(byte)
        bitstream.extend(bits)

    return bitstream

def unpack_bitstream_length_prefix(bitstream):
    cur_index = 0
    for bit in bitstream:
        if bit == '1':
            length_bits = bitstream[cur_index : 2*cur_index + 1]
            file_length = int(''.join(length_bits), 2)
            return file_length, bitstream[2*cur_index + 1:]
        cur_index += 1

    print("Something wrong happened while getting length as prefix!!!")


def get_decompresseed_bits(file_length, bitstream):
    decompressed_bits = []
    lexicon = ['0', '1']

    cur_index = 0
    while cur_index < len(bitstream):
        bitcount = math.ceil(math.log2((len(lexicon))))
        cur_chunk = ''.join(bitstream[cur_index : cur_index + bitcount])

        index = int(cur_chunk, 2)
        decompressed_bits.extend(list(lexicon[index]))

        lexicon.append(lexicon[index] + '1')
        lexicon[index] += '0'
        cur_index += bitcount

    return decompressed_bits[: 8*file_length]


def write_bits_to_file(bitarray, wfile):
    for i in range(int(len(bitarray) / 8)):
        bitstring = ''.join(bitarray[8*i : 8*(i+1)])
        wfile.write(bytes([int(bitstring, 2)]))

def decompress(input_file_name, output_file_name):
    with open(input_file_name, 'rb') as rfile, open(output_file_name, 'wb') as wfile:
        bitstream = get_file_bitstream(rfile)
        while bitstream.pop() != '1': pass #removing dummy suffix

        file_length, bitstream = unpack_bitstream_length_prefix(bitstream)
        decompressed_bits = get_decompresseed_bits(file_length, bitstream)

        write_bits_to_file(decompressed_bits, wfile)


def get_parameters():
    if len(sys.argv) != 3: raise Exception("Should pass exactly 2 parameters, passed: {0}".format(len(sys.argv) - 1))
    return sys.argv[1], sys.argv[2]

def main():

    input_file_name, output_file_name = get_parameters()
    decompress(input_file_name, output_file_name)

if __name__ == "__main__":
    main()
