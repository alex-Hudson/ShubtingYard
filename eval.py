import sys
import random
import copy

class CmdLineParse:
    def get_inputs(self):
        # Function to handle command line usage
        args = sys.argv
        args = args[2:] # First element of args is the file name, second is formula

        if len(args) == 0:
            print('You have not passed any commands in!')
        else:
            to_return=[]
            for a in args:
                if a == '--help':
                    print('Basic command line program')
                    print('Options:')
                    print('    --help -> show this basic help menu.')
                    print('    --monty -> show a Monty Python quote.')
                    print('    --veg -> show a random vegetable')
                elif a == '--monty':
                    print('What\'s this, then? "Romanes eunt domus"? People called Romanes, they go, the house?')
                elif a == '--veg':
                    print(random.choice(['Carrot', 'Potato', 'Turnip']))
                else:
                    a = self.to_num(a)
                    to_return.append(a)
        print(to_return)
        return to_return 
    
    def get_expression(self):
        args = sys.argv
        self.expression=args[1]
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
            x=inputs['x']
            y=inputs['y']
            to_return = eval(expression)
            outputs[index]['calc']=to_return
        self.outputs=outputs


    def get_range(self, number_range, number, key):
        index = 0
        for i in range(number-5, number+5):
            try: 
                number_range[index]
            except:
                number_range.append({})
            number_range[index][key]=i
            index += 1
        return number_range

    def output(self):
        for output in self.outputs:
            print('x:', output['x'], 'y:', output['y'], 'equals',  output['calc'])



class ShuntingYard:                       
    def split_string(self, string):
        return [char for char in string]

    def is_number(self, input):
        try:
            int(input)
            return True
        except TypeError:
            return False

    def seperate_operators_from_numbers(self, expression):
        #split string
        self.split_string(expression)

        # check if operator or number 

        # put operators in dict

        # put numbers in dict
        # Return dict with numbers and values

    def eval(self, expression)
        obj = self.seperate_operators_from_numbers(expression)



test=CmdLineParse()
expression=test.get_expression()
print(expression)
shunting_yard = new ShuntingYard()
shunting_yard.eval(expression)

# args = test.get_inputs()
# test.do_calc(expression, args)
# test.output()
