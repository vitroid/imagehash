#
# 画像を白黒にし、コントラストを最強にし、2x2d2にする。
# その名前のディレクトリを掘り、そこに実体の場所を保存する。
# また、実体の場所だけのデータベースを別に作り、そちらにはハッシュ内の場所を保存する。
#
# このprototypeでは、ディレクトリに実際に保存するのではなく、
# メモリー上ですべて処理する。

from sqlitedict import SqliteDict
from imagehash import ImageHash
from contextlib import contextmanager


class ImageHashOnDisk(ImageHash):
    def __init__(self, basename, flag='c', maxlevel=8):
        # hash path to file path
        self.locations = SqliteDict(basename + ".locs.sqlite", flag=flag)
        # file path to hash path
        self.thumbs = SqliteDict(basename + ".thumbs.sqlite", flag=flag)
        self.maxlevel = maxlevel


@contextmanager
def ihopen(name, flag='c', maxlevel=8):
    ih = ImageHashOnDisk(name, flag=flag, maxlevel=maxlevel)
    yield ih
    ih.thumbs.commit()
    ih.locations.commit()
