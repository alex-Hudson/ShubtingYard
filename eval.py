import sys
from input_parser import InputParser
from shuntingYard import ShuntingYardEngine
import argparse


# Define singanture
arg_parser = argparse.ArgumentParser(add_help=False)
arg_parser.add_argument('expression', type=str, help="Expression to be evaluated")

# Parse command line
args = arg_parser.parse_args(sys.argv[1:])
print(args.expression)

engine = ShuntingYardEngine(args.expression)
input_parser = InputParser(sys.stdin)

# Evaluate on input
for line, vars in input_parser.items():
    print "=", vars
    print line, "=>", engine.eval(vars)
