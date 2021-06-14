from PIL import Image, ImageDraw, ImageFont
from IT8951 import constants

import config as cfg


class DisplayManager:
    def __init__(self, display, writing_manager):
        self.display = display
        self.writing_manager = writing_manager

    def _place_written_text(self, text):
        """ Place written text
        """
        font = ImageFont.truetype(cfg.FONTPATH, cfg.FONTSIZE)
        text_width, _ = font.getsize(text)
        text_height = cfg.FONTSIZE

        self.writing_manager.move_cursors(text_width, text_height)
        draw_x = self.writing_manager.x_cursor
        draw_y = self.writing_manager.y_cursor

        img = Image.new('L', (text_width, text_height), "#ffffff")
        # img2.save('test_image.png', 'PNG')
        draw = ImageDraw.Draw(img)
        draw.text((0, 0), text, "#000", font=font)
        img = img.transpose(Image.FLIP_LEFT_RIGHT)

        self.display.frame_buf.paste(img, (draw_x, draw_y))


    def _place_blank_text_box(self):
        """ Erase last written text box
        """
        diff_box = self.writing_manager.get_diff_box()
        self.writing_manager.pop_diff_box()
        box_width = diff_box[2] - diff_box[0]
        box_height = diff_box[3] - diff_box[1]
        draw_x = self.writing_manager.x_cursor
        draw_y = self.writing_manager.y_cursor
        self.writing_manager.move_cursors(box_width, box_height, -1)

        img = Image.new('L', (box_width, box_height), "#ffffff")
        draw = ImageDraw.Draw(img)
        self.display.frame_buf.paste(img, (draw_x, draw_y))

        return diff_box


    def _place_writing_box(self):
        """ Place writing box (rectangle shape)
        """
        w, h = cfg.WRITING_RECT_WIDTH, cfg.WRITING_RECT_HEIGHT
        shape = [(0, 0), (w, h)]
        
        # creating new Image object
        img = Image.new("L", (w, h))
        
        # create rectangle image
        img1 = ImageDraw.Draw(img)  
        img1.rectangle(shape, fill ="#ffffff", outline ="grey", width=5)
        dims = (self.display.width, self.display.height)
        
        paste_coords = [cfg.WRITING_RECT_X, cfg.WRITING_RECT_Y]
        self.display.frame_buf.paste(img, paste_coords)

    def draw_writing_box(self):
        self._place_writing_box()
        self.display.draw_full(constants.DisplayModes.GC16)

    def draw_written_text(self, text):
        print(f"Drawing '{text}'")
        self._place_written_text(text)
        self.display.draw_partial(
            constants.DisplayModes.DU,
            diff_box=self.writing_manager.get_diff_box()
        )
    
    def erase_last_written_text(self):
        diff_box = self._place_blank_text_box()
        self.display.draw_partial(
            constants.DisplayModes.DU,
            diff_box=diff_box
        )
