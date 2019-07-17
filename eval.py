import sys
import random
import copy
import re
import parse


class ShuntingYard:
    precedences = {'+': 0, '-': 0, '*': 1, '/': 1, '^': 2}

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

    def get_function(self, op):
        ops = {"+": (lambda x, y: x+y),
               "-": (lambda x, y: x-y),
               "*": (lambda x, y: x*y),
<<<<<<< .merge_file_a08372
               "^": (lambda x, y: x**y)}
=======
               "^": (lambda x, y: x ^ y)}
>>>>>>> .merge_file_a03460
        return ops[op]

    def peek(self, stack):
        return stack[-1] if stack else None

    def apply_operator(self, operators, values):
        operator = operators.pop()
        right = values.pop()
        left = values.pop()
        func = self.get_function(operator)
        answer = func(left, right)
        values.append(answer)

    def greater_precedence(self, op1, op2):
        return self.precedences[op1] > self.precedences[op2]

    def calculate(self, expression):
        operators = []
        values = []
        s = re.findall('[\\^]|[+-/*//()]|\d+', expression)
        for token in s:
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

        # nums_and_operators = self.seperate_operators_from_numbers(expression)
        x = args[0]
        y = args[1]
        print(x, y)

        answer = self.calculate(expression)
        print(answer)


cmd_parse = parse.CmdLineParse()
expression = cmd_parse.get_expression()
args = cmd_parse.get_inputs()
# cmd_parse.do_calc(expression, args)
args = cmd_parse.get_inputs()
print(expression)
shunting_yard = ShuntingYard()
shunting_yard.eval(expression, args)

# args = test.get_inputs()
# test.do_calc(expression, args)
# test.output()
