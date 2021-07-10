from PIL import ImageFont
import pytest
import os

from tanink.display_manager import DisplayManager
from tanink.place_element import PlaceElement
from tanink.diffbox_manager import DiffBoxManager
import config as cfg


@pytest.fixture
def diffbox_manager():
    manager = DiffBoxManager(transpose=True)
    manager.rect_x = 8
    manager.rect_y = 8
    manager.rect_width = 100
    manager.rect_height = 100
    manager.rect_margin = 0
    manager.text_spacing = 0
    manager.x_cursor = 108
    manager.y_cursor = 8
    manager.fontsize = 30
    manager.row_index = 0

    return manager


@pytest.fixture
def place_element(mocker, diffbox_manager):
    display = mocker.Mock()
    place = PlaceElement(
        display=display,
        diffbox_manager=diffbox_manager
    )
    font_path = os.path.join(
        os.path.dirname(__file__),
        'assets',
        'FreeSans.ttf'
    )
    place.font_size = 30
    place.font = ImageFont.truetype(font_path, place.font_size)
    place.transpose = True
    return place


@pytest.fixture
def display_manager(mocker, place_element):
    display = mocker.Mock()
    manager = DisplayManager(
        display=display,
        diffbox_manager=place_element.diffbox_manager
    )
    manager.place = place_element
    return manager
