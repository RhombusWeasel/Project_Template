from utils.tree.composites.base import Composite

class Selector(Composite):
  def tick(self, blackboard):
    while self.current_child < len(self.children):
      result = self.children[self.current_child].tick(blackboard)
      if result != "failure":
        if result == "success":
          self.reset()
        return result
      self.current_child += 1

    self.reset()
    return "failure"