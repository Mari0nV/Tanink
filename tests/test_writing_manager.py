import pytest


@pytest.mark.parametrize('nb_box, transpose, curr_x, curr_y, w, h, direction, exp_x, exp_y, init_diff_boxes, diff_boxes', [
    (1, True, 108, 8, 30, 30, 1, 76, 8, [], [
     (76, 8, 108, 40)]),  # add box on same row
    # remove box on same row
    (1, True, 76, 8, 30, 30, -1, 108, 8,
     [(76, 8, 108, 40)], [(76, 8, 108, 40)]),
    (1, True, 8, 8, 30, 30, 1, 76, 40, [], [
     (76, 40, 108, 72)]),  # add box on next row
    # remove first box of second row
    (1, True, 76, 40, 30, 30, -1, 108, 40,
     [(76, 40, 108, 72)], [(76, 40, 108, 72)]),
    # add box on same row (no transpose)
    (1, False, 8, 8, 30, 30, 1, 40, 8, [], [(8, 8, 40, 40)]),
    # remove box on same row (no transpose)
    (1, False, 40, 8, 30, 30, -1, 8, 8, [(8, 8, 40, 40)], [(8, 8, 40, 40)]),

])
def test_move_cursor(
    writing_manager, nb_box, transpose, curr_x, curr_y, w, h, direction, exp_x, exp_y, init_diff_boxes, diff_boxes
):
    writing_manager.transpose = transpose
    writing_manager.x_cursor = curr_x
    writing_manager.y_cursor = curr_y
    writing_manager.diff_boxes = init_diff_boxes

    writing_manager.move_cursors(w, h, direction, nb_box=nb_box)

    assert writing_manager.x_cursor == exp_x
    assert writing_manager.y_cursor == exp_y
    assert writing_manager.diff_boxes == diff_boxes


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


def test_multiple_add_and_erase_on_writing_manager(writing_manager):
    # add boxes
    writing_manager.move_cursors(30, 30)
    writing_manager.move_cursors(30, 30)
    writing_manager.move_cursors(30, 30)

    assert writing_manager.x_cursor == 12
    assert writing_manager.y_cursor == 8
    assert writing_manager.diff_boxes == [
        (76, 8, 108, 40),
        (44, 8, 76, 40),
        (12, 8, 44, 40)
    ]

    # remove box
    writing_manager.pop_diff_box()

    assert writing_manager.x_cursor == 44
    assert writing_manager.y_cursor == 8
    assert writing_manager.diff_boxes == [
        (76, 8, 108, 40),
        (44, 8, 76, 40)
    ]

    # remove box
    writing_manager.pop_diff_box()

    assert writing_manager.x_cursor == 76
    assert writing_manager.y_cursor == 8
    assert writing_manager.diff_boxes == [
        (76, 8, 108, 40)
    ]


def test_multiline_on_writing_manager(writing_manager):
    # add more boxes than a row can display
    writing_manager.move_cursors(30, 30)
    writing_manager.move_cursors(30, 30)
    writing_manager.move_cursors(30, 30)
    writing_manager.move_cursors(30, 30)

    assert writing_manager.x_cursor == 76
    assert writing_manager.y_cursor == 40
    assert writing_manager.diff_boxes == [
        (76, 8, 108, 40),
        (44, 8, 76, 40),
        (12, 8, 44, 40),
        (76, 40, 108, 72)
    ]

    # remove box
    writing_manager.pop_diff_box()
    assert writing_manager.x_cursor == 108
    assert writing_manager.y_cursor == 40
    assert writing_manager.diff_boxes == [
        (76, 8, 108, 40),
        (44, 8, 76, 40),
        (12, 8, 44, 40)
    ]

    # remove box
    writing_manager.pop_diff_box()
    assert writing_manager.x_cursor == 44
    assert writing_manager.y_cursor == 8
    assert writing_manager.diff_boxes == [
        (76, 8, 108, 40),
        (44, 8, 76, 40)
    ]


def test_corner_cases_on_writing_manager(writing_manager):
    # try to remove inexisting box
    writing_manager.pop_diff_box()

    assert writing_manager.x_cursor == 108
    assert writing_manager.y_cursor == 8
    assert writing_manager.diff_boxes == []

    # add one box after erase
    writing_manager.move_cursors(30, 30)

    assert writing_manager.x_cursor == 76
    assert writing_manager.y_cursor == 8
    assert writing_manager.diff_boxes == [
        (76, 8, 108, 40)
    ]

    # try to remove two boxes instead of one
    writing_manager.pop_diff_box()
    writing_manager.pop_diff_box()

    assert writing_manager.x_cursor == 108
    assert writing_manager.y_cursor == 8
    assert writing_manager.diff_boxes == []


@pytest.mark.parametrize('width, output, diff_boxes', [
    (None, ((12, 8, 44, 40), 1), [
        (74, 8, 108, 40),
        (44, 8, 74, 40)
    ]),
    (32, ((12, 8, 44, 40), 1), [
        (74, 8, 108, 40),
        (44, 8, 74, 40)
    ]),
    (62, ((12, 8, 74, 40), 2), [(74, 8, 108, 40)]),
    (96, ((12, 8, 108, 40), 3), []),
])
def test_pop_diff_box(writing_manager, width, output, diff_boxes):
    writing_manager.diff_boxes = [
        (74, 8, 108, 40),
        (44, 8, 74, 40),
        (12, 8, 44, 40),
    ]

    assert writing_manager.pop_diff_box(width) == output
    assert writing_manager.diff_boxes == diff_boxes
