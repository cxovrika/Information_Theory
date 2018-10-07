import sys
import collections as COL

characters = " აბგდევზთიკლმნოპჟრსტუფქღყშჩცძწჭხჯჰ"

def get_parameters():
    if len(sys.argv) != 3: raise Exception("Should pass exactly 2 parameters, passed: {0}".format(len(sys.argv) - 1))
    return sys.argv[1], sys.argv[2]

def calculate_and_store_distribution(input_file_name, output_file_name):
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

        single_probs = []
        dual_probs = []
        for character in characters:
            single_probs.append(str("%.7f" % (single_dict[character] / total_symbols)))

            for suffix in characters:
                dual_probs.append(str("%.7f" % (dual_dict[character + suffix] / total_symbols)))

        wfile.writelines([' '.join(single_probs) + '\n', ' '.join(dual_probs)] )



def main():
    input_file_name, output_file_name = get_parameters()
    calculate_and_store_distribution(input_file_name, output_file_name)


if __name__ == "__main__":
    main()
