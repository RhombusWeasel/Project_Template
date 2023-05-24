from utils.logger import Logger
from utils.tree.composites.base import Composite

class Sequence(Composite):
  def __init__(self, name='', **kwargs):
    super().__init__(name, **kwargs)
    self.current_child = 0
    self.logger = Logger(self.name)
    for key, value in kwargs.items():
      setattr(self, key, value)

  
  def tick(self, blackboard):
    while self.current_child < len(self.children):
      self.logger.info(f"Executing child: {self.children[self.current_child].name}")
      result = self.children[self.current_child].tick(blackboard)
      if result == self.SUCCESS:
        self.current_child += 1
      else:
        return result

    return self.SUCCESS