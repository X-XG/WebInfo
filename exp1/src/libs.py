import json

class wordIndex():
    __fp = open('../output/PostingList.json')
    __dict = json.load(__fp)

    def __init__(self,word):
        self.count = 1
        # 找到关于词项文档索引列表\
        if word in wordIndex.__dict:
            self.list = wordIndex.__dict[word]
        else:
            self.list = []
        self.length = len(self.list)

    def current_id(self):
        if self.count > self.length:
            return -1
        else:
            return self.list.index(self.count)[0]

    def next(self):
        self.count += 1

class Doc:
    __fp = open('../output/DocMap.json')
    __list = list(json.load(__fp))

    def __init__(self, id):
        self.doc_path = Doc.__list[id]

    def print_path(self):
        print(self.doc_path)

    def print_doc(self):
        with open('../dataset/US_Financial_News_Articles/' + self.doc_path) as self.fp:
            print(self.fp.read())

class MergeList():
    def __init__(self, word1, word2):
        self.L1 = wordIndex(word1)
        self.L2 = wordIndex(word2)
        self.list = []

    def AND(self) -> list:
        while True:
            id1 = self.L1.current_id()
            id2 = self.L2.current_id()
            if id1 < 0 or id2 < 0:
                break
            if id1 == id2:
                self.list.append(id1)
                self.L1.next()
                self.L2.next()
            elif id1 < id2:
                self.L1.next()
            else:
                self.L2.next()
        return self.list

    def OR(self):
        while True:
            id1 = self.L1.current_id()
            id2 = self.L2.current_id()
            if id1 < 0 or id2 < 0:
                break
            if id1 == id2:
                self.list.append(id1)
                self.L1.next()
                self.L2.next()
            elif id1 < id2:
                self.list.append(id1)
                self.L1.next()
            else:
                self.list.append(id2)
                self.L2.next()
        return self.list
        
if __name__ == '__main__':
    a = Doc(1)

    a.print_doc()
    a.print_path()