from PIL import Image, ImageFilter
from random import randint
from resizeimage import resizeimage


def color_pop(l, white, black):
    for i in range(len(l)):
        if l[i] == white:
            l[i] = (0, 0, 0)
        elif l[i] == black:
            l[i] = (255, 255, 255)
    return l


def get_lowest_index(colors):
    val = 255
    index = 0
    color = (0, 0, 0)
    for i in range(len(colors)):
        r, g, b = colors[i]
        grey = (r + g + b) // 3
        val = min(val, grey)
        if grey == val:
            index = i
            color = (r, g, b)
    return index, color


def get_highest_index(colors):
    val = 0
    index = 0
    color = (255, 255, 255)
    for i in range(len(colors)):
        r, g, b = colors[i]
        grey = (r + g + b) // 3
        val = max(val, grey)
        if grey == val:
            index = i
            color = (r, g, b)
    return index, color


def set_colors(colors):
    li, white = get_lowest_index(colors)
    colors[li] = (0, 0, 0)
    hi, black = get_highest_index(colors)
    colors[hi] = (255, 255, 255)
    return colors, white, black

def warhol_filter():
    image = Image.open('../app/static/app/images/santaclaus.jpeg').convert(
        'RGB')

    w, h = image.size
    s = min(w, h)
    box = ((w - s) / 2, 0, (w + s) / 2, s)
    image = image.crop(box=box).resize((s, s))
    image = image.quantize(6).convert('RGB')
    image = image.filter(ImageFilter.SMOOTH_MORE).filter(
        ImageFilter.SMOOTH_MORE).filter(
            ImageFilter.SMOOTH_MORE).quantize(6).convert('RGB')

    l = list(image.getdata())
    color_set, white, black = set_colors(list(set(l)))
    l = color_pop(l, white, black)
    px = len(l)

    new_pixels = [{str(rgb): rgb for rgb in color_set}]
    new_pixels.extend([{
        str(rgb): (randint(0, 50), randint(0, 50), randint(0, 50))
        if rgb == (0, 0, 0) else (randint(200, 255), randint(200, 255), randint(200, 255)) if rgb == (255, 255, 255) else (randint(0, 255), randint(0, 255), randint(0, 255))
        for rgb in color_set
    } for _ in range(3)])

    warhol_pixels = []

    for n in range(2):
        c = 0
        while (c < px):
            warhol_pixels.extend(
                list(
                    map(lambda p: new_pixels[2 * n + 0].get(p),
                        map(str, l[c:(c + s)]))))
            warhol_pixels.extend(
                list(
                    map(lambda p: new_pixels[2 * n + 1].get(p),
                        map(str, l[c:(c + s)]))))
            c += s

    image = Image.new('RGB', (2 * s, 2 * s))
    image.putdata(warhol_pixels)
    image = resizeimage.resize_cover(image, [800, 800], validate=False)

    image.save('../app/static/app/images/santawarhol.png')
    image.show()


def main():
    warhol_filter()

    
if __name__ == '__main__':
    main()
