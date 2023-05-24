import sys
import select
import tty
import termios
from utils.cmd_utils.window import Window

class InputWindow(Window):
    def __init__(self, x, y, width, height, title='', on_enter=None, manager=None):
        super().__init__(x, y, width, height, title)
        self.on_enter = on_enter
        self.user_input = ""
        self.cursor_pos = 1
        self.manager = manager

    def move_cursor(self, x, y):
        self.cursor_pos = x + (y + 1) * self.width

    def update_cursor(self, manager):
        manager.move_cursor(self.x + self.cursor_pos, self.y + 1)

    def clear(self):
        for i in range(1, self.height - 1):
            self.buffer[i] = ['│'] + [' ' for _ in range(self.width - 2)] + ['│']
        self.draw_border()

    def update(self):
        old_settings = termios.tcgetattr(sys.stdin)
        try:
            tty.setraw(sys.stdin.fileno())
            if sys.stdin in select.select([sys.stdin], [], [], 0.2)[0]:
                char = sys.stdin.read(1)
                if ord(char) == 13:  # Enter
                    if self.on_enter:
                        self.on_enter(self.user_input)
                    self.user_input = ""
                    self.cursor_pos = 1
                    self.update_cursor(self.manager)
                    self.clear()
                elif ord(char) == 127:  # Backspace
                    self.user_input = self.user_input[:-1]
                    self.cursor_pos -= 1
                    self.update_cursor(self.manager)
                    self.clear()
                    self.write(self.user_input, 1, 0)
                else:
                    self.user_input += char
                    self.clear()
                    self.write(self.user_input, 1, 0)
                    self.cursor_pos += 1
            self.update_cursor(self.manager)
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)