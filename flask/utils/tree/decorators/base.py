from utils.tree.node import Node

class Decorator(Node):
  def __tick__(self, blackboard):
    raise NotImplementedError("Decorator node must implement __tick__ method")