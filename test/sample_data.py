#!/usr/bin/python3 -B
import argparse
from random import randint

def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-i', '--input-file', required=True)
    argparser.add_argument('-o', '--output-file', required=True)
    argparser.add_argument('-s', '--sample-size', 
                           help='Size of sample as num of lines', required=True)

    command_args = argparser.parse_args()

    random_sample = get_random_sample(command_args.input_file,
                     int(command_args.sample_size))
    write_out(random_sample, command_args.output_file)

# Random sample of rows using reservoir sampling
def get_random_sample(input_file, sample_size):
    with open(input_file, 'r') as f:
        reservoir = [f.readline() for i in range(0, sample_size)]

        i = sample_size
        for line in f:
            i += 1        
            index_to_replace = randint(0, i)

            if index_to_replace < sample_size:
                reservoir[index_to_replace] = line

        return reservoir

def write_out(sample, output_file):
    with open(output_file, 'w') as f:
        for row in sample:
            f.write(row)

if __name__ == '__main__':
    main()
