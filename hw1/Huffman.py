import sys
import collections as COL
import math

def get_parameters():
    if len(sys.argv) != 3: raise Exception("Should pass exactly 2 parameters, passed: {0}".format(len(sys.argv) - 1))
    return sys.argv[1], sys.argv[2]

def generate_huffman_codes(input_file_name, output_file_name):
    with open(input_file_name, 'r', encoding='UTF-8') as rfile, open(output_file_name, 'w', encoding='UTF-8') as wfile:
        n = int(rfile.readline());
        sizes = [float(x) for x in rfile.readline().split(' ')]

        codes = COL.defaultdict(lambda:[])
        nodes = [[sizes[i], [i]] for i in range(n)]

        while len(nodes) > 1:
            nodes = sorted(nodes, key=lambda x:(x[0]))
            frst = nodes.pop(0)
            scnd = nodes.pop(0)

            for x in frst[1]: codes[x].append('0')
            for x in scnd[1]: codes[x].append('1')

            thrd = [frst[0] + scnd[0], frst[1] + scnd[1]]
            nodes.insert(0, thrd)

        for i in range(n):
            wfile.write('%s\n' % ''.join(reversed(codes[i])))


def main():
    input_file_name, output_file_name = get_parameters()
    generate_huffman_codes(input_file_name, output_file_name)


if __name__ == "__main__":
    main()
