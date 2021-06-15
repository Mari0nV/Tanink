import pytest

from tanink.display_manager import DisplayManager
from tanink.writing_manager import WritingManager


@pytest.fixture
def writing_manager():
    manager = WritingManager()
    manager.writing_rect_x = 8
    manager.writing_rect_y = 8
    manager.writing_rect_width = 100
    manager.writing_rect_height = 100
    manager.writing_rect_margin = 0
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
    manager.font_path = '/usr/share/fonts/truetype/freefont/FreeSans.ttf'
    manager.font_size = 30

    return manager
