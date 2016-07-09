from PIL import Image, ImageChops


def autocrop(im, fuzz=0.5):
    """Get the border colour from the top left pixel, using getpixel.
    Subtracts a scalar from the differenced image, this is a quick way
    of saturating all values under 100, 100, 100 to zero to remove any fuzz
    resulting from compression.
    """
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, fuzz, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)


def check_min_size(im, min_size):
    width, height = im.size
    if width < min_size or height < min_size:
        return False
    return True
