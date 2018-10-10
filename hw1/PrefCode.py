import sys
import collections as COL
import math

def get_parameters():
    if len(sys.argv) != 3: raise Exception("Should pass exactly 2 parameters, passed: {0}".format(len(sys.argv) - 1))
    return sys.argv[1], sys.argv[2]


def generate_next_word(_word, size):
    word = list(_word)
    added = False
    for i in reversed(range(len(word))):
        if added: continue
        if word[i] == '0': added = True
        word[i] = '1' if word[i] == '0' else '0'

    return ''.join(word + ['0' for i in range(size - len(word))])

def generate_pref_codes(input_file_name, output_file_name):
    with open(input_file_name, 'r', encoding='UTF-8') as rfile, open(output_file_name, 'w', encoding='UTF-8') as wfile:
        n = int(rfile.readline());
        sizes = [int(x) for x in rfile.readline().split(' ')]
        if sum([math.pow(1/2, x) for x in sizes]) > 1: return

        sizes = sorted(enumerate(sizes), key=lambda x:x[1])
        words = []

        current_word = ''
        for sz in sizes:
            if current_word == '':
                current_word = ''.join('0' for i in range(sz[1]))
            else:
                current_word = generate_next_word(current_word, sz[1])

            words.append([sz[0], current_word])


        for word in sorted(words, key=lambda x:x[0]):
            wfile.write('%s\n' % word[1])


def main():
    input_file_name, output_file_name = get_parameters()
    generate_pref_codes(input_file_name, output_file_name)


if __name__ == "__main__":
    main()
