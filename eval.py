import sys
import random
import copy
import re


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


class ShuntingYard:
    def split_string(self, string):
        return [char for char in string]

    def is_number(self, input):
        try:
            int(input)
            return True
        except ValueError:
            return False

    def find_occurrences(self, s, ch):
        return [i for i, letter in enumerate(s) if letter == ch]

    def seperate_operators_from_numbers(self, expression):
        # check if operator or number
        operators = re.findall("[+/*()-]", expression)
        numbers = [int(i) for i in re.findall(r'\d+', expression)]

        # put in dict
        to_return = {}
        to_return["operators"] = operators
        to_return["numbers"] = numbers
        return to_return

    def peek(self, stack):
        return stack[-1] if stack else None

    def apply_operator(self, operators, values):
        operator = operators.pop()
        right = values.pop()
        left = values.pop()
        values.append(eval("{0}{1}{2}".format(left, operator, right)))

    def greater_precedence(self, op1, op2):
        precedences = {'+': 0, '-': 0, '*': 1, '/': 1}
        return precedences[op1] > precedences[op2]

    def calculate(self, expression):
        operators = []
        values = []
        for token in expression:
            if self.is_number(token):
                values.append(int(token))
            elif token == '(':
                operators.append(token)
            elif token == ')':
                top = self.peek(operators)
                while top is not None and top != '(':
                    self.apply_operator(operators, values)
                    top = self.peek(operators)
                operators.pop()  # Discard the '('
            else:
                # Operator
                top = self.peek(operators)
                while top is not None and top not in "()" and self.greater_precedence(top, token):
                    self.apply_operator(operators, values)
                    top = self.peek(operators)
                operators.append(token)
        while self.peek(operators) is not None:
            self.apply_operator(operators, values)

        return values[0]

    def eval(self, expression, args):
        expression = expression.replace('x', str(args[0]))
        expression = expression.replace('y', str(args[1]))

        #nums_and_operators = self.seperate_operators_from_numbers(expression)
        x = args[0]
        y = args[1]
        print(x, y)

        answer = self.calculate(expression)


cmd_parse = CmdLineParse()
expression = cmd_parse.get_expression()
args = cmd_parse.get_inputs()
print(expression)
shunting_yard = ShuntingYard()
shunting_yard.eval(expression, args)

# args = test.get_inputs()
# test.do_calc(expression, args)
# test.output()
