"""
Graphics module contains some methods that can be used to make image editing easier.
"""
# Package Imports
from PIL import Image, ImageDraw


def transparency_paste(background_image, foreground_image, pos):
    """
    Pastes the foreground image onto the background image while maintaining the foreground image's transparency.

    Args:
        background_image (PIL.Image.Image) : The background image.
        foreground_image (PIL.Image.Image) : The foreground image.
        pos (int, int) : Where on the image to paste the foreground image.
    """
    # Create a new image with the same size as the background image.
    new_image = Image.new('RGBA', background_image.size)

    # Paste the foreground image onto the new image.
    new_image.paste(foreground_image, pos)

    # Alpha composite the new image onto the background image.
    background_image.alpha_composite(new_image)


def color_behind_image(base_image, color):
    """
    Colors behind an image.
    Will only color with alpha nonsense.

    Args:
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
