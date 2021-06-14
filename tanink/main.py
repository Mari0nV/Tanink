from IT8951.display import AutoEPDDisplay

from tanink.writing_manager import WritingManager
from tanink.display_manager import DisplayManager
import asyncio


async def keyboard_events(display_manager):
    await asyncio.sleep(1)
    display_manager.draw_written_text('a')
    display_manager.draw_written_text('a')
    await asyncio.sleep(1)
    display_manager.erase_last_written_text()
    display_manager.erase_last_written_text()
    display_manager.draw_written_text('b')


async def tasks(loop):
    display = AutoEPDDisplay(vcom=-2.36, rotate=None, spi_hz=24000000)
    await asyncio.create_task(display.clear())

    writing_manager = WritingManager()
    display_manager = DisplayManager(
        display=display,
        writing_manager=writing_manager
    )

    # Display writing box
    await asyncio.create_task(display_manager.draw_writing_box())
    keyboard = loop.create_task(keyboard_events(display_manager))
    update = loop.create_task(display_manager.draw_buffer())

    await keyboard
    await update


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(tasks(loop))


if __name__ == '__main__':
    main()
