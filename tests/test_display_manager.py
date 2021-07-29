import pytest


def test_draw_and_erase_text(display_manager):
    display_manager.draw_written_text('a')

    assert display_manager.writing_buffer == ['a']
    assert display_manager.diffbox_manager.x_cursor == 88
    assert display_manager.chapter.text == 'a'

    display_manager.draw_written_text('b')

    assert display_manager.writing_buffer == ['a', 'b']
    assert display_manager.diffbox_manager.x_cursor == 68
    assert display_manager.chapter.text == 'ab'

    display_manager.erase_last_written_text()

    assert display_manager.writing_buffer == ['a']
    assert display_manager.diffbox_manager.x_cursor == 88
    assert display_manager.chapter.text == 'a'


def test_erase_nothing(display_manager):
    display_manager.erase_last_written_text()

    assert display_manager.diff_boxes_to_erase == []


def test_erase_with_no_writing_buffer(
    display_manager
):
    display_manager.diffbox_manager.diff_boxes = [
        (76, 8, 108, 40),
        (44, 8, 76, 40),
        (12, 8, 44, 40)
    ]

    display_manager.erase_last_written_text()

    assert display_manager.diff_boxes_to_erase == [(12, 8, 44, 40)]

    display_manager.erase_last_written_text()

    assert display_manager.diff_boxes_to_erase == [(12, 8, 76, 40)]


def test_display_on_multiple_rows(display_manager):
    words = ('a', 'b', 'c', ' ', 'd', 'e', 'f', ' ', 'g', 'h', 'i')
    for word in words:
        display_manager.draw_written_text(word)

    assert display_manager.chapter.text == 'abc def ghi'
    assert display_manager.diffbox_manager.diff_boxes == [
        (88, 8, 108, 40), (68, 8, 88, 40), (52, 8, 68, 40), (44, 8, 52, 40),
        (88, 40, 108, 72), (68, 40, 88, 72), (60, 40, 68, 72), (52, 40, 60, 72),
        (92, 72, 108, 104), (76, 72, 92, 104), (60, 72, 76, 104)
    ]
