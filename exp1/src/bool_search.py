import json

'''
LL(1) grammar:
    E-> T OR E | T
    T-> F AND T | F
    F-> NOT F | (E) | word
using recursive descent
'''
class Searcher:
    def __init__(self):
        postinglist_path = '..\\output\\PostingList.json'
        wordmap_path = '..\\output\\wordmap.json'

        with open(wordmap_path,'r',encoding="utf-8")as fp_wordmap:
            self.WordMap = json.load(fp_wordmap)

        with open(postinglist_path,'r',encoding="utf-8")as fp_postinglist:
            self.PostingList = json.load(fp_postinglist)
            self.word_num = self.PostingList[0]

    def bool_search(self ,query:str):
        self.token = query.replace('(', ' ( ').replace(')', ' ) ').split()
        self.ptr = 0
        self.token.append('$')
        return self.E()[0]

    def E(self):
        T = self.T()
        if(T[1] == False):
            return([], False)
        elif(self.token[self.ptr]=='OR'):
            self.ptr += 1
            E = self.E()
            return (Searcher.OR(T[0], E[0]), True)
        else:
            return(T[0], True)

    def T(self):
        F = self.F()
        if(F[1] == False):
            return([], False)
        elif(self.token[self.ptr]=='AND'):
            self.ptr += 1
            T = self.T()
            return (Searcher.AND(F[0], T[0]), True)
        else:
            return (F[0], True)

    def F(self):    
        if(self.token[self.ptr]=='NOT'):
            self.ptr += 1
            F = self.F()
            return (self.NOT(F[0]), True)
        elif(self.token[self.ptr]=='('):
            self.ptr += 1
            E = self.E()
            self.ptr += 1
            return(E[0], True)
        else:
            list = self.GetList(self.token[self.ptr])
            self.ptr += 1
            return (list, True)

    def GetList(self, word):    
        word_id = self.WordMap[word]
        pre_list = self.PostingList[word_id]
        return [x[0] for x in pre_list]

    @staticmethod
    def AND(L1, L2):
        result = []
        p1 = 0
        p2 = 0
        len1 = len(L1) 
        len2 = len(L2)
        while True:
            if p1 == len1 or p2 == len2:
                break
            if L1[p1] == L2[p2]:
                result.append(L1[p1])
                p1 += 1
                p2 += 1
            elif L1[p1] < L2[p2]:
                p1 += 1
            else:
                p2 += 1
        return result

    @staticmethod
    def OR(L1: list, L2: list) -> list:
        result = []
        p1 = 0
        p2 = 0
        len1 = len(L1)
        len2 = len(L2)
        while True:
            if p1 == len1 and p2 == len2:
                break
            elif p1 < len1 and p2 == len2:
                result.append(L1[p1])
                p1 += 1
            elif p1 == len1 and p2 < len2:
                result.append(L2[p2])
                p2 += 1
            elif L1[p1] == L2[p2]:
                result.append(L1[p1])
                p1 += 1
                p2 += 1
            elif L1[p1] < L2[p2]:
                result.append(L1[p1])
                p1 += 1
            elif L1[p1] > L2[p2]:
                result.append(L2[p2])
                p2 += 1
        return result

    def NOT(self, L):
        all = list(range(1, self.word_num + 1))
        return [x for x in all if x not in L]

if __name__ == '__main__':
    a = Searcher()
    print(a.bool_search('(intern AND uup)AND NOT establish OR support' ))