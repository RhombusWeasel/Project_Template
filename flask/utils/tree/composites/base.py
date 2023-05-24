from utils.tree.node import Node

class Composite(Node):
  def __init__(self, name='', **kwargs):
    super().__init__(name)
    self.children = []
    self.current_child = 0
    for key, value in kwargs.items():
      setattr(self, key, value)

  def reset(self):
    self.current_child = 0

  def add_child(self, child):
    self.children.append(child)

  def remove_child(self, child):
    self.children.remove(child)