import os
from utils.tree.behaviours.tool import Tool

class WriteFileTool(Tool):
  def __init__(self, name='WRITE_FILE_TOOL', blackboard=None):
    super().__init__(
      name=name,
      description='This tool reads the contents of a file and writes it to the blackboard.',
      args={
        'filepath': 'file_name.ext',
        'data': 'data to write to file'
      },
      action=self.write_file,
      blackboard=blackboard
    )

  def write_file(self, blackboard):
    blackboard.set('status', 'Writing file...', namespace=self.name)
    filename = blackboard.get('filepath', namespace=self.name)
    data = blackboard.get('data', namespace=self.name)

    if not filename or not data:
      blackboard.set('output', 'No filename or data provided.', namespace=self.name)
      return self.FAILURE
    
    if not os.path.exists('files'):
      os.mkdir('files')

    try:
      with open(f'files/{filename}', 'w') as file:
        file.write(data)
      file.close()
      blackboard.set('output', 'File written.', namespace=self.name)
      return self.SUCCESS
    except Exception as e:
      #self.logger.error(f'Error writing file: {e}')
      blackboard.set('output', e, namespace=self.name)
      return self.FAILURE