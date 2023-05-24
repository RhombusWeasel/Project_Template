import sys

class WindowManager:
    def __init__(self, cols, rows):
        self.windows = []
        self.cols = cols
        self.rows = rows
        self.cursor_pos = (0, 0)

    def add_window(self, window):
        if not window in self.windows:
            self.windows.append(window)

    def move_cursor(self, x, y):
        self.cursor_pos = (x, y)

    def get_changes(self):
        changes = []
        for window in self.windows:
            for i in range(window.height):
                for j in range(window.width):
                    if (len(window.prev_buffer) <= i
                    or len(window.prev_buffer[i]) <= j
                    or window.buffer[i][j] != window.prev_buffer[i][j]):
                        changes.append((window.x + j, window.y + i, window.buffer[i][j]))
        return changes

    def render(self):
        changes = self.get_changes()

        for x, y, char in changes:
            sys.stdout.write("\033[%d;%dH" % (y + 1, x + 1))
            if char.startswith("\\"):
                sys.stdout.write(char.encode('unicode_escape').decode())  # Handle the escape character
            else:
                sys.stdout.write(char)

        # Restore cursor position
        x, y = self.cursor_pos
        sys.stdout.write("\033[%d;%dH" % (y + 1, x + 1))
        sys.stdout.flush()

        for window in self.windows:
            window.prev_buffer = [row.copy() for row in window.buffer]

        # Write window buffers and values to output.debug file
        with open("output.debug", "w") as debug_file:
            debug_file.write("Rendering windows:\n")
            for idx, window in enumerate(self.windows):
                debug_file.write(f"Window {idx}:\n")
                self.dump_object_attributes(window, debug_file)
                for row in window.buffer:
                    debug_file.write("".join(row) + "\n")
                debug_file.write("\n")
            debug_file.write("Changes: " + str(changes) + "\n")
            debug_file.write("=" * 40 + "\n")

    def dump_object_attributes(self, obj, file):
        for key, value in vars(obj).items():
            file.write(f"[{key}: {value}]\n")