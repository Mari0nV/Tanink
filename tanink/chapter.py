import json
import os


class Chapter:
    def __init__(self, id):
        self.id = id
        self.text = ""

    def add_text(self, text):
        self.text += text
    
    def save(self):
        filepath = os.environ.join(
            os.path.dirname(__name__),
            "save",
            f'chapter_{id}.json'
        )

        with open(filepath, "w"):
            json.dump({
                "text": self.text
            })
