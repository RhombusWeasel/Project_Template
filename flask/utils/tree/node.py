class Node:
    SUCCESS = 'SUCCESS'
    FAILURE = 'FAILURE'
    RUNNING = 'RUNNING'
    WAITING = 'WAITING'
    
    def __init__(self, name):
      self.name = name
      self.status = 'WAITING'

    def setup(self):
      raise NotImplementedError()

    def tick(self, blackboard):
      raise NotImplementedError()