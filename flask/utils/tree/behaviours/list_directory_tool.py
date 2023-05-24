import os
import re
from utils.tree.behaviours.tool import Tool

class ListDirectoryTool(Tool):
  def __init__(self, name='', blackboard=None):
    super().__init__(
      name=name,
      description='This tool lists the contents of your working directory or any subfolder thereof.',
      args={'dirpath': 'directory_path (/ for current directory)'},
      action=self.list_directory,
      blackboard=blackboard
    )

  def list_directory(self, blackboard):
    blackboard.set('status', 'Listing directory contents...', namespace=self.name)
    dirpath = f'files/{blackboard.get("dirpath", namespace=self.name)}'
    dirpath = self.sanitize_path(dirpath)

    if not dirpath or not os.path.exists(dirpath) or not os.path.isdir(dirpath):
      blackboard.set('status', 'Failed to list directory contents.', namespace=self.name)
      blackboard.set('output', 'Invalid directory path or directory does not exist.', namespace=self.name)
      return self.FAILURE

    contents = os.listdir(dirpath)

    # Store the directory contents in the blackboard
    blackboard.set('dir_contents', contents, namespace=self.name)
    return self.SUCCESS

  def sanitize_path(self, path):
    sanitized_path = re.sub(r'\.\.|[<>:"|?*]', '', path)
    return sanitized_path
