from math import ceil

import config as cfg


class WritingManager:
    """ Manage x and y cursors in writing box, when adding or removing text.
        Save computed diff boxes in a list, to have memory of where text has been
        written.
    """

    def __init__(self, transpose=cfg.TRANSPOSE):
        self.transpose = transpose
        self.rect_x = cfg.WRITING_RECT_X
        self.rect_y = cfg.WRITING_RECT_Y
        self.rect_width = cfg.WRITING_RECT_WIDTH
        self.rect_height = cfg.WRITING_RECT_HEIGHT
        self.rect_margin = cfg.WRITING_RECT_MARGIN
        self.text_spacing = cfg.TEXT_SPACING

        if self.transpose:
            self.x_cursor = self.rect_x + self.rect_width - self.rect_margin
        else:
            self.x_cursor = self.rect_x + self.rect_margin
        self.y_cursor = self.rect_y + self.rect_margin
        self.prev_x_cursor = self.x_cursor
        self.prev_y_cursor = self.y_cursor
        self.diff_boxes = []

    def move_cursors(self, width, height, direction=1, round_to=4, new_row=False, nb_box=1):
        """ Move x and y cursors according to the dimensions of the new box.
            Add the new box into the list of diff boxes if direction is not -1.
            (direction = -1 if it's a box to erase)
        """
        # rounding width and height to have the right dimensions when computing diff box
        width = self._round_to(width, round_to=round_to, nb_box=nb_box)
        height = self._round_to(height, round_to=round_to, nb_box=nb_box)

        self.prev_x_cursor = self.x_cursor
        self.prev_y_cursor = self.y_cursor
        if direction == 1:  # display a new box on screen
            # we need to display the box on a new row
            if self.no_more_space(width) or new_row:
                self.y_cursor += height + self.text_spacing
                if self.transpose:
                    self.prev_x_cursor = self.rect_x + self.rect_width - self.rect_margin
                    self.x_cursor = self.prev_x_cursor - width
                else:
                    self.prev_x_cursor = self.rect_x + self.rect_margin
                    self.x_cursor = self.prev_x_cursor + width
            # there is space on the screen row to display a new box
            else:
                self.x_cursor += width * (-1)**int(self.transpose)
            self._add_diff_box(height, nb_box)
        elif self.diff_boxes:  # user wants to go back
            # there is space to go back staying on the same row
            if self.transpose and self.rect_x + self.rect_width - self.rect_margin - self.x_cursor >= width:
                self.x_cursor += width
            elif not self.transpose and self.x_cursor - width >= self.rect_x + self.rect_margin:
                self.x_cursor -= width
            # we need to go back on last row
            elif self.y_cursor > self.rect_y + self.rect_margin:
                self.y_cursor -= (height + self.text_spacing)
                if self.transpose:
                    self.x_cursor = self.diff_boxes[-2][0]
                else:
                    self.x_cursor = self.diff_boxes[-2][2]

    def _round_to(self, value, round_to=4, nb_box=1):
        box_value = ceil(value / nb_box)
        new_value = 0
        for i in range(nb_box):
            new_value += box_value + round_to - 1 - (value - 1) % round_to
        return new_value

    def _add_diff_box(self, height, nb_box=1):
        min_x = min(self.x_cursor, self.prev_x_cursor)
        min_y = min(self.y_cursor, self.y_cursor + height)
        max_x = max(self.x_cursor, self.prev_x_cursor)
        max_y = max(self.y_cursor, self.y_cursor + height)
        box_width = (max_x - min_x) / nb_box

        for i in range(nb_box):
            self.diff_boxes.append((
                min_x + i * box_width,
                min_y,
                min_x + (i + 1) * box_width,
                max_y
            ))

    def get_cursors(self):
        return self.x_cursor, self.y_cursor

    def get_prev_cursors(self):
        return self.prev_x_cursor, self.prev_y_cursor

    def no_more_space(self, width):
        """ Return True if there is no space on the row for a box with specific width.
        """
        if self.transpose and self.x_cursor - self.rect_x >= width + self.rect_margin:
            return False
        elif not self.transpose and self.x_cursor + width + self.rect_margin <= self.rect_x + self.rect_width:
            return False

        return True

    def get_diff_box(self, size=None):
        if self.diff_boxes:
            if size is None:
                return self.diff_boxes[-1]
            else:
                min_x = min([box[0] for box in self.diff_boxes[-size:]])
                min_y = min([box[1] for box in self.diff_boxes[-size:]])
                max_x = max([box[2] for box in self.diff_boxes[-size:]])
                max_y = max([box[3] for box in self.diff_boxes[-size:]])
                return (min_x, min_y, max_x, max_y)

    def pop_diff_box(self, width=None):
        if width:
            box_width = 0
            nb_box = 0
            while width > box_width:
                if len(self.diff_boxes) > nb_box:
                    box_width += self.diff_boxes[-nb_box][2] - \
                        self.diff_boxes[-nb_box][0]
                    nb_box += 1
                else:
                    break
            if nb_box:
                diff_box = self.get_diff_box(nb_box)
                height = self.diff_boxes[-1][3] - self.diff_boxes[-1][1]
                self.move_cursors(box_width, height, direction=-1)
                for i in range(nb_box):
                    self.diff_boxes.pop()
                return diff_box, nb_box

        elif self.diff_boxes:
            diff_box = self.get_diff_box()
            width = self.diff_boxes[-1][2] - self.diff_boxes[-1][0]
            height = self.diff_boxes[-1][3] - self.diff_boxes[-1][1]
            self.move_cursors(width, height, direction=-1)
            self.diff_boxes.pop()
            return diff_box, 1

        return None, 0
