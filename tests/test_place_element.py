import pytest


@pytest.mark.parametrize('last_word, text, expected', [
    ('', 'b', 'b'),
    ('banan', 'e', 'banane'),
    ('bana', 'ne', 'banane'),
    ('banane', ' ', ''),
    ('banane', ' k', 'k'),
    ('banane', ' kiwi', 'kiwi'),
    ('banane', ' kiwi ', ''),
    ('banane', ' kiwi p', 'p'),
    ('banane', ', k', 'k'),
    ('banane', '', 'banan'),
    ('a', ',c,', ''),
    ('a', 'a,b,c', 'c'),
])
def test_update_last_word(place_element, last_word, text, expected):
    place_element.last_word = last_word

    place_element._update_last_word(text)
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
