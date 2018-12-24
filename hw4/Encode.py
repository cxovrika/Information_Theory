import sys
import numpy as np

def get_parameters():
    if len(sys.argv) != 4: raise Exception("Should pass exactly 3 parameters, passed: {0}".format(len(sys.argv) - 1))
    return sys.argv[1], sys.argv[2], sys.argv[3]



def encode(input_file_name, pol_file_name, output_file_name):
    with open(input_file_name, 'r') as rfile, open(pol_file_name, 'r') as pfile, open(output_file_name, 'w') as wfile:
        lines = [line.rstrip('\n') for line in rfile]
        p = int(lines[0])
        n = int(lines[1])
        g = [int(c) for c in lines[2].split(' ')]
        g = remove_suffix_zeros(g)

        lines = [line.rstrip('\n') for line in pfile]
        k_in = int(lines[0])
        inp = [int(c) for c in lines[1].split(' ')]
        h = n - len(g) + 1
        matrix =   np.array([np.array([0 for j in range(n)]) for i in range(h)])
        for i in range(h):
            for j in range(len(g)):
                matrix[i, j + i] = g[j]

        result = []
        for chunk in chunks(inp, h):
            chunk = np.array(chunk)
            chunk = chunk.dot(matrix) % p
            result.extend(list(chunk))
            print(chunk)

        wfile.write('{0}\n'.format(len(result)))
        wfile.write(' '.join([str(x) for x in result]))

def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


def remove_suffix_zeros(a):
    cp = [x for x in a]
    while len(cp) > 0 and cp[-1] == 0:
        cp.pop()
    return cp

def main():
    input_file_name, pol_file_name, output_file_name = get_parameters()
    encode(input_file_name, pol_file_name, output_file_name)

if __name__ == "__main__":
    main()
