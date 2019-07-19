class Branch():
    # Branch of stack, can insert left and right, and set root node value
    def __init__(self):
        # Create empty tree
        self.tree={}

    def insert_left(self, input):
        self.tree['left']=input

    def insert_right(self, input):
        self.tree['right']=input

    def get_left_child(self):
        print 'left'

    def get_right_child(self):
        print 'right'

    def set_root_value(self, value):
        print 'root'

    def get_parent(self):
        print 'parent'
    
    def set_parent(self, parent):
        print 'set parent'

    def create_branch(self):
        print 'create branch'

