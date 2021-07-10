from IT8951 import constants
import asyncio

from tanink.place_element import PlaceElement


class DisplayManager:
    """ Manage the display of text on the screen.
        Place or remove text boxes and update the screen.
    """

    def __init__(self, display, diffbox_manager):
        self.display = display
        self.diffbox_manager = diffbox_manager
        self.place = PlaceElement(
            display=display,
            diffbox_manager=diffbox_manager
        )

        self.writing_buffer = []
        self.diff_boxes_to_erase = []

    async def draw_writing_box(self):
        self.place.place_writing_box()
        await self.display.draw_full(constants.DisplayModes.GC16)

    def draw_written_text(self, text):
        print(f"Drawing '{text}'")
        self.place.place_written_text(text)
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
                if self.place.box_to_update:  # multiple lines to update (a word has been moved)
                    diff_box = self.place.box_to_update
                else:
                    diff_box = self.diffbox_manager.get_diff_box(
                        size=len(text)
                    )
                print("diffbox to update", diff_box)
                await self.display.draw_partial(
                    constants.DisplayModes.DU,
                    diff_box=diff_box
                )

            else:
                await asyncio.sleep(0.01)

    def erase_last_written_text(self):
        print("Erasing last written text")
        if self.writing_buffer:
            print("buffer", self.writing_buffer)
            self.writing_buffer.pop()
            self.diffbox_manager.pop_diff_box()
        else:
            diff_box = self.place.place_blank_text_box()
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
                        print("diff box to erase (else)",
                              self.diff_boxes_to_erase)
                    else:
                        self.diff_boxes_to_erase.append(diff_box)
