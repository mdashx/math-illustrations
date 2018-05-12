'''
How would you set the current color to green? Pink? Violet? Orange?

Point is 1/72 inch

8.5′′ × 11′′ ==  612 × 792 points2
'''

from collections import namedtuple
import colorsys
from itertools import cycle

FILENAME = './tmp.ps'

PAGE_WIDTH = 612
PAGE_HEIGHT = 792

GREEN = '00ff00'
RED = 'ff0000'  # Will turn into pink as it gets lighter (to meet requirements of the exercise)
VIOLET = 'ff00ff'
ORANGE = 'ff6a00'
BLUE = '0000ff'
BLACK = '000000'
WHITE = 'ffffff'

Position = namedtuple('Position', ['x', 'y'])


def get_color_from_hex(hexcode):
    color_values = map(''.join, zip(*[iter(hexcode)] * 2))
    return tuple([int(color, 16) / 255.0 for color in color_values])


def set_color(color):
    return f'{color} setrgbcolor'


def fill_square(start_x, start_y, width):
    square_code = []
    square_code.append('newpath')
    square_code.append(f'{start_x} {start_y} moveto')
    square_code.append(f'{width} 0 rlineto 0 {width} rlineto -{width} 0 rlineto')
    square_code.append(f'closepath fill')
    return '\n'.join(square_code)


def extra_column(how_many_squares, num_columns):
    if (how_many_squares % num_columns) > 0:
        return 1
    else:
        return 0


def get_positions(margin, offset, width, how_many_squares):
    positions = []
    num_columns = (PAGE_WIDTH - margin) // (width + offset)
    num_rows = how_many_squares // num_columns + extra_column(how_many_squares, num_columns)

    for i in range(0, num_rows):
        for j in range(0, num_columns):
            x = margin + offset * j + width * j
            y = PAGE_HEIGHT - width - width * i - margin - offset * i
            positions.append(Position(x, y))

    return positions, num_columns, num_rows


def get_colors(start_colors, num_columns, num_rows):
    lighten_degree = 1.0 / num_rows
    start_colors = cycle(start_colors)
    first_row = [start_colors.__next__() for i in range(num_columns)]
    for i in range(num_rows):
        for j in range(num_columns):
            original_color = colorsys.rgb_to_hls(*get_color_from_hex(first_row[j]))
            lighter_color = list(original_color)
            lighten_factor = lighten_degree * i
            lightness = original_color[1]
            if lighten_factor > 0:
                lighter_color[1] = lightness + (lightness * lighten_factor)
            yield colorsys.hls_to_rgb(*lighter_color)


def main():
    margin = 10
    offset = 5
    width = 144
    how_many_squares = 20

    positions, num_columns, num_rows = get_positions(margin, offset, width, how_many_squares)

    start_colors = [GREEN, RED, VIOLET, ORANGE]
    colors = iter(get_colors(start_colors, num_columns, num_rows))

    ps_code = ['%!']

    for position in positions:
        ps_code.append(set_color(' '.join([str(c) for c in colors.__next__()])))
        ps_code.append(fill_square(position.x, position.y, width))
        ps_code.append('\n')
    print('\n'.join(ps_code))


if __name__ == '__main__':
    main()
