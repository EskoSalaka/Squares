import sys
import numpy
from numba import jit

from PIL import Image, ImageFilter


def update_progress(n, tot):
    """A simple progress indicator."""
    sys.stdout.write("\r[{} / {}]".format(n, tot))


def to_pixel_array(array, square_color, background_color):
    """
    Converts the numpy 2d-array of 1's and 0's to a image data-array. The data array will simply have the given
    RGB-color array [R, G, B], square_color, in place of ones and the given background_color in place of zeros.

    :param array: A numpy 2d-array of 1's and 0's
    :param square_color: An RGB color array to paint the squares
    :param background_color: An RGB color array to paint the background
    :return: An image data-array
    """
    pixel_array = numpy.zeros((array.shape[0], array.shape[1], 3), dtype=numpy.uint8)

    for y in range(len(pixel_array)):
        for x in range(len(array[y])):
            if array[y][x]:
                pixel_array[y][x] = square_color
            else:
                pixel_array[y][x] = background_color

    return pixel_array.astype("uint8")


def create_squares(first_line, width, height, painter_func, *func_extras, custom_first_line=None, progress=True):
    """
    Creates an array of 1's and 0's of given width and height where 1's represent painted squares. The squares are
    painted according to a given function 'painter_func'. he structure of the 'painter_func' is described in more detail
    later.Basically, each 'square', or element of the array, is iterated and passed to the 'painter_func', which in
    turn either paints the square according to its logic. It is used in the following way:
    squares_iterator[0] = painter_func(squares, n, h, x, func_extras)

    Optinally a first line, or row, can be specified with 'first_line'. The legal arguments for 'first_line' are:
    'random' -- fills the first line randomly
    'ones' -- fills the first line with ones
    'zeros' -- fills the first line with zeros.
    'custom' -- fills the first line with the given 'custom_first_line'
    'none' -- leaves the first line empty.

    In case the 'first_line' is something other than 'none', the iteration process will begin from the second line!

    :param first_line: What kind of first line, or row, to have. Either 'random', 'ones', 'zeros', 'custom' or 'none'
    :param width: The width of the canvas in squares (pixels)
    :param height: The height of the canvas in squares (pixels)
    :param painter_func: The painter function which paints the squares according to some logic
    :param custom_first_line: In case 'custom' was specified as the 'first line', this will be set as the first line
    :param progress: Boolean value to specify if a simple progress message is displayed while iterating
    :param func_extras: Any extras the painter_func needs, leave empty otherwise
    :return: A numpy 2d-array of 1's and 0's representing painted and non-painted squares
    """
    squares = numpy.zeros((height, width), dtype=numpy.uint8)
    squares_iterator = numpy.nditer(squares, op_flags=['writeonly'], flags=['multi_index'])

    if first_line == 'random':
        for _ in range(width):
            squares_iterator[0] = numpy.random.randint(0, 2)
            squares_iterator.iternext()
    elif first_line == 'zeros':
        for _ in range(width):
            squares_iterator.iternext()
    elif first_line == 'ones':
        for _ in range(width):
            squares_iterator[0] = 1
            squares_iterator.iternext()
    elif first_line == 'custom':
        for _ in range(width):
            squares_iterator[0] = custom_first_line[squares_iterator.multi_index[1]]
            squares_iterator.iternext()
    elif first_line == 'none':
        pass
    else:
        print('Wrong positional argument for "first_line"')

    tot = width * height
    while not squares_iterator.finished:
        h = squares_iterator.multi_index[0]
        x = squares_iterator.multi_index[1]
        n = width * h + x + 1

        squares_iterator[0] = painter_func(squares, n, h, x, func_extras)

        if progress:
            update_progress(n, tot)

        squares_iterator.iternext()

    return squares


def paint(array, square_color, background_color, save_loc='squares.BMP'):
    """Converts the given numpy 2d-array to an image data-array and creates an image from it."""
    image = Image.fromarray(to_pixel_array(array, square_color, background_color), mode='RGB')
    image.save(save_loc, "BMP", quality=95, optimize=True)
    image.show()


def painter_func_demo(array, n, h, x, *extras):
    """
    A simple demostration of how the painter func works. Generally, these functions require the 2d-numpy array itself,
    the current square number n, the row number h, the current column index x and a list of extras, which can be
    anything. They always return either 1 or 0 representing a painted or non-painted square.

    This one simply paints the square if the square number n is even.

    :param array: A numpy 2d-array of 1's and 0's
    :param n: The current square number
    :param h: The current row
    :param x: The current column index
    :param extras: A list of any extra the func needs
    :return: Either 1 to paint the square or 0 to leave it empty
    """

    return 1 if n % 2 == 0 else 0
