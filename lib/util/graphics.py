"""
Graphics module contains some methods that can be used to make image editing easier.
"""
# Package Imports
from PIL import Image, ImageDraw, ImageOps, ImageFilter
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
        new_size = int(base_image.size[0] * factor + 0.5), int(base_image.size[1] * factor + 0.5)

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


def drop_shadow(base_image, angle=135, distance=5, blur_strength=10, alpha=255):
    """
    Drops a shadow behind the given image.

    Args:
        base_image (PIL.Image.Image) : The base image to rotate.
        angle (int) : The angle to drop the shadow, in degrees.
                      Defaults to 135 (down-right).
        distance (int) : The distance to drop the shadow.
                         Defaults to 5.
        blur_strength (int) : The strength of the drop shadow's blur.
        alpha (int) : The alpha value of the shadow.

    Returns:
        PIL.Image.Image : A new image.
    """
    # Make a shadow image using the size of the base image plus the distance plus the blur strength.
    shadow_image_size = (base_image.size[0] + distance + blur_strength ** 2,
                         base_image.size[1] + distance + blur_strength ** 2)
    shadow_image = Image.new('RGBA', shadow_image_size, (0, 0, 0, 0))
    shadow_image_form = Image.new('RGBA', base_image.size, (0, 0, 0, alpha))

    # Paste the shadow image form onto the shadow image using the base image as a mask.
    angle_radians = math.radians(angle)
    shadow_image.paste(shadow_image_form, (
        int((distance + blur_strength**2) / 2 + math.sin(angle_radians) * distance + 0.5),
        int((distance + blur_strength**2) / 2 - math.cos(angle_radians) * distance + 0.5)
    ), mask=base_image)

    # Blur it.
    shadow_image = shadow_image.filter(ImageFilter.GaussianBlur(blur_strength))

    # Paste the base image onto the shadow image.
    transparency_paste(shadow_image, base_image, (int(shadow_image_size[0] / 2), int(shadow_image_size[1] / 2)),
                       centered=True)

    # Return the final image.
    return shadow_image


def text_in_boundaries(base_image, font, text, x_boundaries, text_y, fill=(255, 255, 255), use_ellipsis=True):
    """
    Draws text within the given boundaries.
    Args:
        base_image (PIL.Image.Image) : The base image to rotate.
        font (PIL.ImageFont.ImageFont) : The font to write with.
        text (str) : The actual text to write.
        x_boundaries: (int, int) : The left then right boundaries of where to write.
        text_y (int) : The y position of the text.
        fill (int, int, int) : What color to write in.
        use_ellipsis (bool) : Whether to put an ellipsis at the end if the text was shortened.
    """
    # Get the width of the area we're writing in.
    text_max_width = x_boundaries[1] - x_boundaries[0]

    # Create a drawer for this image.
    text_writer = ImageDraw.Draw(base_image)

    # If the text already fits, then write and return.
    if font.getsize(text)[0] <= text_max_width:
        text_writer.text((x_boundaries[0], text_y), text, font=font, fill=fill)
        return

    # Otherwise, keep taking one letter off at a time until it fits.
    text = text[:-1]
    while text and font.getsize(text + '...' if use_ellipsis else text)[0] > text_max_width:
        text = text[:-1]

    # Now write.
    text_writer.text((x_boundaries[0], text_y), text + '...' if use_ellipsis else text, font=font, fill=fill)
