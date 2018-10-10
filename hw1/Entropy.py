import sys
import collections as COL
import math

characters = ' აბგდევზთიკლმნოპჟრსტუფქღყშჩცძწჭხჯჰ'

def get_parameters():
    if len(sys.argv) != 3: raise Exception("Should pass exactly 2 parameters, passed: {0}".format(len(sys.argv) - 1))
    return sys.argv[1], sys.argv[2]

def calculate_and_store_entropy(input_file_name, output_file_name):
    with open(input_file_name, 'r', encoding='UTF-8') as rfile, open(output_file_name, 'w', encoding='UTF-8') as wfile:
        single_dict = COL.defaultdict(lambda:0)
        dual_dict = COL.defaultdict(lambda:0)

        total_symbols = 0
        prev_character = ' '

        for character in rfile.read():
            single_dict[character] += 1
            dual_dict[prev_character + character] += 1
            prev_character = character
            total_symbols += 1


        symnbol_entropy = 0
        dual_entropy = 0

        for character in characters:
            single_prob = (single_dict[character] / total_symbols)
            symnbol_entropy += -(single_prob * math.log(single_prob, 2)) if single_prob != 0 else 0;

            for suffix in characters:
                dual_prob = (dual_dict[character + suffix] / total_symbols)
                dual_entropy += -(dual_prob * math.log(dual_prob, 2)) if dual_prob != 0 else 0;

        wfile.writelines([str("%.7f" % symnbol_entropy) + '\n', str("%.7f" % dual_entropy) + '\n',  str("%.7f" % (dual_entropy-symnbol_entropy))])


def main():
    input_file_name, output_file_name = get_parameters()
    calculate_and_store_entropy(input_file_name, output_file_name)


if __name__ == "__main__":
    main()
