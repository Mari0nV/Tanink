from PIL import Image, ImageDraw, ImageFont
import re

import config as cfg


class PlaceElement:
    """ Place various elements on screen such as:
        - written text box
        - blank text box (for when text is erased)
        - writing box (big rectangle box)
    """
    def __init__(self, display, writing_manager):
        self.display = display
        self.writing_manager = writing_manager

        self.font_size = cfg.FONTSIZE
        self.font = ImageFont.truetype(cfg.FONTPATH, self.font_size)
        self.transpose = cfg.TRANSPOSE

        self.last_word = ""
        self.word_delimiter = "[\\.,;\\-: ]"

    def _update_last_word(self, text=None, nb_box=1):
        """ Update last word:
            - add character if text is a continuity of a word
            - replace last word if the beginning new word is present in text
            - remove character if there is no text
        """
        if text:
            for character in text:
                if not re.match(f'{self.word_delimiter}' + '{1}', character):
                    self.last_word += character
                else:
                    self.last_word = ""
        else:
            self.last_word = self.last_word[:-nb_box]

    def _has_new_word(self, text):
        """ Return True if text contains the beginning of a new word.
        """
        if not self.last_word:
            return True

        if " " in text:
            return True

        if re.match(f'{self.word_delimiter}+[^{self.word_delimiter[1:]}+{self.word_delimiter}*$', text):
            # for strings like 'a,a' or ',a,'
            return True

        return False

    def move_word_on_new_row(self, text):
        """ Move text and previous letters on next row if there is not enough space for the entire word.
        """
        for index, character in enumerate(text):
            width, _ = self.font.getsize(character)
            if self.writing_manager.no_more_space(width) and not re.match(self.word_delimiter, character):
                if index == 0:
                    # move the content of last word + text down
                    last_word_width = self.font.getsize(self.last_word)
                    self.place_blank_text_box(last_word_width)
                    total_width = self.font.getsize(self.last_word + self.text)
                    self.writing_manager.move_cursors(total_width, self.font_size, new_row=True)
                    draw_x, draw_y = self._compute_drawing_box(total_width)

    def _compute_drawing_box(self, width=None, forward=True):
        if forward:  # cursor is after the character that has just been added
            if self.transpose:
                # drawing box starts at cursors after they move
                draw_x, draw_y = self.writing_manager.get_cursors()
            else:
                # drawing box starts at cursors before they move
                draw_x, draw_y = self.writing_manager.get_prev_cursors()
        else:  # cursors is before the blank box that has just been added
            if self.transpose:
                # drawing box starts at cursors before they move
                draw_x, draw_y = self.writing_manager.get_prev_cursors()
            else:
                # drawing box starts at cursors after they move
                draw_x, draw_y = self.writing_manager.get_cursors()
        
        return draw_x, draw_y

    def place_written_text(self, text):
        """ Place written text
        """
        text_width, _ = self.font.getsize(text)
        text_height = self.font_size

        if self.writing_manager.no_more_space(text_width) and not self._has_new_word(text):
            self.move_word_on_new_row(text)
            return

        self._update_last_word(text)
        self.writing_manager.move_cursors(text_width, text_height)
        draw_x, draw_y = self._compute_drawing_box()
    
        img = Image.new('L', (text_width, text_height), "#ffffff")
        draw = ImageDraw.Draw(img)
        draw.text((0, 0), text, "#000", font=self.font)
        if self.transpose:
            img = img.transpose(Image.FLIP_LEFT_RIGHT)

        self.display.frame_buf.paste(img, (draw_x, draw_y))

    def place_blank_text_box(self, width=None):
        """ Erase last written text box
        """
        if width:
            nb_box = self.writing_manager.pop_diff_box(width)
            draw_x, draw_y = self._compute_drawing_box(width, forward=False)
            height = self.font_size
        else:
            nb_box = 1
            diff_box = self.writing_manager.get_diff_box()
            if diff_box:
                width = diff_box[2] - diff_box[0]
                height = diff_box[3] - diff_box[1]
                self.writing_manager.pop_diff_box()
                draw_x, draw_y = self._compute_drawing_box(forward=False)
            else:
                return

        self._update_last_word(nb_box=nb_box)
        img = Image.new('L', (width, height), "#ffffff")
        self.display.frame_buf.paste(img, (draw_x, draw_y))

        return diff_box

    def place_writing_box(self):
        """ Place writing box (rectangle shape)
        """
        w, h = cfg.WRITING_RECT_WIDTH, cfg.WRITING_RECT_HEIGHT
        shape = [(0, 0), (w, h)]
        img = Image.new("L", (w, h))
        img1 = ImageDraw.Draw(img)  
        img1.rectangle(shape, fill ="#ffffff", outline ="grey", width=5)
        
        paste_coords = [cfg.WRITING_RECT_X, cfg.WRITING_RECT_Y]
        self.display.frame_buf.paste(img, paste_coords)
