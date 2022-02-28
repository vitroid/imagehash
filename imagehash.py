#
# ツリー状のデータベースでは保存しにくいので、平坦なデータベースにする。
# 1つのthumbnailに対し複数のファイル、ひとつのファイルに対し複数のthumbnail
# 
# このprototypeでは、ディレクトリに実際に保存するのではなく # メモリー上ですべて処理する。

import cv2
import numpy as np
from collections import defaultdict

class ImageHash():
    def __init__(self, maxlevel=8):
        # file path to thumbnail hashes
        self.thumbs = dict()
        # thumbnail hash files
        self.locations = defaultdict(list)
        self.maxlevel = maxlevel
    def coarsegrain(self, image, level=1):
        assert 0 < level < self.maxlevel+1
        width = 2**level
        depth = width
        tn = cv2.resize(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), (width, width)).astype(int)
        vmin = np.min(tn)
        vmax = np.max(tn)
        return hash(tuple(((tn-vmin) * depth // (vmax-vmin+1)).flatten()))
    def query_by_image(self, image, similarity=8):
        if similarity > self.maxlevel:
            similarity = self.maxlevel
        tn = self.coarsegrain(image, similarity)
        return self.locations[tn]
    def register(self, image, path):
        thumbs = [0,]
        for level in range(1,self.maxlevel+1):
            tn = self.coarsegrain(image, level)
            if tn not in self.locations:
                self.locations[tn] = []
            self.locations[tn].append(path)
            thumbs.append(tn)
        self.thumbs[path] = thumbs
    def query_by_name(self, name):
        if name in self.thumbs:
            return self.thumbs[name]
        return None

