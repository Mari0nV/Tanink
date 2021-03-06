import asyncio
from IT8951.display import VirtualEPDDisplay

from tanink.chapter import Chapter
from tanink.display_manager import DisplayManager
from tanink.keyboard_manager import KeyboardManager
from tanink.diffbox_manager import DiffBoxManager


async def keyboard_events(display_manager):
    keyboard_manager = KeyboardManager(display_manager)
    while True:
        keyboard_manager.check_key_pressed()
        await asyncio.sleep(0.1)


async def tasks(loop):
    display = VirtualEPDDisplay(dims=(1872, 1404))
    await asyncio.create_task(display.clear())

    diffbox_manager = DiffBoxManager()
    chapter = Chapter(id=0)
    display_manager = DisplayManager(
        display=display,
        diffbox_manager=diffbox_manager,
        chapter=chapter
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
