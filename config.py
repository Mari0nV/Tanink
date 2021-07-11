
TRANSPOSE = False

# Text config
FONTSIZE = 60
FONTPATH = 'assets/FreeSans.ttf'
TEXT_SPACING = 4

# Writing box dimensions and position - use multiples of 4
# Screen is 1872×1404
WRITING_RECT_Y = 100
# WRITING_RECT_WIDTH = 1100
WRITING_RECT_WIDTH = 180
if TRANSPOSE:
    WRITING_RECT_X = 8
else:
    WRITING_RECT_X = 600 - (WRITING_RECT_WIDTH + 8)
WRITING_RECT_HEIGHT = 408
WRITING_RECT_MARGIN = 8
