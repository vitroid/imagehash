from imagehashondisk import ihopen
import sys
import cv2

with ihopen("store", flag='r') as ih:
    lines = sys.stdin.readlines()
    for line in lines:
        name = line.strip()
        image = cv2.imread(name)
        # 似た画像をツリー構造で返す。
        # maxlevelを大きくするほど、細かい差を区別する。
        print(f"<h2>{name}</h2><p>")
        for similarity in range(6, 3, -1):
            q = ih.query(image, similarity=similarity)
            if len(q) > 1:
                print(f"<h3>Similarity {similarity}</h3><p>")
                for path in q:
                    if path != name:
                        print(
                            f"{path}<br /><img src='file://{path}' width-max='100px' height='100px' /><br />")
        print("</p>")
