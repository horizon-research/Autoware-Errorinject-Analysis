import argparse
import sys
from pycparser import c_parser, c_ast, parse_file
import pdb

def main():
    input_dir = sys.argv[1]
    pdb.set_trace()
    ast = parse_file(input_dir, use_cpp = True)

    pdb.set_trace()
    print('tree parsed')

if __name__ == '__main__':
    main()