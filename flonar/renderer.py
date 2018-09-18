
class Page(object):
    def __init__(self, src_path, trgt_path, replaceDict):
        src = open(src_path, "r")
        trgt = open(trgt_path, "w")
        for line in src:
            for r, w in replaceDict.items():
                line = line.replace(r, str(w))
            trgt.write(line)
        src.close()
        trgt.close()

class Http(object):
    def __init__(self, src_path, replaceDict):
        src = open(src_path, "r")
        self.http = ''
        for line in src:
            for r, w in replaceDict.items():
                line = line.replace(r, str(w))
            self.http += line
        src.close()
        

