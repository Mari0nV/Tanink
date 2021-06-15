import keyboard
from queue import Queue
import re


class KeyboardManager:
    def __init__(self, display_manager):
        self.display_manager = display_manager
        self.events = Queue()
        keyboard.start_recording(self.events)

    def check_key_pressed(self):
        while not self.events.empty():
            key = self.events.get_nowait()
            if key.event_type == 'down' and re.match('^\w{1}$', key.name):
                self.display_manager.draw_written_text(key.name)
