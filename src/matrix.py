#!/usr/bin/env python3.6
import click
import numpy
from PIL import Image


@click.group()
def main():
    """
    Convert between matrices.txt and BMP file formats.
    """
    pass


@main.command('extract', help="Extract matrices.txt to individual image files.")
@click.argument('input', type=click.File('r'))
def extract(input):
    count, width, height, *values = map(int, input.read().split())
    assert max(values) <= 0xff and len(values) == count * (width * height)

    matrices = numpy.array_split(values, count)
    for number, matrix in enumerate(matrices, 1):
        matrix.shape = [width, height]  # Convert to 2D matrix
        matrix = numpy.flip(matrix, 0)  # FIXME: only for compatibility
        image = Image.fromarray(matrix.astype('uint8'), mode='L')  # 8 bit gray
        image.save(f"{number}.bmp")


@main.command('create', help="Create matrices.txt from individual image files.")
@click.option('--noise', is_flag=True, help="Add random noise to the matrices.")
@click.option('--output', required=True, type=click.File('w'))
@click.argument('input', nargs=-1, type=click.File('rb'))
def create(input, output, noise=False):
    noise_maximum = 150
    dimensions = list()
    matrices = list()

    for image in input:
        image = Image.open(image).convert(mode="L")
        dimensions += [image.size]

        if noise:
            random = numpy.random.randint(0, noise_maximum, size=image.shape)
            numpy.clip(image + random, 0, 0xff, out=image)

        image = numpy.flip(image, 0)  # FIXME: only for compatibility
        matrices += [image.flatten()]

    assert all([dimension == dimensions[0] for dimension in dimensions])
    width, height = dimensions[0]

    data = map(str, numpy.array(matrices).flatten())
    output.write(f"{len(matrices)} {width} {height} {' '.join(data)}\n")


if __name__ == '__main__':
    main()
