from sys import stdin


def crange(start, stop):
    ret = []
    for c in range(ord(start), ord(stop) + 1):
        ret.append(chr(c))
    return ret

# <equation>                ::= <variable> <whitespace> { <operator_and_operand> <whitespace> } |
#                               '(' <equation> ')' <whitespace> { <operator_and_operand> <whitespace> }
# <variable>                ::= <number> | <number> '(' <variable_name> ')' | <number> <variable_name>
# <operator_and_operand>    ::= <operator> <whitespace> '(' <variable> ')' | <operator> <whitespace> <variable> |
#                               <operator> <whitespace> '(' <equation> ')' | <operator> <whitespace> <equation> |
#                               <variable_name> | '(' <equation> ')'
# <variable_name>           ::= 'a'..'z'
# <whitespace>              ::= { ' ' }
# <number>                  ::= [ '-' ] <integer> [ '.' <integer> ]
# <integer>                 ::= <digit>+
# <operator>                ::= '^' | '/' | '*' | '-' | '+'
# <digit>                   ::= '0'..'9'


class Parser:
    def __init__(self):
        self.pointerStack = []
        self.parseMe = ""
        self.onMatchCallback = None
        self.muteCallbacks = 0

    def match(self, matchMe):
        if self.pointerStack[-1] >= len(self.parseMe):
            return False
        elif self.parseMe[self.pointerStack[-1]] == matchMe:
            self.pointerStack[-1] += 1
            return True
        else:
            return False

    def onMatch(self, name, value=None):
        if self.muteCallbacks == 0 and self.onMatchCallback is not None:
            self.onMatchCallback(name, value)

    def peek(self):
        if self.pointerStack[-1] >= len(self.parseMe):
            return None
        else:
            return self.parseMe(self.pointerStack[-1])

    def pointerCache(self):
        self.pointerStack.append(self.pointerStack[-1])

    def pointerPop(self):
        self.pointerStack.pop()

    def pointerCommit(self):
        self.pointerStack[-1] = self.pointerStack.pop()

    def test(self, parseMe):
        self.pointerStack = [0]
        self.parseMe = parseMe

        return self.equation() and self.pointerStack[-1] == len(self.parseMe)

    def equation(self):
        variable = self.variable()
        if variable is not None:
            val = variable
        else:
            equation = self.bracketed(self.equation, True)
            if equation is not None:
                val = equation
            else:
                return None

        val += self.whitespace()
        buf = self.operator_and_operand()
        while buf is not None:
            val += buf
            val += self.whitespace()
            buf = self.operator_and_operand()

        return val

    def variable(self):
        val = self.number()

        if val is not None:
            return val

        val = self.variable_name()
        if val is not None:
            return val
        else:
            return None

    def operator_and_operand(self):
        val = ""

        # Test for <number><var name>
        self.pointerCache()
        self.muteCallbacks += 1
        varName = self.bracketed(self.variable_name)
        self.muteCallbacks -= 1
        if varName is not None:
            self.pointerCommit()
            self.onMatch("operator", "*")
            self.onMatch("variable_name", varName)
            val += varName
            return val
        else:
            self.pointerPop()

        # Test for <number>(<equation)
        self.pointerCache()
        self.muteCallbacks += 1
        equation = self.bracketed(self.equation, True)
        self.muteCallbacks -= 1
        if equation is not None:
            self.pointerCommit()
            val += equation
            self.onMatch("operator", "*")
            self.onMatch("bracketStart")
            tempParser = Parser()
            tempParser.onMatchCallback = self.onMatchCallback
            tempParser.test(equation)
            self.onMatch("bracketEnd")
        else:
            self.pointerPop()

        # Test for normal <variable> <operator> <variable>
        self.pointerCache()

        operator = self.operator()
        if operator is None:
            self.pointerPop()
            return None

        val += operator
        val += self.whitespace()

        operand = self.bracketed(self.variable)
        if operand is not None:
            self.pointerCommit()
            return val + operand

        operand = self.bracketed(self.equation)
        if operand is not None:
            self.pointerCommit()
            return val + operand[1]
        else:
            self.pointerPop()
            return None

    def bracketed(self, func, required=False):
        bracketed = False
        self.pointerCache()

        if self.match('('):
            bracketed = True
            self.onMatch("bracketStart")
        elif required:
            self.pointerPop()
            return None

        val = func()
        if val is None:
            self.pointerPop()
            if bracketed:
                self.onMatch("bracketCancel")
            return None

        if bracketed:
            if self.match(')'):
                self.pointerCommit()
                self.onMatch("bracketEnd")
                return val
            else:
                self.pointerPop()
                self.onMatch("bracketCancel")
                return None
        else:
            self.pointerCommit()
            return val

    def variable_name(self):
        for x in crange('a', 'z'):
            if self.match(x):
                self.onMatch("variable_name", x)
                return x
        return None

    def whitespace(self):
        if not self.match(' '):
            return ''
        else:
            while self.match(' '):
                pass
            return ' '

    def number(self):
        val = ""
        if self.match('-'):
            val += "-"

        left = self.integer()
        if left is None:
            return None

        val += left
        if self.match('.'):
            val += "."
            buf = self.integer()
            if buf is None:
                return None
            else:
                val += buf
                self.onMatch("number", val)
                return val
        else:
            self.onMatch("number", val)
            return val

    def integer(self):
        val = self.digit()
        if val is None:
            return None
        else:
            buf = self.digit()
            while buf is not None:
                val += buf
                buf = self.digit()
            return val

    def operator(self):
        for x in ['^', '/', '*', '-', '+']:
            if self.match(x):
                self.onMatch("operator", x)
                return x
        return None

    def digit(self):
        for x in crange('0', '9'):
            if self.match(x):
                return x
        return None


class Tree:
    class TreeNode:
        nodePriority = {
            "number": 0,
            "variable_name": 0,
            "operator": 2,
            "brackets": 1
        }

        operatorPriority = {
            "^": 0,
            "/": 1,
            "*": 1,
            "+": 2,
            "-": 2
        }

        def __init__(self, type=None, value=None):
            self.type = type
            self.value = value
            self.parentNode = None
            self.leftBranch = None
            self.rightBranch = None

        def __gt__(self, other):
            if (self.nodePriority[self.type] != self.nodePriority[other.type]):
                return self.nodePriority[self.type] > self.nodePriority[other.type]
            elif other.type == "operator":
                return self.operatorPriority[self.value] > self.operatorPriority[other.value]
            else:
                return False

        def __str__(self):
            tempNode = self
            indent = ""
            while tempNode.parentNode is not None:
                tempNode = tempNode.parentNode
                indent += "  "
            ret = "%sType: %s, Value: %s" % (indent, self.type, self.value)
            if self.leftBranch is not None:
                ret += "\n%sLeft: (\n%s)" % (indent, self.leftBranch)
            else:
                ret += "\n%sLeft: None" % (indent)
            if self.rightBranch is not None:
                ret += "\n%sRight: (\n%s)" % (indent, self.rightBranch)
            else:
                ret += "\n%sRight: None" % (indent)
            return ret

    def __init__(self):
        self.nodePtr = None
        self.variables = {}
        self.bracketPositions = []

    def setVariables(self, variables):
        self.variables = variables

    def _insertOperator(self, operator):
        newNode = self.TreeNode("operator", operator)
        insertBetween = False

        # move down the tree while the new node is a higher priority than the current, and up the tree while its a lower priority
        while (newNode < self.nodePtr):
            self.nodePtr = self.nodePtr.rightBranch
            insertBetween = True

        # Move up the tree while the new node is a lower priority
        while (newNode > self.nodePtr):
            if self.nodePtr.parentNode is None:
                newNode.leftBranch = self.nodePtr
                self.nodePtr.parentNode = newNode
                self.nodePtr = newNode
            elif insertBetween:
                newNode.parentNode = self.nodePtr.parentNode
                self.nodePtr.parentNode.rightBranch = newNode
                self.nodePtr.parentNode = newNode
                newNode.leftBranch = self.nodePtr
                self.nodePtr = newNode
                break
            else:
                self.nodePtr = self.nodePtr.parentNode

        # Insert the node here
        if self.nodePtr.rightBranch is not None:
            self.nodePtr.parentNode = newNode
            newNode.leftBranch = self.nodePtr
            self.nodePtr = newNode

    def _insertNumberOrVariable(self, name, value):
        operandNode = self.TreeNode(name, value)
        self.nodePtr.rightBranch = operandNode
        operandNode.parentNode = self.nodePtr

    def _startBrackets(self):
        self.bracketPositions.append(self.nodePtr)
        self.nodePtr = None

    def _commitBrackets(self):
        bracketsNode = self.TreeNode("brackets")
        bracketsNode.leftBranch = self.getRootNode()
        self.nodePtr = self.bracketPositions.pop()
        if self.nodePtr is not None:
            self.nodePtr.rightBranch = bracketsNode
            bracketsNode.parentNode = self.nodePtr
        else:
            self.nodePtr = bracketsNode

    def _cancelBrackets(self):
        self.nodePtr = self.bracketPositions.pop()

    def receiveNode(self, name, value):
        #print("Received node: %s - %s" % (name, value))
        if name == "number" or name == "variable_name":
            if self.nodePtr is None:
                self.nodePtr = self.TreeNode(name, value)
            else:
                self._insertNumberOrVariable(name, value)
        elif name == "operator":
            self._insertOperator(value)
        elif name == "bracketStart":
            self._startBrackets()
        elif name == "bracketEnd":
            self._commitBrackets()
        elif name == "bracketCancel":
            self._cancelBrackets()
        else:
            pass  # print("Unhandled: %s" % (name))
        # self.dump()

    def getRootNode(self):
        rootNode = self.nodePtr
        if rootNode is None:
            return None

        while rootNode.parentNode is not None:
            rootNode = rootNode.parentNode
        return rootNode

    def dump(self):
        print(str(self.getRootNode()))

    def _solve(self, node):
        leftVal = None
        rightVal = None

        if node.leftBranch is not None:
            leftVal = self._solve(node.leftBranch)
        if node.rightBranch is not None:
            rightVal = self._solve(node.rightBranch)

        if node.type is "number":
            return float(node.value)
        elif node.type is "variable_name":
            return self.variables[node.value]
        elif node.type is "operator":
            if node.value == "^":
                return leftVal ** rightVal
            if node.value == "*":
                return leftVal * rightVal
            elif node.value == "/":
                return leftVal / rightVal
            elif node.value == "+":
                return leftVal + rightVal
            elif node.value == "-":
                return leftVal - rightVal
        elif node.type is "brackets":
            return leftVal
        else:
            pass  # print("Unhandled: %s" % (node.type))

    def solve(self):
        return self._solve(self.getRootNode())


def main():
    parser = Parser()
    tree = Tree()
    parser.onMatchCallback = tree.receiveNode

    input = stdin.readlines()
    for key in range(len(input)):
        input[key] = input[key].strip()

    if len(input) == 0:
        print("No formula specified")
        return

    valid = parser.test(input[0])
    input.pop(0)
    if not valid:
        print("Invalid formula")
        return

    for vars in input:
        varObj = {}
        for varDef in vars.split():
            vals = varDef.split("=")
            varObj[vals[0]] = float(vals[1])
        tree.setVariables(varObj)
        print(tree.solve())


def test():
    parser = Parser()
    tree = Tree()
    parser.onMatchCallback = tree.receiveNode

    #valid = parser.test("2(3x / (2y - 1))")
    valid = parser.test("(x + y) / (x - y) + 6")
    if not valid:
        print("Invalid formula")
        return

    tree.setVariables({"x": 5.0, "y": 3.0})
    # tree.dump()
    print(tree.solve())


main()
# test()
