import os
from utils.tree.behaviours.tool import Tool

class ReadFileTool(Tool):
  def __init__(self, name='', blackboard=None):
    super().__init__(
      name=name,
      description='This tool reads the contents of a file.',
      args={'filepath': 'file_name.ext'},
      action=self.read_file,
      blackboard=blackboard
    )

  def read_file(self, blackboard):
    blackboard.set('status', 'Reading file...', namespace=self.name)
    filename = blackboard.get('filepath', namespace=self.name)

    path = f'files/{filename}'
    if not filename or not os.path.exists(path):
      blackboard.set('status', 'Failed to read file.', namespace=self.name)
      blackboard.set('output', 'No filename provided or file does not exist.', namespace=self.name)
      return self.FAILURE

    with open(path, 'r') as file:
      contents = file.read()
    file.close()

    # Store the file contents in the blackboard
    blackboard.set('file_contents', contents, namespace=self.name)
    return self.SUCCESS