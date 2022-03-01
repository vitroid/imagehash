from imagehashondisk import ihopen

with ihopen("store", flag='r') as ih:
    print(len(ih.thumbs))
    for path, ths in ih.thumbs.items():
        print(path, ths)
    for tn, paths in ih.locations.items():
        print(tn, paths)
