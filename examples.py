import math
import numpy
from squares import paint, create_squares
# from numba import jit


########################################################################################################################
# Some handy math functions
########################################################################################################################

def is_prime(n):
    if n % 2 == 0 and n > 2:
        return False
    return 1 if all(n % i for i in range(3, int(math.sqrt(n)) + 1, 2)) else 0


def fib(n):
    return int((1 + math.sqrt(5))**n - (1 - math.sqrt(5))**n) / (2**n*math.sqrt(5))


def is_fibonacci(n):
    phi = 0.5 + 0.5 * math.sqrt(5.0)
    a = phi * n
    return n == 0 or abs(round(a) - a) < 1.0 / n


def ulam_numbers(a, b, n):
    U = [a, b]
    i = 2

    for _ in [[0]] * (n - 2):
        t = _ * 3 * i

        for a in U:
            for b in U:
                t[a + b] += a != b
        i = t[i + 1:].index(2) + i + 1
        U += [i]

    return U


def divisor_sum(n):
    sum([i for i in range(1, n) if n % i == 0])


# Can be speeded up a lot with numba
# @jit
def mandelbrot(z, max_iterations=1000):
    c = z

    for _ in range(max_iterations):
        if abs(z) > 2:
            return 0
        else:
            z = pow(z, 2) + c

    return 1


########################################################################################################################
# Some stuff. Feel free to add your own.
########################################################################################################################

def main():
    white = [255, 255, 255]
    black = [0, 0, 0]

    # # Primes of the first 1 000 000 numbers as squares.
    # s = create_squares('none', 1000, 1000, lambda array, n, h, x, *extras: is_prime(n))
    # paint(s, black, white, 'primes_1000x1000.BMP')

    # An interesting kind of Sierpinski-triangles: Paint the square if the sum of the number of painted squares of all
    # the above rows, starting from each row's current column index is even.
    # s = create_squares('ones', 1000, 1000, lambda array, n, h, x, *extras: array[:h-1, x:].sum() % 2)
    # paint(s, black, white, 'gcd_ones_1000x1000.BMP')

    # Same, but with a random first line
    # s = create_squares('random', 1000, 1000, lambda array, n, h, x, *extras: array[:h, x:].sum() % 2)
    # paint(s, black, white, 'triangles_random_1000x1000.BMP')

    # Suprisingly, it's hard to see any pattern if we do the same as above but check for divisibility by 3
    # s = create_squares('ones', 1000, 1000, lambda array, n, h, x, *extras: 1 if array[:h, x:].sum() % 3 == 0 else 0)
    # paint(s, black, white, 'div_3_1000x1000.BMP')

    # And again the same with a random first line
    # s = create_squares('random', 1000, 1000, lambda array, n, h, x, *extras: 1 if array[:h, x:].sum() % 3 == 0 else 0)
    # paint(s, black, white, 'div_3_1000x1000.BMP')

    # Color the square if the three above squares are mirror-symmetric starting with a random first line
    # def mirror_symmetric_3(array, n, h, x, *extras):
    #     a = array[h - 1][x - 1]
    #     c = array[h - 1][x + 1] if x + 1 < array[h - 1].size else array[h - 1][0]
    #     return 1 if (a and c) or (not a and not c) else 0
    #
    #
    # s = create_squares('random', 1000, 1000, mirror_symmetric_3)
    # paint(s, black, white, 'mirror_symmetric_3_1000x1000.BMP')

    # The same as above, but with 5 above squares
    # def mirror_symmetric_5(array, n, h, x, *extras):
    #     a = array[h - 1][x - 2]
    #     b = array[h - 1][x - 1]
    #     d = array[h - 1][x + 1] if x + 1 < array[h - 1].size else array[h - 1][0]
    #     e = array[h - 1][x + 2] if x + 2 < array[h - 1].size else array[h - 1][1]
    #     return 1 if (a and b and d and e) or (not a and not b and not d and not e) or \
    #                 (a and not b and not d and e) or (not a and b and d and not e) else 0
    #
    #
    # s = create_squares('random', 1000, 1000, mirror_symmetric_5)
    # paint(s, black, white, 'mirror_symmetric_5_1000x1000.BMP')

    # Color the square if exactly one of the two above corner squares are colored
    # def one_corner(array, n, h, x, *extras):
    #     a = array[h - 1][x - 1]
    #     c = array[h - 1][x + 1] if x + 1 < array[h - 1].size else array[h - 1][0]
    #     return (a + c) % 2
    #
    #
    # s = create_squares('random', 1000, 1000, one_corner)
    # paint(s, black, white, 'one_corner_1000x1000.BMP')

    # Same as above, but with a first line of zeros and a single one
    # def one_corner(array, n, h, x, *extras):
    #     a = array[h - 1][x - 1]
    #     c = array[h - 1][x + 1] if x + 1 < array[h - 1].size else array[h - 1][0]
    #     return (a + c) % 2
    #
    #
    # cl = numpy.zeros(1000)
    # cl[500] = 1
    # s = create_squares('custom', 1000, 1000, one_corner, custom_first_line=cl)
    # paint(s, black, white, 'one_corner_1000x1000.BMP')

    # The Ulam numbers of the first 1000 numbers. This way of generating Ulam numbers is not particularly great.
    # ulam_num = ulam_numbers(1, 2, 900)
    # ul1 = create_squares('none', 100, 100, lambda array, n, h, x, *extras: 1 if n in extras[0] else 0, *ulam_num)
    # paint(ul1, [0, 0, 0], [255, 255, 255], 'ulam1_100x100.BMP')

    # The binary representation of the first 1000 Ulam numbers
    # ulam_num = ulam_numbers(1, 2, 1000)
    # s = create_squares('none', 15, 1000, lambda array, n, h, x, *extras: (extras[0][h] & (1 << x)) >> x, *ulam_num)
    # paint(s, black, white, 'ulam_binaries_15x1000.BMP')

    # Paint the square if the current square number is comprime withe the product of the row and column numbers.
    # We get some rather interesting squares
    # s = create_squares('none', 1000, 1000, lambda array, n, h, x, *extras: math.gcd(n, x*h) == 1)
    # paint(s, black, white, 'coprimes3_1000x1000.BMP')

    # Paint the square if the current row number, column number and square number are all coprime
    # s = create_squares('none', 1000, 1000,lambda array, n, h, x, *extras: math.gcd(n, x) == 1 and math.gcd(h, x) == 1 and math.gcd(n, h) == 1)
    # paint(s, black, white, 'coprimes2_1000x1000.BMP')

    # Paint the square if these two following are coprime: number of painted squares of
    # the above rows starting from each row's current column index and ending in it.
    # s = create_squares('ones', 1000, 1000,
    #                    lambda array, n, h, x, *extras: math.gcd(array[:h-1, x:].sum(), array[:h-1, :x].sum()) == 1)
    # paint(s, black, white, 'gcd_ones_1000x1000.BMP')

    # Simple Mandelbrot set. Very slow way.
    def mandelbrot_set(array, n, h, x, *extras):
        z = complex(-2.0 + 3.0 * x / 1500.0, -1.0 + 2.0 * h / 1000.0)
        return mandelbrot(z, max_iterations=10000)

    s = create_squares('none', 1500, 1000, mandelbrot_set)
    paint(s, black, white, 'mandelbrot_1500x1000.BMP')


if __name__ == '__main__':
    main()
