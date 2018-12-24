import sys

def get_parameters():
    if len(sys.argv) != 3: raise Exception("Should pass exactly 2 parameters, passed: {0}".format(len(sys.argv) - 1))
    return sys.argv[1], sys.argv[2]



def parity_check(input_file_name, output_file_name):
    with open(input_file_name, 'r') as rfile, open(output_file_name, 'w') as wfile:
        lines = [line.rstrip('\n') for line in rfile]
        p = int(lines[0])
        n = int(lines[1])

        g = [int(c) for c in lines[2].split(' ')]
        t = [0 for i in range(n + 1)]
        t[0] = p - 1
        t[n] = 1
        result, reminder = pol_div(t, g, n, p)
        result = fill_suffix_zeros(result, n)

        if len(reminder) == 0:
            wfile.write('YES\n')
            wfile.write(' '.join(str(r) for r in result))
        else:
            wfile.write('NO')

def remove_suffix_zeros(a):
    cp = [x for x in a]
    while len(cp) > 0 and cp[-1] == 0:
        cp.pop()
    return cp

def fill_suffix_zeros(a, n):
    while len(a) < n: a.append(0)
    return a

def pol_sum(a, b, n, p):
    a = [x % p for x in a]
    b = [x % p for x in b]

    while len(a) < len(b): a.append(0)
    while len(b) < len(a): b.append(0)

    res = [a[i] + b[i] for i in range(len(a))]
    res = [(x + p) % p for x in res]

    return remove_suffix_zeros(res)

def pol_sub(a, b, n, p):
    a = [x % p for x in a]
    b = [x % p for x in b]

    while len(a) < len(b): a.append(0)
    while len(b) < len(a): b.append(0)

    res = [a[i] - b[i] for i in range(len(a))]
    res = [(x + p) % p for x in res]

    return remove_suffix_zeros(res)

def pol_mult(a, b, n, p):
    result = [0 for i in range(len(a) + len(b))]

    for idx_a, val_a in enumerate(a):
        for idx_b, val_b in enumerate(b):
            result[idx_a + idx_b] += val_a * val_b

    result = [x%p for x in result]
    result = remove_suffix_zeros(result)

    return result

def pol_div(a, b, n, p):
    a = remove_suffix_zeros(a)
    b = remove_suffix_zeros(b)

    result = []
    reminder = []

    while True:
        a = remove_suffix_zeros(a)
        if len(a) == 0: break

        if len(a) >= len(b):
            co_a = a[-1]
            co_b = b[-1]
            co = 0
            while True:
                if (co * co_b) % p == co_a: break
                co += 1

            dummy = [0 for i in range(len(a) - len(b) + 1)]
            dummy[-1] = co
            to_sub = pol_mult(b, dummy, n, p)
            a = pol_sub(a, to_sub, n, p)
            result = pol_sum(result, dummy, n, p)

        else:
            reminder = [x for x in a]
            break


    result = remove_suffix_zeros(result)
    reminder = remove_suffix_zeros(reminder)
    return result, reminder


def main():
    input_file_name, output_file_name = get_parameters()
    parity_check(input_file_name, output_file_name)

if __name__ == "__main__":
    main()
