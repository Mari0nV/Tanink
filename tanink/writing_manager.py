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
    
    def move_cursors(self, width, height, direction=1):
        prev_x_cursor = self.x_cursor
        prev_y_cursor = self.y_cursor
        if self.x_cursor - self.writing_rect_x > width:
            self.x_cursor -= width * direction
        else:
            self.y_cursor += height * direction + self.text_spacing
            self.x_cursor = self.writing_rect_x + self.writing_rect_width - self.writing_rect_margin
            self.x_cursor -= width * direction
        
        self._add_diff_box(
            self.x_cursor, prev_x_cursor, self.y_cursor, self.y_cursor + height
        )

    def _add_diff_box(self, min_x, max_x, min_y, max_y, round_to=4):
        min_x -= min_x % round_to
        max_x += round_to-1 - (max_x-1) % round_to
        min_y -= min_y % round_to
        max_y += round_to-1 - (max_y-1) % round_to

        self.diff_boxes.append(
            (min_x, min_y, max_x, max_y)
        )

    def get_diff_box(self):
        return self.diff_boxes[-1]

    def pop_diff_box(self):
        self.diff_boxes.pop()
