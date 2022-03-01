from imagehashondisk import ihopen
# from imagehash import open
import sys
import PIL


with ihopen("store") as ih:
    # with open() as ih:
    lines = sys.stdin.readlines()
    for line in lines:
        name = line.strip()
        print(name)
        try:
            image = PIL.Image.open(name)
            ih.register(image, name)
        except PIL.UnidentifiedImageError:
            print(f"{name}: UnidentifiedImageError")
    print(len(ih.thumbs))
