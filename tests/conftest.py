import pytest

from tanink.writing_manager import WritingManager


@pytest.fixture
def writing_manager():
    manager = WritingManager()
    manager.writing_rect_x = 10
    manager.writing_rect_y = 10
    manager.writing_rect_width = 100
    manager.writing_rect_height = 100
    manager.writing_rect_margin = 0
    manager.text_spacing = 0

    return manager
