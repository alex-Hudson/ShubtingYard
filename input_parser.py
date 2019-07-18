import sys
import random
import copy
import argparse
import json
import csv
import re

class InputParser:
    # Reads lines from a stream and extras variable values

    # ENH: Handle n input variables and n input equations
    def __init__(self, strm):
        # Class to parse arguments from command line
        self.strm = strm

    def items(self):
        # Yield parse lines from self.strm
        ##
        # Yields:
        # line
        # vars    Dict of variable values

        for line in self.strm:
            line = line.rstrip()
            # splits string into dict of var_name:num 
            vars = dict((key.strip(), value.strip()) for key, value in (
                element.split('=') for element in line.split(', ')))

            yield line, vars
