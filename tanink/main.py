from IT8951.display import AutoEPDDisplay

from tanink.writing_manager import WritingManager
from tanink.display_manager import DisplayManager


def main():
        display = AutoEPDDisplay(vcom=-2.36, rotate=None, spi_hz=24000000)
        display.clear()

        writing_manager = WritingManager()
        display_manager = DisplayManager(
            display=display,
            writing_manager=writing_manager
        )

        # Display writing box
        display_manager.draw_writing_box()

        # Display letters
        display_manager.draw_written_text('a')
        display_manager.draw_written_text('b')
        display_manager.draw_written_text('c')
        
        display_manager.erase_last_written_text()

        display_manager.draw_written_text('d')


if __name__ == '__main__':
    main()
