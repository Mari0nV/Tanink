import pytest
import os

from tanink.display_manager import DisplayManager
from tanink.writing_manager import WritingManager
import config as cfg


@pytest.fixture
def writing_manager():
    manager = WritingManager(transpose=True)
    manager.rect_x = 8
    manager.rect_y = 8
    manager.rect_width = 100
    manager.rect_height = 100
    manager.rect_margin = 0
    manager.text_spacing = 0
    manager.x_cursor = 108
    manager.y_cursor = 8

    return manager


@pytest.fixture
def display_manager(mocker, writing_manager):
    display = mocker.Mock()
    manager = DisplayManager(
        display=display,
        writing_manager=writing_manager
    )
    manager.font_path = os.path.join(
        os.path.dirname(__file__),
        'assets',
        'FreeSans.ttf'
    )
    manager.font_size = 30
    manager.transpose = True

    return manager
