#
# ツリー状のデータベースでは保存しにくいので、平坦なデータベースにする。
# 1つのthumbnailに対し複数のファイル、ひとつのファイルに対し複数のthumbnail
#
# このprototypeでは、ディレクトリに実際に保存するのではなく # メモリー上ですべて処理する。

import cv2
import numpy as np
from collections import defaultdict
import sys

class ImageHash():
    def __init__(self, maxlevel=8):
        # file path to thumbnail hashes
        self.thumbs = dict()
        # thumbnail hash files
        self.locations = defaultdict(set)
        self.maxlevel = maxlevel

    def coarsegrain(self, image, level=1):
        assert 0 < level < self.maxlevel + 1
        assert image is not None
        width = 2**level
        depth = width
        tn = cv2.resize(
            cv2.cvtColor(
                image,
                cv2.COLOR_BGR2GRAY),
            (width,
            width)).astype(int)
        vmin = np.min(tn)
        vmax = np.max(tn)
        if vmin == vmax or tn is None:
            return hash(tuple(np.zeros_like(tn).flatten()))
        return hash(tuple(((tn - vmin) * depth // (vmax - vmin + 1)).flatten()))

    def query(self, image, similarity=8):
        if image is None:
            return []
        if similarity > self.maxlevel:
            similarity = self.maxlevel
        tn = self.coarsegrain(image, similarity)
        return self.locations[tn]

    def delete(self, path):
        if path not in self.thumbs:
            return
        for tn in self.thumbs[path]:
            self.locations[tn].remove(path)
        del self.thumbs[path]

    def register(self, image, path, overwrite=True):
        if image is None:
            return
        if path in self.thumbs:
            assert not overwrite
            self.delete(path)
        thumbs = [0, ]
        for level in range(1, self.maxlevel + 1):
            tn = self.coarsegrain(image, level)
            self.locations[tn].add(path)
            thumbs.append(tn)
        self.thumbs[path] = thumbs
