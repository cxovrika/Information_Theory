import sys
import numpy as np

def get_parameters():
    if len(sys.argv) != 4: raise Exception("Should pass exactly 3 parameters, passed: {0}".format(len(sys.argv) - 1))
    return sys.argv[1], sys.argv[2], sys.argv[3]



def bch(input_file_name, pwr_file_name, output_file_name):
    with open(input_file_name, 'r') as rfile, open(pwr_file_name, 'r') as pfile, open(output_file_name, 'w') as wfile:
        lines = [line.rstrip('\n') for line in rfile]
        p = int(lines[0])
        n = int(lines[1])
        g = [int(c) for c in lines[2].split(' ')]

        lines = [line.rstrip('\n') for line in pfile]
        dlt = int(lines[0])

        circle = [[1]]
        alpha = [0, 1]
        while True:
            last = circle[-1].copy()
            new_element = pol_mult(alpha, last, n, p)
            _, new_element = pol_div(new_element, g, n, p)

            if len(new_element) == 1 and new_element[0] == 1: break
            circle.append(new_element)

        # print(circle)

        fix = [0] * len(circle)
        final = [1]

        for pwr in range(1, dlt):
            if fix[pwr] == 1: continue
            x = pwr
            cnt = 1

            while True:
                fix[x] = 1
                x = (x * p) % len(circle)
                if x == pwr: break
                cnt += 1

            # print("circle:", circle)
            powers = [[1]]
            for i in range(cnt):
                last = powers[-1].copy()
                new_element = pol_mult(last, circle[pwr].copy(), n, p)
                _, new_element = pol_div(new_element, g, n, p)
                powers.append(new_element)

            # print("powers:", powers)

            koes = [0] * len(powers)
            result = []
            go(powers, koes, len(powers) - 1, result, n, p, g)
            # print("result:", result)
            # print(pwr, result)
            final = pol_mult(final, result, n, p)
            final = remove_suffix_zeros(final)

        final = fill_suffix_zeros(final, p**n - 1)

        wfile.write('{0}\n'.format(p))
        wfile.write('{0}\n'.format(p**n - 1))
        wfile.write(' '.join([str(x) for x in final]))




def go(powers, koes, idx, result, n, p, g):
    if idx == -1:
        if sum(koes) == 0: return
        res = []
        for i, koe in enumerate(koes):
            power = powers[i]
            ko = [koe]
            power = pol_mult(power, ko, n, p)
            power = remove_suffix_zeros(power)
            res = pol_sum(res, power,n ,p)
            res = remove_suffix_zeros(res)

        _, reminder = pol_div(res, g, n, p)
        if len(reminder) == 0:
            result.extend(koes)
    else:
        for i in range(p):
            koes[idx] = i
            go(powers, koes, idx - 1, result, n, p, g)
            if len(result) > 0: return


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
    input_file_name, pwr_file_name, output_file_name = get_parameters()
    bch(input_file_name, pwr_file_name, output_file_name)

if __name__ == "__main__":
    main()
