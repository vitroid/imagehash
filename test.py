from imagehash import ImageHash
# from imagehashondisk import ImageHashOnDisk
import cv2
import json
import sys

def images_iter(q):
    for k in q:
        if isinstance(q[k], dict):
            yield from images_iter(q[k])
        else:
            yield k, q[k]


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
    q = ih.query_by_image(image, similarity=5)
    if q is not None:
        print(f"<h2>{name}</h2><p>")
        for path, tn in images_iter(q):
            print(f"<img src='file://{path}' width='100px' height='auto' />")
        print("</p>")

# めっちゃうまく動いている。
# 次はストレージへの保管。単純に、pythonのツリー構造をそのままディスク上に展開できるmoduleはないか?
# pickleのようなもので、disk上で動くもの。
