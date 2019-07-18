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

# Open test file
open('test_results.txt', 'w').close()
File_object = open("test_results.txt","r+")
File_object.write("expression = %s\n" % args.expression)


# Evaluate on input
for line, vars in input_parser.items():
    print "=", vars
    answer = engine.eval(vars)    
    print line, "=>", answer
    # print to test.txt using my function
    L = ['Using my func: ', str(answer), '\n']
    File_object.writelines(L)

    #change vars to floats
    temp={}
    for key,var in vars.items():
        temp[key]=float(var)

    # print to test.txt using python inbuilt function
    testL = ['Using inbuilt func: ', str(eval(args.expression, temp)), '\n'] 
    File_object.writelines(testL)

File_object.close()