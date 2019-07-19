from branch import Branch
import re

class ParseTree():
    ##
    # Takes expression and returns BNF form via buildParseTree
    ##
    def __init__(self, expression):
        self.expression = expression
        self.tree=Branch() #init empty tree

    def buildParseTree(self):
        # Find all numbers and operators and put into list
        fplist = re.findall(
            r"[+*-/()\^]| *(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", self.expression)
        tree = self.tree

        for i in fplist:
            if i == '(':
                current_branch = tree.create_branch()
                current_branch.insert_left('')
                tree.set_parent(current_branch)
                current_branch = current_branch.get_left_child()

            elif i in ['+', '-', '*', '/']:
                current_branch = tree
                current_branch.set_root_value(i)
                current_branch.insert_right('')
                tree.set_parent(current_branch)
                current_branch = current_branch.get_right_child()

            elif i == ')':
                current_branch = tree.get_parent()

            elif i not in ['+', '-', '*', '/', ')']:
                try:
                    current_branch = tree
                    current_branch.set_root_value(int(i))
                    parent = tree.get_parent()
                    current_branch = parent

                except ValueError:
                    raise ValueError("token '{}' is not a valid integer".format(i))

        return tree

parse_tree=ParseTree("3+4*5")
pt = parse_tree.buildParseTree()
#pt.postorder()  #defined and explained in the next section

