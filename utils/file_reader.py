import codecs

def read_list(path):
    try:
        return [line.strip() for line in codecs.open(path, encoding='utf-8', errors='ignore').readlines()]
    except:
        return False