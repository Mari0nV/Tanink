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
    diffbox_manager, nb_box, transpose, curr_x, curr_y, w, h, direction, exp_x, exp_y, init_diff_boxes, diff_boxes
):
    diffbox_manager.transpose = transpose
    diffbox_manager.x_cursor = curr_x
    diffbox_manager.y_cursor = curr_y
    diffbox_manager.diff_boxes = init_diff_boxes
    diffbox_manager.fontsize = h

    diffbox_manager.move_cursors(w, direction, nb_box=nb_box)

    assert diffbox_manager.x_cursor == exp_x
    assert diffbox_manager.y_cursor == exp_y
    assert diffbox_manager.diff_boxes == diff_boxes


@pytest.mark.parametrize('size, diff_box', [
    (None, (11, 9, 15, 18)),
    (1, (11, 9, 15, 18)),
    (2, (5, 2, 15, 18)),
    (3, (1, 2, 15, 18)),
])
def test_get_diff_box(diffbox_manager, size, diff_box):
    diffbox_manager.diff_boxes = [
        (1, 2, 5, 9), (5, 2, 10, 9), (11, 9, 15, 18)
    ]

    assert diffbox_manager.get_diff_box(size) == diff_box


def test_multiple_add_and_erase_on_diffbox_manager(diffbox_manager):
    # add boxes
    diffbox_manager.move_cursors(30)
    diffbox_manager.move_cursors(30)
    diffbox_manager.move_cursors(30)

    assert diffbox_manager.x_cursor == 12
    assert diffbox_manager.y_cursor == 8
    assert diffbox_manager.diff_boxes == [
        (76, 8, 108, 40),
        (44, 8, 76, 40),
        (12, 8, 44, 40)
    ]

    # remove box
    diffbox_manager.pop_diff_box()

    assert diffbox_manager.x_cursor == 44
    assert diffbox_manager.y_cursor == 8
    assert diffbox_manager.diff_boxes == [
        (76, 8, 108, 40),
        (44, 8, 76, 40)
    ]

    # remove box
    diffbox_manager.pop_diff_box()

    assert diffbox_manager.x_cursor == 76
    assert diffbox_manager.y_cursor == 8
    assert diffbox_manager.diff_boxes == [
        (76, 8, 108, 40)
    ]


def test_multiline_on_diffbox_manager(diffbox_manager):
    # add more boxes than a row can display
    diffbox_manager.move_cursors(30)
    diffbox_manager.move_cursors(30)
    diffbox_manager.move_cursors(30)
    diffbox_manager.move_cursors(30)

    assert diffbox_manager.x_cursor == 76
    assert diffbox_manager.y_cursor == 40
    assert diffbox_manager.diff_boxes == [
        (76, 8, 108, 40),
        (44, 8, 76, 40),
        (12, 8, 44, 40),
        (76, 40, 108, 72)
    ]

    # remove box
    diffbox_manager.pop_diff_box()
    assert diffbox_manager.x_cursor == 108
    assert diffbox_manager.y_cursor == 40
    assert diffbox_manager.diff_boxes == [
        (76, 8, 108, 40),
        (44, 8, 76, 40),
        (12, 8, 44, 40)
    ]

    # remove box
    diffbox_manager.pop_diff_box()
    assert diffbox_manager.x_cursor == 44
    assert diffbox_manager.y_cursor == 8
    assert diffbox_manager.diff_boxes == [
        (76, 8, 108, 40),
        (44, 8, 76, 40)
    ]


def test_corner_cases_on_diffbox_manager(diffbox_manager):
    # try to remove inexisting box
    diffbox_manager.pop_diff_box()

    assert diffbox_manager.x_cursor == 108
    assert diffbox_manager.y_cursor == 8
    assert diffbox_manager.diff_boxes == []

    # add one box after erase
    diffbox_manager.move_cursors(30)

    assert diffbox_manager.x_cursor == 76
    assert diffbox_manager.y_cursor == 8
    assert diffbox_manager.diff_boxes == [
        (76, 8, 108, 40)
    ]

    # try to remove two boxes instead of one
    diffbox_manager.pop_diff_box()
    diffbox_manager.pop_diff_box()

    assert diffbox_manager.x_cursor == 108
    assert diffbox_manager.y_cursor == 8
    assert diffbox_manager.diff_boxes == []


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
def test_pop_diff_box(diffbox_manager, width, output, diff_boxes):
    diffbox_manager.diff_boxes = [
        (74, 8, 108, 40),
        (44, 8, 74, 40),
        (12, 8, 44, 40),
    ]

    assert diffbox_manager.pop_diff_box(width) == output
    assert diffbox_manager.diff_boxes == diff_boxes


def test_with_multiple_boxes(diffbox_manager):
    diffbox_manager.move_cursors(60, nb_box=2)

    assert diffbox_manager.x_cursor == 44
    assert diffbox_manager.y_cursor == 8
    assert diffbox_manager.diff_boxes == [
        (76, 8, 108, 40),
        (44, 8, 76, 40),
    ]


@pytest.mark.parametrize('nb_rows, expected_diff_box', [
    (0, None),
    (1, (8, 40, 108, 80)),
    (2, (8, 0, 108, 80)),
    (3, (8, 0, 108, 80))
])
def test_get_row_diff_box(diffbox_manager, nb_rows, expected_diff_box):
    diffbox_manager.y_cursor = 40
    diffbox_manager.row_height = 40
    diffbox_manager.row_index = 1

    assert diffbox_manager.get_row_diff_box(nb_rows) == expected_diff_box
