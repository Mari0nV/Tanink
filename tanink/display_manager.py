from PIL import Image, ImageDraw, ImageFont
from IT8951 import constants

import config as cfg
import asyncio


class DisplayManager:
    def __init__(self, display, writing_manager):
        self.display = display
        self.writing_manager = writing_manager
        self.writing_buffer = []
        self.diff_boxes_to_erase = []
        self.font_path = cfg.FONTPATH
        self.font_size = cfg.FONTSIZE
        self.transpose = cfg.TRANSPOSE

    def _place_written_text(self, text):
        """ Place written text
        """
        font = ImageFont.truetype(self.font_path, self.font_size)
        text_width, _ = font.getsize(text)
        text_height = self.font_size

        self.writing_manager.move_cursors(text_width, text_height)
        if self.transpose:
            # drawing box starts at cursors after they move
            draw_x = self.writing_manager.x_cursor
            draw_y = self.writing_manager.y_cursor
        else:
            # drawing box starts at cursors before they move
            draw_x = self.writing_manager.prev_x_cursor
            draw_y = self.writing_manager.prev_y_cursor
    
        img = Image.new('L', (text_width, text_height), "#ffffff")
        draw = ImageDraw.Draw(img)
        draw.text((0, 0), text, "#000", font=font)
        if self.transpose:
            img = img.transpose(Image.FLIP_LEFT_RIGHT)

        self.display.frame_buf.paste(img, (draw_x, draw_y))

    def _place_blank_text_box(self):
        """ Erase last written text box
        """
        diff_box = self.writing_manager.get_diff_box()
        if diff_box:
            box_width = diff_box[2] - diff_box[0]
            box_height = diff_box[3] - diff_box[1]
            self.writing_manager.pop_diff_box()
            if self.transpose:
                # drawing box starts at cursors before they move
                draw_x = self.writing_manager.prev_x_cursor
                draw_y = self.writing_manager.prev_y_cursor
            else:
                # drawing box starts at cursors after they move
                draw_x = self.writing_manager.x_cursor
                draw_y = self.writing_manager.y_cursor


            img = Image.new('L', (box_width, box_height), "#ffffff")
            self.display.frame_buf.paste(img, (draw_x, draw_y))

        return diff_box

    def _place_writing_box(self):
        """ Place writing box (rectangle shape)
        """
        w, h = cfg.WRITING_RECT_WIDTH, cfg.WRITING_RECT_HEIGHT
        shape = [(0, 0), (w, h)]
        img = Image.new("L", (w, h))
        img1 = ImageDraw.Draw(img)  
        img1.rectangle(shape, fill ="#ffffff", outline ="grey", width=5)
        
        paste_coords = [cfg.WRITING_RECT_X, cfg.WRITING_RECT_Y]
        self.display.frame_buf.paste(img, paste_coords)

    async def draw_writing_box(self):
        self._place_writing_box()
        await self.display.draw_full(constants.DisplayModes.GC16)

    def draw_written_text(self, text):
        print(f"Drawing '{text}'")
        self._place_written_text(text)
        self.writing_buffer.append(text)
    
    async def draw_buffer(self):
        while True:
            while self.diff_boxes_to_erase:
                diff_box = self.diff_boxes_to_erase[0]
                self.diff_boxes_to_erase = self.diff_boxes_to_erase[1:]
                await self.display.draw_partial(
                    constants.DisplayModes.DU,
                    diff_box=diff_box
                )
            if self.writing_buffer:
                text = ''.join(self.writing_buffer)
                self.writing_buffer = []

                print("before draw partial")
                await self.display.draw_partial(
                    constants.DisplayModes.DU,
                    diff_box=self.writing_manager.get_diff_box(
                        size=len(text)
                    )
                )

            else:
                await asyncio.sleep(0.01)

    def erase_last_written_text(self):
        print("Erasing last written text")
        if self.writing_buffer:
            print("buffer", self.writing_buffer)
            self.writing_buffer.pop()
            self.writing_manager.pop_diff_box()
        else:
            diff_box = self._place_blank_text_box()
            if diff_box:
                if not self.diff_boxes_to_erase:
                    self.diff_boxes_to_erase.append(diff_box)
                    print("diff box to erase (if)", self.diff_boxes_to_erase)
                else:
                    last_box = self.diff_boxes_to_erase[-1]
                    if diff_box[1] == last_box[1]:  # boxes on same row
                        self.diff_boxes_to_erase.pop()
                        self.diff_boxes_to_erase.append((
                            min(diff_box[0], last_box[0]),
                            diff_box[1],
                            max(diff_box[2], last_box[2]),
                            diff_box[3]
                        ))
                        print("diff box to erase (else)", self.diff_boxes_to_erase)
                    else:
                        self.diff_boxes_to_erase.append(diff_box)
