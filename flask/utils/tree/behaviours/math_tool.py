from utils.logger import Logger
from utils.tree.behaviours.tool import Tool

# A tool is a leaf node that performs an action
# It must return either SUCCESS, FAILURE or RUNNING
# It can read and write to the blackboard
# The action is a function that takes the blackboard as an argument. 
# it is called when the tool is ticked, return true or false based on the result of the action
def default_function(blackboard):
    return True

class MathTool(Tool):
    def __init__(self, name='', blackboard=None):
      super().__init__(
        name=name,
        description='This tool returns the evaluation of a simple mathematical expression. You cannot use this for user input.',
        args={
          'expression': 'expression eg 2 * 6'
        },
        action=self.evaluate,
        blackboard=blackboard
      )

    def evaluate(self, blackboard):
      expression = blackboard.get('expression', namespace=self.name)
      if not expression:
        blackboard.set('status', 'Failed to evaluate expression.', namespace=self.name)
        return self.FAILURE
      else:
        try:
          output = eval(expression)
          blackboard.set('output', output, namespace=self.name)
          return self.SUCCESS
        except Exception as error:
          blackboard.set('status', 'Failed to evaluate expression.', namespace=self.name)
          blackboard.set('output', f'Error evaluating expression: {error}', namespace=self.name)
          return self.FAILURE
