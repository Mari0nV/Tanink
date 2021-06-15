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
            if key.event_type == 'down':
                if re.match('^[\w,.:;-\\\(\\\?\\\/]{1}$', key.name):
                    self.display_manager.draw_written_text(key.name)
                else:
                    self.handle_special(key.name)
    
    def handle_special(self, name):
        try:
            getattr(self, f'_{name}')()
        except Exception:
            print("No method implemented for", name)

    def _backspace(self):
        self.display_manager.erase_last_written_text()

    def _space(self):
        self.display_manager.draw_written_text(' ')
