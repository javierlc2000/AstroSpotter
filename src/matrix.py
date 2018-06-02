#!/usr/bin/env python3.6
import click
import numpy


@click.group()
def main():
    # TODO: make it compatible with BMP and PNG by using PIL or Pillow
    """
    Convert between matrices.txt and Netpbm ASCII PGM file formats.
    Replaces more than 344 lines of C++ code.
    """
    pass


@main.command('extract', help="Extract matrices.txt to individual image files.")
@click.argument('input', type=click.File('r'))
def extract(input):
    count, width, height, *values = map(int, input.read().split())
    matrices = numpy.array_split(values, count)

    assert len(values) == count * (width * height)
    assert max(values) <= 0xff  # 255

    for number, matrix in enumerate(matrices, 1):
        matrix.shape = [width, height]  # Convert to 2D matrix
        matrix = numpy.flip(matrix, 0)  # Mirror aling the X axis

        numpy.set_printoptions(threshold=numpy.nan, linewidth=numpy.nan)
        pixels = str(matrix).translate({ord(c):' ' for c in "[]"})

        with open(f"{number}.pgm", 'w') as output:
            output.write(f"P2\n{width} {height}\n255\n{pixels}")


@main.command('create', help="Create matrices.txt from individual image files.")
@click.option('--noise', is_flag=True, help="Add random noise to the matrices.")
@click.option('--output', required=True, type=click.File('w'))
@click.argument('input', nargs=-1, type=click.File('r'))
def create(input, output, noise=False):
    dimensions = list()
    matrices = list()

    for matrix in input:
        magic, *numbers = matrix.read().split()
        assert magic == "P2" # ASCII PGM

        width, height, maximum, *values = map(int, numbers)
        assert maximum == 0xff # 255

        matrix = numpy.array_split(values, width)
        matrix = numpy.flip(matrix, 0)
        matrix = matrix.flatten()

        if noise:
            random = numpy.random.randint(0, 150, size=matrix.shape)
            numpy.clip(matrix + random, 0, maximum, out=matrix)

        dimensions += [(width, height)]
        matrices += [matrix]

    assert all([dimension == dimensions[0] for dimension in dimensions])
    width, height = dimensions[0]

    data = ' '.join(map(str, numpy.array(matrices).flatten()))
    output.write(f"{len(matrices)} {width} {height} {data}\n")


if __name__ == '__main__':
    main()
