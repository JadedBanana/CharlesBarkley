"""
Graphics module contains some methods that can be used to make image editing easier.
"""


def transparency_paste(background_image, foreground_image, pos):
    """
    Pastes the foreground image onto the background image while maintaining the foreground image's transparency.

    Args:
        background_image (PIL.Image.Image) : The background image.
        foreground_image (PIL.Image.Image) : The foreground image.
        pos (int, int) : Where on the image to paste the foreground image.

    Returns:
        PIL.Image.Image : The finalized image.
    """
    # Create a new image with the same size as the background image.
    new_image = Image.new('RGBA', background_image.size)

    # Paste the foreground image onto the new image.
    new_image.paste(foreground_image, pos)

    # Alpha composite the new image onto the background image.
    return Image.alpha_composite(background_image, new_image)