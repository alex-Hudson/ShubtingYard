import re


class ShuntingYard:
    precedences = {'+': 0, '-': 0, '*': 1, '/': 1, '**': 2, "^": 2}

    def __init__(self, expression, args):
        self.eval(expression, args)

    def is_number(self, input):
        try:
            float(input)
            return True
        except ValueError:
            return False

    def seperate_operators_from_numbers(self, expression):
        # Find all numbers and operators and put into list
        exp = re.findall(
            r"[+*-/()\^]| *(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", expression)
        # Handle **
        for index, token in enumerate(exp):
            if token == '*' and exp[index+1] == '*':
                exp[index] = '**'
                del exp[index+1]
        return exp

    def get_function(self, op):
        ops = {"+": (lambda x, y: x+y),
               "-": (lambda x, y: x-y),
               "*": (lambda x, y: x*y),
               "**": (lambda x, y: x**y),
               "^": (lambda x, y: x**y)}
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
        s = self.seperate_operators_from_numbers(expression)
        for token in s:
            if self.is_number(token):
                values.append(float(token))
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
        for row in args:
            x = row["var1"]
            y = row["var2"]
            tmp = expression.replace('x', str(x))
            tmp = tmp.replace('y', str(y))
            print(x, y)
            answer = self.calculate(tmp)
            print(answer)
