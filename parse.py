import sys
import random
import copy
import argparse
import json
import csv


class CmdLineParse:
    # ENH: Handle n input variables and n input equations
    def __init__(self):
        # Class to parse arguments from command line
        self.get_inputs()

    @property
    # returns args
    def args(self):
        return self.args

    @property
    # returns expression
    def expression(self):
        if "expression" in self.args:
            return self.args["expression"]
        else:
            return None

    def parse_file(self):
        reader = csv.reader(open('data.txt'), delimiter=',')
        rows = []
        for row in reader:
            new_row = {}
            new_row['var1'] = row[0].strip()
            new_row['var2'] = row[1].strip()
            print(new_row)
            rows.append(new_row)

        # ENH: will need changing to handle multiple lines in input file
        return rows[0]

    def get_inputs(self):
        # Usze argparse lib to parse inputs
        parent_parser = argparse.ArgumentParser(add_help=False)
        parent_parser.add_argument('expression', type=str)
        file_parser = argparse.ArgumentParser(parents=[parent_parser])
        file_parser.add_argument('--file', type=str)
        args = file_parser.parse_known_args()
        args = vars(args[0])  # args[0] is the namespace
        self.expression = args["expression"]

        if args['file'] is None:
            variable_parser = argparse.ArgumentParser(parents=[parent_parser])
            variable_parser.add_argument('var1', type=float)
            variable_parser.add_argument('var2', type=float)

            variables = vars(variable_parser.parse_args())
            args.update(variables)
        print(args)

        # If --file given, load from file, else load from data in cmd line
        if args is None:
            print('You have not passed any commands in!')
            return
        if args["file"] is not None:
            self.args = self.parse_file()
        else:
            self.args = args
