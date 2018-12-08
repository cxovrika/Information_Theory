import sys
import numpy as np


def get_parameters():
    if len(sys.argv) != 3: raise Exception("Should pass exactly 2 parameter, passed: {0}".format(len(sys.argv) - 1))
    return sys.argv[1], sys.argv[2]


def parity_check(input_file_name, output_file_name):
    with open(input_file_name, 'r') as rfile, open(output_file_name, 'w') as wfile:
        lines = [line.rstrip('\n') for line in rfile]
        params = lines[0].split(' ')
        lines = lines[1:]
        n = int(params[0])
        k = int(params[1])

        matrix = np.array([ np.array([int(c) for c in line]) for line in lines])
        positions = [i for i in range(n)]

        for i in range(k):
            if matrix[i, i] == 0:

                found = False
                for l in range(i + 1, k):
                    if matrix[l, i] == 1:
                        matrix[[i, l]] = matrix[[l, i]]
                        found = True
                        break

                if not found:
                    for j in range(i + 1, n):
                        if matrix[i, j] == 1:
                            matrix[:, [i, j]] = matrix[:, [j, i]]
                            positions[i], positions[j] = positions[j], positions[i]
                            break

            for l in range(k):
                if matrix[l, i] == 1 and l != i:
                    matrix[l, :] -= matrix[i, :]
                    matrix[l, :] %= 2

        indexes = np.argsort(positions)

        xirtam = matrix[:, k:]
        xirtam = xirtam.transpose()
        xirtam = np.concatenate((xirtam, np.identity(n - k, int)), axis = 1)

        xirtam = xirtam[:, indexes]

        wfile.write('{0} {1}\n'.format(n, n - k))

        for i in range(n-k):
            line = ''.join([str(xirtam[i, j]) for j in range(n)])
            wfile.write(line + '\n')


def main():
    input_file_name, output_file_name = get_parameters()
    parity_check(input_file_name, output_file_name)


if __name__ == "__main__":
    main()
