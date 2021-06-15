import config as cfg


class WritingManager:
    def __init__(self):
        self.writing_rect_x = cfg.WRITING_RECT_X
        self.writing_rect_y = cfg.WRITING_RECT_Y
        self.writing_rect_width = cfg.WRITING_RECT_WIDTH
        self.writing_rect_height = cfg.WRITING_RECT_HEIGHT
        self.writing_rect_margin = cfg.WRITING_RECT_MARGIN
        self.text_spacing = cfg.TEXT_SPACING

        self.x_cursor = self.writing_rect_x + self.writing_rect_width - self.writing_rect_margin
        self.y_cursor = self.writing_rect_y + self.writing_rect_margin
        self.diff_boxes = []
    
    def move_cursors(self, width, height, direction=1, round_to=4):
        """ Move x and y cursors according to the dimensions of the new box.
            Add the new box into the list of diff boxes if direction is not -1.
            (direction = -1 if it's a box to erase)
        """
        # rounding width and height to have the right dimensions when computing diff box
        width += round_to - 1 - (width - 1) % round_to
        height += round_to - 1 - (height - 1) % round_to

        prev_x_cursor = self.x_cursor
        prev_y_cursor = self.y_cursor
        if direction == 1:  # display a new box on screen
            # there is space on the screen row to display a new box
            if self.x_cursor - self.writing_rect_x >= width:
                self.x_cursor -= width
            # we need to display the box on a new row
            else:
                self.y_cursor += height + self.text_spacing
                prev_x_cursor = self.writing_rect_x + self.writing_rect_width - self.writing_rect_margin
                self.x_cursor = prev_x_cursor - width
            self.diff_boxes.append((
                min(self.x_cursor, prev_x_cursor),
                min(self.y_cursor, self.y_cursor + height),
                max(self.x_cursor, prev_x_cursor),
                max(self.y_cursor, self.y_cursor + height),
            ))
        elif self.diff_boxes:  # user wants to go back
            # there is space to go back staying on the same row
            if self.writing_rect_x + self.writing_rect_width - self.writing_rect_margin - self.x_cursor >= width:
                self.x_cursor += width
            # we need to go back on last row
            elif self.y_cursor > self.writing_rect_y + self.writing_rect_margin:
                self.y_cursor -= (height + self.text_spacing)
                self.x_cursor = self.diff_boxes[-2][0]

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

    def pop_diff_box(self):
        if self.diff_boxes:
            width = self.diff_boxes[-1][2] - self.diff_boxes[-1][0]
            height = self.diff_boxes[-1][3] - self.diff_boxes[-1][1]
            self.move_cursors(width, height, direction=-1)
            self.diff_boxes.pop()
