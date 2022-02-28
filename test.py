from imagehash import ImageHash
# from imagehashondisk import ImageHashOnDisk
import cv2
import json
import sys



# ih = ImageHashOnDisk("test", maxlevel=8)
ih = ImageHash(maxlevel=8)
images = sys.stdin.readlines()
for line in images:
    name = line.strip()
    image = cv2.imread(name)
    ih.register(image, name)

for line in images:
    name = line.strip()
    image = cv2.imread(name)
    # 似た画像をツリー構造で返す。
    # maxlevelを大きくするほど、細かい差を区別する。
    print(f"<h2>{name}</h2><p>")
    for similarity in range(6,2,-1):
        print(f"<h3>Similarity {similarity}</h3><p>")
        q = ih.query_by_image(image, similarity=similarity)
        if q is not None:
            for path in q:
                print(f"<img src='file://{path}' width='100px' height='auto' />")
    print("</p>")

