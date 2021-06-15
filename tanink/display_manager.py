from PIL import Image, ImageDraw, ImageFont
from IT8951 import constants

import config as cfg
import asyncio


class DisplayManager:
    def __init__(self, display, writing_manager):
        self.display = display
        self.writing_manager = writing_manager
        self.writing_buffer = []
        self.diff_box_to_erase = ()

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
        draw = ImageDraw.Draw(img)
        draw.text((0, 0), text, "#000", font=font)
        img = img.transpose(Image.FLIP_LEFT_RIGHT)

        self.display.frame_buf.paste(img, (draw_x, draw_y))

    def _place_blank_text_box(self):
        """ Erase last written text box
        """
        diff_box = self.writing_manager.get_diff_box()
        box_width = diff_box[2] - diff_box[0]
        box_height = diff_box[3] - diff_box[1]
        print("diff_box", diff_box)
        print("x_cursor", self.writing_manager.x_cursor)
        print("y_cursor", self.writing_manager.y_cursor)
        draw_x = self.writing_manager.x_cursor
        draw_y = self.writing_manager.y_cursor
        self.writing_manager.pop_diff_box()

        img = Image.new('L', (box_width, box_height), "#ffffff")
        draw = ImageDraw.Draw(img)
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
        dims = (self.display.width, self.display.height)
        
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
            if self.diff_box_to_erase:
                diff_box = self.diff_box_to_erase
                self.diff_box_to_erase = ()
                await self.display.draw_partial(
                    constants.DisplayModes.DU,
                    diff_box=diff_box
                )
            elif self.writing_buffer:
                text = ''.join(self.writing_buffer)
                self.writing_buffer = []

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
        else:
            diff_box = self._place_blank_text_box()
            if not self.diff_box_to_erase:
                self.diff_box_to_erase = diff_box
                print("diff box to erase (if)", self.diff_box_to_erase)
            else:
                # TODO: Handle diff boxes on different rows
                self.diff_box_to_erase = (
                    min(diff_box[0], self.diff_box_to_erase[0]),
                    min(diff_box[1], self.diff_box_to_erase[1]),
                    max(diff_box[2], self.diff_box_to_erase[2]),
                    max(diff_box[3], self.diff_box_to_erase[3])
                )
                print("diff box to erase (else)", self.diff_box_to_erase)
