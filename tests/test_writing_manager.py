import pytest


@pytest.mark.parametrize('curr_x, curr_y, w, h, direction, exp_x, exp_y', [
    (110, 10, 30, 30, 1, 80, 10),
    (80, 10, 30, 30, -1, 110, 10),
    (10, 10, 30, 30, 1, 80, 40),
])
def test_move_cursor(writing_manager, curr_x, curr_y, w, h, direction, exp_x, exp_y):
    writing_manager.x_cursor = curr_x
    writing_manager.y_cursor = curr_y

    writing_manager.move_cursors(w, h, direction)

    assert writing_manager.x_cursor == exp_x
    assert writing_manager.y_cursor == exp_y


@pytest.mark.parametrize('size, diff_box', [
    (None, (11, 9, 15, 18)),
    (1, (11, 9, 15, 18)),
    (2, (5, 2, 15, 18)),
    (3, (1, 2, 15, 18)),
])
def test_get_diff_box(writing_manager, size, diff_box):
    writing_manager.diff_boxes = [
        (1, 2, 5, 9), (5, 2, 10, 9), (11, 9, 15, 18)
    ]

    assert writing_manager.get_diff_box(size) == diff_box
