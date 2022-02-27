#
# 画像を白黒にし、コントラストを最強にし、2x2d2にする。
# その名前のディレクトリを掘り、そこに実体の場所を保存する。
# また、実体の場所だけのデータベースを別に作り、そちらにはハッシュ内の場所を保存する。
# 
# このprototypeでは、ディレクトリに実際に保存するのではなく、
# メモリー上ですべて処理する。

import cv2
import numpy as np

class ImageHash():
    def __init__(self, maxlevel=8):
        # file path to hash path
        self.directory = dict()
        # hash path to file path
        self.tree = dict()
        self.maxlevel = maxlevel
    def coarsegrain(self, image, level=1):
        assert 0 < level < self.maxlevel+1
        width = 2**level
        depth = width
        tn = cv2.resize(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), (width, width)).astype(int)
        vmin = np.min(tn)
        vmax = np.max(tn)
        return str(((tn-vmin) * depth // (vmax-vmin+1)).flatten())
    def query_by_image(self, image, similarity=8):
        if similarity > self.maxlevel:
            similarity = self.maxlevel
        level = 1
        branch = self.tree
        while True:
            tn = self.coarsegrain(image, level)
            if tn in branch:
                if level == similarity:
                    # multiple hit
                    return branch[tn]
                level += 1
                branch = branch[tn]
            else:
                return
    def register(self, image, uniquename):
        branch = self.tree
        for level in range(1,self.maxlevel+1):
            tn = self.coarsegrain(image, level)
            if tn not in branch:
                branch[tn] = dict()
            branch = branch[tn]
        # the leave
        # branch[uniquename] = image
        branch[uniquename] = cv2.resize(image, (100,100))
        # ここは、ツリー内でのデータ位置を保管してほしい。(上書きした時にはそれをたどって古いデータを消す。)
        self.directory[uniquename] = tn
    def query_by_name(self, name):
        if name in self.directory:
            return self.directory[name]
        return None

