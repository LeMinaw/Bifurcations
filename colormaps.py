"""Linear colormaps."""

from utils import clamp, lin_interp

class ColorMap:
    """Basic linear colormaps."""

    def __init__(self, start, end):
        """Creates a new ColorMap.
        - start: Start color
        - end: End color
        Colors are 8-bit RGB colors, so (r, g, b) tuples of integers in [0, 255]."""
        self.start, self.end = start, end

    def __call__(self, x, start=0, end=1, max_out=255):
        """Will map a value to a color.
        - x: The value a color will be mapped to
        - start: Value that will be mapped to the ColorMap start color
        - end: Value that will be mapped to the ColorMap end color"""
        return tuple([clamp(lin_interp(x, start, end, self.start[i], self.end[i]) / 255 * max_out, 0, max_out) for i in range(3)])


black           = ColorMap((000, 000, 000), (000, 000, 000))
white_to_black  = ColorMap((000, 000, 000), (255, 255, 255))
blue_to_red     = ColorMap((000, 000, 255), (255, 000, 000))
cyan_to_red     = ColorMap((000, 255, 255), (255, 000, 000))
black_to_red    = ColorMap((000, 000, 000), (255, 000, 000))
red_to_black    = ColorMap((255, 000, 000), (000, 000, 000))
blue_to_black   = ColorMap((000, 190, 255), (000, 000, 000))
orange_to_black = ColorMap((255, 145, 000), (000, 000, 000))
