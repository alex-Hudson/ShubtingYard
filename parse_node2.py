from branch import Branch
import re
import copy 

class ParseTree():
    ##
    # Takes expression and returns BNF form via buildParseTree
    ##
    def __init__(self, expression):
        self.expression = expression
        self.tree=Branch() #init empty tree
        self.buildParseTree(expression)

    def buildParseTree(self, expression):
        # Find all numbers and operators and put into list
        fplist = re.findall(r"[+*-/()\^]| *(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", expression)
        tree = self.tree
        current_branch = Branch()

        for i in fplist:
            if i == '(':
                current_branch = Branch()
                current_branch.insert_left('')
                tree.set_parent(current_branch)
                current_branch = current_branch.get_left_child()

            elif i in ['+', '-', '*', '/']:
                current_branch = Branch()
                current_branch.set_root_value(i)
                tree.set_parent(current_branch.tree)
                tree.insert_right({})
                current_branch = Branch()

            elif i == ')':
                current_branch = tree.get_parent()

            elif i not in ['+', '-', '*', '/', ')']:
                try:
                    current_branch = current_branch.set_root_value(int(i))
                    tree = current_branch

                except ValueError:
                    raise ValueError("token '{}' is not a valid integer".format(i))

        print self.tree.tree
        return tree

parse_tree=ParseTree("3+4*5")

