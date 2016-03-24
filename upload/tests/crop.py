from PIL import Image

def crop(left, top, width, height):
    img = Image.open('example.jpg')
    box = (left, top, left+width, top+height)
    img.crop(box).save('cropped.jpg')

if __name__ == '__main__':
    crop(432, 295, 265, 210)