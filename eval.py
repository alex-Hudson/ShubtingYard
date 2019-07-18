import sys
import random
import copy
import re
from input_parser import InputParser
from shuntingYard import ShuntingYard
import argparse


# Define singanture
arg_parser = argparse.ArgumentParser(add_help=False)
arg_parser.add_argument('expression', type=str,
                        help="Expression to be evaluated")
arg_parser.add_argument(
    '--file', type=str, help="File to read input values from")

# Parse command line
args = arg_parser.parse_args(sys.argv[1:])
print(args.expression)

engine = ShuntingYard()
input_parser = InputParser(sys.stdin)

# Evaluate on input
for line, vars in input_parser.items():
    print line, "=>", engine.eval(args.expression,vars)
