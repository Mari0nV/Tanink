import pytest

from tanink.writing_manager import WritingManager


@pytest.mark.parametrize('curr_x, curr_y, w, h, direction, exp_x, exp_y', [
    (110, 10, 30, 30, 1, 80, 10),
    (80, 10, 30, 30, -1, 110, 10),
    (10, 10, 30, 30, 1, 80, 40),
])
def test_move_cursor(curr_x, curr_y, w, h, direction, exp_x, exp_y):
    manager = WritingManager()
    manager.writing_rect_x = 10
    manager.writing_rect_y = 10
    manager.writing_rect_width = 100
    manager.writing_rect_height = 100
    manager.writing_rect_margin = 0
    manager.text_spacing = 0
    manager.x_cursor = curr_x
    manager.y_cursor = curr_y

    manager.move_cursors(w, h, direction)

    assert manager.x_cursor == exp_x
    assert manager.y_cursor == exp_y
