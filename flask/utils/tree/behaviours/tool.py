from utils.tree.node import Node

# A tool is a leaf node that performs an action
# It must return either SUCCESS, FAILURE or RUNNING
# It can read and write to the blackboard
# The action is a function that takes the blackboard as an argument. 
# it is called when the tool is ticked, return true or false based on the result of the action
def default_function(blackboard):
    return True

class Tool(Node):
    def __init__(self, name, description, action=None, args={}, blackboard=None):
        super().__init__(name)
        self.description = description
        self.action = action
        self.args = args
        self.blackboard = blackboard

    def tick(self, blackboard):
        # Execute the action associated with this tool
        return self.action(blackboard)
