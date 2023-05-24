class Window:
  def __init__(self, x, y, width, height, title=''):
    self.x = x
    self.y = y
    self.width = width
    self.height = height
    self.title = title
    self.buffer = [[' ' for _ in range(width)] for _ in range(height)]
    self.prev_buffer = []
    self.current_line = 0
    self.draw_border()

  def clear(self):
    self.buffer = [[' ' for _ in range(self.width)] for _ in range(self.height)]
    self.current_line = 1
    self.draw_border()

  def write(self, text, x, y):
    if y < 0 or y >= self.height:
      return
    for i, char in enumerate(text):
      if 0 <= x + i < self.width - 2:
        self.buffer[y + 1][x + i] = char
    if hasattr(self, 'update_cursor') and hasattr(self, 'manager'):
      self.update_cursor(self.manager)

  def print(self, text, newline=True):
    if self.current_line >= self.height - 2:
      self.scroll()
    self.write(text, 1, self.current_line)
    if newline:
      self.current_line += 1
    if hasattr(self, 'update_cursor') and hasattr(self, 'manager'):
      self.update_cursor(self.manager)

  def scroll(self):
    for i in range(1, self.height - 2):
      self.buffer[i][1:-1] = self.buffer[i + 1][1:-1]
    self.buffer[self.height - 2] = ['│'] + [' ' for _ in range(self.width - 2)] + ['│']
    self.current_line -= 1

  def draw_border(self):
    self.buffer[0] = ['┌'] + ['─'] * (self.width - 2) + ['┐']
    self.buffer[-1] = ['└'] + ['─'] * (self.width - 2) + ['┘']
    for i in range(1, self.height - 1):
      self.buffer[i] = ['│'] + self.buffer[i][1:-1] + ['│']

    title_start = (self.width - len(self.title)) // 2
    self.buffer[0][title_start:title_start + len(self.title)] = list(self.title)