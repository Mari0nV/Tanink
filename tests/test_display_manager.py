def test_draw_and_erase_text(display_manager):
    display_manager.draw_written_text('a')

    assert display_manager.writing_buffer == ['a']
    assert display_manager.writing_manager.x_cursor == 88

    display_manager.draw_written_text('b')

    assert display_manager.writing_buffer == ['a', 'b']
    assert display_manager.writing_manager.x_cursor == 68

    display_manager.erase_last_written_text()

    assert display_manager.writing_buffer == ['a']
    assert display_manager.writing_manager.x_cursor == 88

def test_erase_nothing(display_manager):
    display_manager.erase_last_written_text()

    assert display_manager.diff_boxes_to_erase == []


def test_erase_with_no_writing_buffer(
    display_manager
):
    display_manager.writing_manager.diff_boxes = [
        (76, 8, 108, 40),
        (44, 8, 76, 40),
        (12, 8, 44, 40)
    ]

    display_manager.erase_last_written_text()

    assert display_manager.diff_boxes_to_erase == [(12, 8, 44, 40)]

    display_manager.erase_last_written_text()

    assert display_manager.diff_boxes_to_erase == [(12, 8, 76, 40)]
