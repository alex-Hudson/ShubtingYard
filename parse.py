import sys
import random
import copy
import argparse
import json
import csv


class CmdLineParse:

    def parse_file(self):
        reader = csv.reader(open('data.txt'), delimiter=',')
        rows = []
        items = []
        for row in reader:
            new_row = {}
            new_row['expression'] = row[0]
            new_row['var1'] = row[1]
            new_row['var2'] = row[2]
            print(new_row)
            rows.append(new_row)

        return rows

    def get_inputs(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("expression", help="expression string")
        parser.add_argument("var1", help="variable 1",
                            type=float)
        parser.add_argument("var2", help="variable 2",
                            type=float)
        parser.add_argument(
            "--file", type=str, help="load a .txt file containing an expression and variables")

        args = parser.parse_args()
        print(args)
        return vars(args)

    def handle_inputs(self, args):
        if args is None:
            print('You have not passed any commands in!')
            return
        if args["file"] is not None:
            print "blah"
            to_return = self.parse_file()
        else:
            to_return = []
            for a in args.keys():
                if a == '--help':
                    print('Basic command line program')
                    print('Options:')
                    print('    --help -> show this basic help menu.')
                    print('    --monty -> show a Monty Python quote.')
                    print('    --veg -> show a random vegetable')
                elif a == '--monty':
                    print(
                        'What\'s this, then? "Romanes eunt domus"? People called Romanes, they go, the house?')
                elif a == '--veg':
                    print(random.choice(['Carrot', 'Potato', 'Turnip']))
                else:
                    return args
            return to_return

    def get_expression(self):
        args = sys.argv
        self.expression = args[1]
        return self.expression

    def to_num(self, string):
        # Convert string to either int or float
        try:
            ret = int(string)
        except ValueError:
            # Try float
            ret = float(string)
        return ret

    def do_calc(self, expression, args):
        x_range = self.get_range([], args[0], 'x')
        self.range = self.get_range(x_range, args[1], 'y')
        to_return = []
        outputs = copy.deepcopy(self.range)
        for index, inputs in enumerate(self.range):
            x = inputs['x']
            y = inputs['y']
            to_return = eval(expression)
            outputs[index]['calc'] = to_return
        print(outputs[5]['calc'])
        self.outputs = outputs

    def get_range(self, number_range, number, key):
        index = 0
        for i in range(number-5, number+5):
            try:
                number_range[index]
            except:
                number_range.append({})
            number_range[index][key] = i
            index += 1
        return number_range

    def output(self):
        for output in self.outputs:
            print('x:', output['x'], 'y:', output['y'],
                  'equals',  output['calc'])
