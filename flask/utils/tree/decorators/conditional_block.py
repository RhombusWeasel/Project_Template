from utils.tree.decorators.base import Decorator

class ConditionalBlock(Decorator):
    def __init__(self, name, condition, blackboard=None):
        super().__init__(name, blackboard=blackboard)
        self.condition = condition

    def __tick__(self, blackboard):
        if self.condition(blackboard):
            return self.children[0].tick(blackboard)
        else:
            return self.FAILURE