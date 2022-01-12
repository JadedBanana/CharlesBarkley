"""
Graphics module contains some methods that can be used to make image editing easier.
"""
# Package Imports
from PIL import Image, ImageDraw
import math


def transparency_paste(background_image, foreground_image, pos, centered=False):
    """
    Pastes the foreground image onto the background image while maintaining the foreground image's transparency.

    Args:
        background_image (PIL.Image.Image) : The background image.
        foreground_image (PIL.Image.Image) : The foreground image.
        pos (int, int) : Where on the image to paste the foreground image.
        centered (bool) : Whether to paste the foreground image's center at the pos instead of the top left corner.
    """
    # Create a new image with the same size as the background image.
    new_image = Image.new('RGBA', background_image.size)

    # Paste the foreground image onto the new image.
    new_image.paste(
        foreground_image,
        (int(pos[0] - foreground_image.size[0] / 2), int(pos[1] - foreground_image.size[1] / 2)) if centered else pos
    )

    # Alpha composite the new image onto the background image.
    background_image.alpha_composite(new_image)


def color_behind(base_image, color):
    """
    Colors behind an image.
    Will only color with alpha nonsense.

    Arguments:
        base_image (PIL.Image.Image) : The base image to color under.
        color (int, int, int) : The color to color with.

    Returns:
        PIL.Image.Image : A new image.
    """
    # Create a new image with the same size as the base image.
    new_image = Image.new('RGBA', base_image.size)

    # Create a drawer and draw a neat rectangle.
    drawer = ImageDraw.Draw(new_image)
    drawer.rectangle((-1, -1, base_image.size[0] + 1, base_image.size[1] + 1), color)

    # Paste with transparency.
    transparency_paste(new_image, base_image, (0, 0))

    # Return.
    return new_image


def resize(base_image, new_size=None, factor=None):
    """
    Resizes the given image to the given size.

    Arguments:
        base_image (PIL.Image.Image) : The base image to resize.
        new_size (int, int) : The new size (specific).
                              Must be supplied if factor is not.
        factor (float) : A factor to scale the original image to.
                         Must be supplied if new_size is not.

    Returns:
        PIL.Image.Image : A new image.
    """
    # If neither new_size nor factor were supplied, raise a ValueError.
    if not (new_size or factor):
        raise ValueError('Either new_size or factor need to be supplied')

    # If both new_size and factor were supplied, raise a ValueError.
    if new_size and factor:
        raise ValueError('Either new_size or factor need to be supplied, not both')

    # If we have a factor, perform some minor calculations.
    if factor:
        new_size = int(base_image.size[0] * factor), int(base_image.size[1] * factor)

    # Now return.
    return base_image.resize(
        new_size,
        Image.NEAREST if base_image.width < new_size[0] or base_image.height < new_size[1] else Image.LANCZOS
    )


def rotate(base_image, angle, resize_borders_to_fit=True):
    """
    Rotates the given image to the given angle.

    Args:
        base_image (PIL.Image.Image) : The base image to rotate.
        angle (float) : The angle to rotate the image (clockwise), in degrees.
        resize_borders_to_fit (bool) : Whether to resize the borders of the image to fit the new rotation.

    Returns:
        PIL.Image.Image : A new image.
    """
    # If we resize, remake the base_image.
    if resize_borders_to_fit:
        new_image_diagonals = math.hypot(base_image.size[0], base_image.size[1])
        new_image = Image.new('RGBA', (int(new_image_diagonals * 2), int(new_image_diagonals * 2)))
        transparency_paste(new_image, base_image, (new_image_diagonals, new_image_diagonals), centered=True)
        base_image = new_image

    # Return the rotated image.
    return base_image.rotate(-angle, center=(new_image_diagonals, new_image_diagonals), resample=Image.BILINEAR)