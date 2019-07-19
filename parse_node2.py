class ParseTree():
    ##
    # Takes expression and returns BNF form via buildParseTree
    ##
    def __init__(self, expression):
        self.expression = expression

    def buildParseTree(self):
        fplist = self.expression.split()
        tree={}
        current_branch = {}

        for i in fplist:
            if i == '(':
                current_branch.insertLeft('')
                tree.push(current_branch)
                current_branch = current_branch.getLeftChild()

            elif i in ['+', '-', '*', '/']:
                current_branch.setRootVal(i)
                current_branch.insertRight('')
                tree.push(currentTree)
                current_branch = current_branch.getRightChild()

            elif i == ')':
                current_branch = tree.pop()

            elif i not in ['+', '-', '*', '/', ')']:
                try:
                    current_branch.setRootVal(int(i))
                    parent = tree.pop()
                    current_branch = parent

                except ValueError:
                    raise ValueError("token '{}' is not a valid integer".format(i))

        return tree

parse_tree=ParseTree("3+4*5")
pt = parse_tree.buildParseTree()
#pt.postorder()  #defined and explained in the next section

class Branch():
    # Branch of stack, can insert left and right, and set root node value
    def __init__(self):

    def insert_left(self):

    def insert_right(self):