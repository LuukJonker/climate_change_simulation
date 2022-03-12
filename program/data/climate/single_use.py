from PIL import Image, ImageDraw
import pickle
import sys

img = Image.open(r"img/climate_map.png")
px = img.load()
img.show()

width, height = img.size

print(width, " ", height)

num_coords = (360, 180)

climate_list = [[None] * num_coords[1]] * num_coords[0]

x_interval, y_interval = width / num_coords[0], height / num_coords[1]


def convert_rgba_to_rgb(rgba):
    alpha = int(rgba[3] / 255)

    return (
        int(rgba[0] * alpha),
        int(rgba[1] * alpha),
        int(rgba[2] * alpha)
    )


color_with_climate = {
    (255, 255, 255): 'Ocean',
    (25, 25, 25): 'border',
    (0, 0, 0): 'border',
    (0, 125, 125): 'dfc',
    (0, 120, 255): 'am',
    (102, 102, 102): 'ef',
    (178, 178, 178): 'et',
    (150, 50, 150): 'dsc',
    (161, 161, 161): 'et',
    (142, 142, 142): 'et',
    (193, 193, 193): 'ef',
}


for x in range(num_coords[0]):
    for y in range(num_coords[1]):
        climate = color_with_climate[convert_rgba_to_rgb(color := px[x * x_interval, y * y_interval])]
        climate_list[x][y] = climate if climate != 'border' else climate_list[x][y - 1] if y != 0 \
            else climate_list[x - 1][num_coords[1]]
        sys.stdout.write(f"\r({x}, {y}) is done, got color { color }")
        sys.stdout.flush()

with open("climate", "wb") as pickle_file:
    pickle.dump(climate_list, pickle_file)

with open("climate", "rb") as pickle_file:
    itemlist = pickle.load(pickle_file)

img = Image.new('RGB', (width, height), color='white')
px = img.load()
for x_index, x in enumerate(itemlist):
    for y_index, y in enumerate(x):
        img.putpixel((x_index, y_index), tuple(y))
        print((x_index, y_index), ' ', tuple(y) if tuple(y) != (255, 255, 255) else "")

img.show()

print(climate_list == itemlist)
print(itemlist)
