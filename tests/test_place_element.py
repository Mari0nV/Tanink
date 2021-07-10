import pytest


@pytest.mark.parametrize('last_word, text, nb_box, expected', [
    ('', 'b', 1, 'b'),
    ('banan', 'e', 1, 'banane'),
    ('bana', 'ne', 1, 'banane'),
    ('banane', ' ', 1, ''),
    ('banane', ' k', 1, 'k'),
    ('banane', ' kiwi', 1, 'kiwi'),
    ('banane', ' kiwi ', 1, ''),
    ('banane', ' kiwi p', 1, 'p'),
    ('banane', ', k', 1, 'k'),
    ('banane', '', 1, 'banan'),
    ('a', ',c,', 1, ''),
    ('a', 'a,b,c', 1, 'c'),
    ('bana', '', 2, 'ba'),
    ('bana', '', 4, ''),
    ('bana', '', 7, ''),
])
def test_update_last_word(place_element, last_word, text, nb_box, expected):
    place_element.last_word = last_word

    place_element._update_last_word(text, nb_box=nb_box)
    assert place_element.last_word == expected


@pytest.mark.parametrize('last_word, text, result', [
    ('banan', 'e', False),
    ('', 'b', True),
    ("banane", ",", False),
    ("banane", ', ', True),
    ("banane", ', k', True),
    ('banane', ' kiwi,', True),
    ('', 'b', True),
    ('banane', ',k', True),
    ('banane', ',k,', True),
])
def test_that_text_has_new_word(place_element, last_word, text, result):
    place_element.last_word = last_word

    assert place_element._has_new_word(text) == result


def test_move_word_on_new_row(
    place_element, diffbox_manager
):
    diffbox_manager.diff_boxes = [
        (52, 8, 72, 40),
        (32, 8, 52, 40),
        (12, 8, 32, 40)
    ]
    diffbox_manager.x_cursor = 12
    diffbox_manager.y_cursor = 8
    place_element.last_word = 'a'

    place_element.move_word_on_new_row('b')

    assert diffbox_manager.get_cursors() == (68, 40)
