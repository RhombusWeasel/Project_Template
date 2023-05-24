import os
import re
import subprocess
from utils.tree.behaviours.tool import Tool

class ExecuteFileTool(Tool):
  def __init__(self, name='', blackboard=None):
    super().__init__(
      name=name,
      description='This tool executes a script file and stores its output in the blackboard.',
      args={
        'filepath': 'script_name.ext',
        'args': ['arg1', 'arg2', 'arg3']
      },
      action=self.execute_file,
      blackboard=blackboard
    )

  def execute_file(self, blackboard):
    blackboard.set('status', 'Executing file...', namespace=self.name)
    filepath = f'files/{self.sanitize_path(blackboard.get("filepath", namespace=self.name))}'
    args = blackboard.get('args', namespace=self.name)

    if not filepath or not os.path.exists(filepath):
      blackboard.set('status', 'Failed to execute file.', namespace=self.name)
      blackboard.set('output', 'Invalid file path, file does not exist.', namespace=self.name)
      return self.FAILURE

    try:
      result = subprocess.run(['python', filepath, *args], capture_output=True, text=True, check=True)
      output = result.stdout
    except subprocess.CalledProcessError as error:
      blackboard.set('status', 'Failed to execute file.', namespace=self.name)
      blackboard.set('output', f'Error executing file: {error}', namespace=self.name)
      return self.FAILURE

    blackboard.set('output', output, namespace=self.name)
    return self.SUCCESS
  
  def sanitize_path(self, path):
    sanitized_path = re.sub(r'\.\.|[<>:"|?*]', '', path)
    return sanitized_path
