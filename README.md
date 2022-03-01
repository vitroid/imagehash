# imagehash
Image hash for fast similarity search


## Usage

### Make the index file

```shell
find . -name \*.png | store.py
```

For now, only bitmap images (that are accessible via PILLOW) can be specified.

### Query a similar image

```shell
query.py filename.png
query.py --level 6 filename.png
```

The similarity level is between 1 (lowest resolution (2x2), 1 bit in brightness level) and 8 (highest resolution (256x256), 8 bits in brightness level).



