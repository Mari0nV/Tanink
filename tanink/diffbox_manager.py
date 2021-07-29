from math import ceil

import config as cfg


class DiffBoxManager:
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
        self._fontsize = cfg.FONTSIZE
        self.rounded_fontsize = self._round_to(self._fontsize)
        self.row_height = self.rounded_fontsize + self.text_spacing
        self._x_cursor = self.get_x_cursor_start()
        self._y_cursor = self.rect_y + self.rect_margin
        self.prev_x_cursor = self.x_cursor
        self.prev_y_cursor = self.y_cursor
        self.diff_boxes = []
        self.row_index = 0

    @property
    def y_cursor(self):
        return self._y_cursor

    @y_cursor.setter
    def y_cursor(self, value):
        self.prev_y_cursor = self._y_cursor
        self._y_cursor = self._round_to(value)

        if self._y_cursor > self.prev_y_cursor:
            self.row_index += 1
        elif self._y_cursor < self.prev_y_cursor:
            self.row_index -= 1

    @property
    def x_cursor(self):
        return self._x_cursor

    @x_cursor.setter
    def x_cursor(self, value):
        self.prev_x_cursor = self._x_cursor
        self._x_cursor = self._round_to(value)

    @property
    def fontsize(self):
        return self._fontsize

    @fontsize.setter
    def fontsize(self, value):
        self._fontsize = value
        self.rounded_fontsize = self._round_to(value)
        self.row_height = self.rounded_fontsize + self.text_spacing

    def get_x_cursor_start(self):
        """ Return x cursor value at row start.
            This value depends on the coordinate system (given by the transpose variable)
        """
        return self.rect_x + self.rect_width * int(self.transpose) + (-1)**(int(self.transpose)) * self.rect_margin

    def move_cursors_on_new_row(self):
        self.y_cursor += self.row_height
        self.x_cursor = self.get_x_cursor_start()

    def move_cursors(self, width, direction=1, round_to=4, new_row=False, nb_box=1):
        """ Move x and y cursors according to the dimensions of the new box.
            Add the new box into the list of diff boxes if direction is not -1.
            (direction = -1 if it's a box to erase)
        """
        # If new row, cursors are moved to the next row
        if new_row:
            self.move_cursors_on_new_row()

        # rounding width and height to have the right dimensions when computing diff box
        width = int(width / nb_box)
        width = self._round_to(width, round_to=round_to)

        for _ in range(nb_box):
            if direction == 1:  # display a new box on screen
                # we need to display the box on a new row
                if self.no_more_space(width):
                    self.move_cursors_on_new_row()
                self.x_cursor += width * (-1)**int(self.transpose)
                self._add_diff_box()
            elif self.diff_boxes:  # user wants to go back
                # there is space to go back staying on the same row
                if abs(self.get_x_cursor_start() - self.x_cursor) >= abs((-1)**(int(self.transpose) + 1) * width):
                    self.x_cursor += (-1)**(int(self.transpose) + 1) * width
                # we need to go back on last row
                elif self.y_cursor > self.rect_y + self.rect_margin:
                    self.y_cursor -= self.row_height
                    self.x_cursor = self.diff_boxes[-2][2 *
                                                        int(not self.transpose)]

    def _round_to(self, value, round_to=4, nb_box=1):
        """ Round a value to be a multiple of 4.
            It's necessary to update the e-paper screen correctly.
        """
        box_value = ceil(value / nb_box)
        new_value = 0
        for _ in range(nb_box):
            new_value += box_value + round_to - 1 - (value - 1) % round_to
        return new_value

    def _add_diff_box(self, nb_box=1):
        min_x = min(self.x_cursor, self.prev_x_cursor)
        min_y = min(self.y_cursor, self.y_cursor + self.rounded_fontsize)
        max_x = max(self.x_cursor, self.prev_x_cursor)
        max_y = max(self.y_cursor, self.y_cursor + self.rounded_fontsize)
        box_width = (max_x - min_x) / nb_box

        for i in range(nb_box):
            self.diff_boxes.append((
                int(min_x + i * box_width),
                min_y,
                int(min_x + (i + 1) * box_width),
                max_y
            ))

    def get_cursors(self):
        return self.x_cursor, self.y_cursor

    def get_prev_cursors(self):
        return self.prev_x_cursor, self.prev_y_cursor

    def get_row_start_cursors(self):
        """ Get the coordinates of the start of current row.
            Useful to compute large diff boxes to update.
        """
        return self.get_x_cursor_start(), self.y_cursor

    def get_row_diff_box(self, nb_rows=1):
        if nb_rows:
            x_start = self.get_x_cursor_start()
            x_end = self.rect_x + self.rect_width * \
                int(not self.transpose) - self.rect_margin * \
                (-1)**int(self.transpose)
            if x_start > x_end:
                x_start, x_end = x_end, x_start
            y_end = self.y_cursor + self.row_height
            if nb_rows <= (self.row_index + 1):
                y_start = y_end - nb_rows * self.row_height
            else:
                y_start = y_end - (self.row_index + 1) * self.row_height

            return (x_start, y_start, x_end, y_end)

    def no_more_space(self, width):
        """ Return True if there is no space on the row for a box with specific width.
        """
        remaining_width = (self.rect_x - self.x_cursor) * (-1)**int(self.transpose) \
            - self.rect_margin + self.rect_width * int(not self.transpose)
        if remaining_width >= width:
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
        """
            Remove diff boxes from self.diff_boxes and return them.
            If width is not specified, do that for last diff box.
        """
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
                self.move_cursors(box_width, direction=-1)
                for _ in range(nb_box):
                    self.diff_boxes.pop()
                return diff_box, nb_box

        elif self.diff_boxes:
            diff_box = self.get_diff_box()
            width = self.diff_boxes[-1][2] - self.diff_boxes[-1][0]
            self.move_cursors(width, direction=-1)
            self.diff_boxes.pop()
            return diff_box, 1

        return None, 0
