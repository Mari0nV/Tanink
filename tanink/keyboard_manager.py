import keyboard
from queue import Queue


special_keys = [
    'space', 'backspace', 'caps lock', 'unknown', 'tab', 'maj', 'decimal', 'enter', 'verr.maj',
    'ctrl droite', 'windows gauche'
]

class KeyboardManager:
    """ Manage keyboard input. 
        Associate each key pressed with its corresponding action,
        like writing a character or erasing it.
    """
    def __init__(self, display_manager):
        self.display_manager = display_manager
        self.events = Queue()
        keyboard.start_recording(self.events)
 
    def check_key_pressed(self):
        while not self.events.empty():
            key = self.events.get_nowait()
            if key.event_type == 'down':
                if key.name in special_keys:
                    self.handle_special(key.name)
                elif not keyboard.is_modifier(key.name):
                    self.display_manager.draw_written_text(key.name)
    
    def handle_special(self, name):
        try:
            getattr(self, f'_{name}')()
        except AttributeError as e:
            print("No method implemented for", name)

    def _backspace(self):
        self.display_manager.erase_last_written_text()

    def _space(self):
        self.display_manager.draw_written_text(' ')

