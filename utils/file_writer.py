import codecs
import os

def write_file(path, filename, text):
    try:
        os.makedirs(path, exist_ok=True)
        with codecs.open(f'{path}/{filename}', 'a', encoding='utf-8', errors='ignore') as w:
            w.write(f'{text}\n')
        return True
    except:
        return False
    