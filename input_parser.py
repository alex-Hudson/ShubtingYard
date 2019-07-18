import sys
import random
import copy
import argparse
import json
import csv


class InputParser:
    # Reads lines from a stream and extras vareiable values

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
            yield line, {}  # STUB
