import sys
import random


class CmdLineParse:
    def get_inputs(self):
        # Function to handle command line usage
        args = sys.argv
        # First element of args is the file name, second is formula
        args = args[2:]

        if len(args) == 0:
            print('You have not passed any commands in!')
        else:
            to_return = []
            for a in args:
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
                    a = self.to_num(a)
                    to_return.append(a)
        print(to_return)
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
