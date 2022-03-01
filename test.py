from imagehashondisk import open
# from imagehash import open
import cv2
import sys


with open("test") as ih:
    # with open() as ih:
    lines = sys.stdin.readlines()
    for line in lines:
        name = line.strip()
        print(name)
        image = cv2.imread(name)
        ih.register(image, name)
    print(len(ih.thumbs))
