from utils.tree.composites.base import Composite
from utils.logger import Logger

class PlanExecutor(Composite):
  def __init__(self, name='', **kwargs):
    super().__init__(name, **kwargs)
    self.logger = Logger(self.name)

  def tick(self, blackboard):
    tree_id = blackboard.get('tree_id')
    plan = blackboard.get("plan")
    self.logger.info(f"Plan received from AI: {plan}")
    if plan is None:
      self.logger.error("No plan received from AI, retrying...")
      return self.RUNNING
    else:
      while len(plan) > 0:
        step = plan.pop(0)
        blackboard.set('status', 'Executing plan')
        selected_child_name = step['name']
        if 'args' in step:
          for key, value in step['args'].items():
            blackboard.set(key, value, namespace=step['name'])
        # Check if the selected child name is in the list of child names
        child_names = [child.name for child in self.children]
        if selected_child_name not in child_names:
          self.logger.error(f"Invalid child name received from AI: {selected_child_name}")
          blackboard.set('status', f'Invalid child name received from AI: {selected_child_name}')
          return self.FAILURE
        # Find and execute the selected child
        for child in self.children:
          if child.name == selected_child_name:
            status = child.tick(blackboard)
            self.logger.info(f"Executed child: {child.name}, status: {status}")
            if status == self.FAILURE:
              return status
            if len(plan) == 0:
              blackboard.set('status', 'Plan executed successfully')
              return self.SUCCESS