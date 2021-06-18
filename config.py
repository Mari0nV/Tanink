
TRANSPOSE = False

# Text config
FONTSIZE = 60
FONTPATH = 'assets/FreeSans.ttf'
TEXT_SPACING = 3

# Writing box dimensions and position - use multiples of 4
# Screen is 1872×1404
WRITING_RECT_Y = 100
WRITING_RECT_WIDTH = 1100
if TRANSPOSE:
    WRITING_RECT_X = 100
else:
    WRITING_RECT_X = 1872 - (WRITING_RECT_WIDTH + 100)
WRITING_RECT_HEIGHT = 1200
WRITING_RECT_MARGIN = 8
