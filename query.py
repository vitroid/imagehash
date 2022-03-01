from imagehashondisk import ihopen
import PIL
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--level', metavar="LEVEL", type=int, default=8,
                    help='Similarity level (1=most abstract, 8=most detail')
parser.add_argument('file', metavar="FILE", type=str,
                    help='file to be looked up.')

args = parser.parse_args()

with ihopen("store", flag='r') as ih:
    image = PIL.Image.open(args.file)
    for path in ih.query(image, similarity=args.level):
        print(path)
