from imagehashondisk import open
# from imagehash import open
import sys
import PIL


with open("store") as ih:
    # with open() as ih:
    lines = sys.stdin.readlines()
    for line in lines:
        name = line.strip()
        print(name)
        image = PIL.Image.open(name)
        ih.register(image, name)
    print(len(ih.thumbs))
