import libs
import re

class Lex:
    def __init__(self, query:str):
        self.list = query.replace('(', ' ( ').replace(')', ' ) ').split()
        self.ptr = 0
        print(self.list)

    def GetIdList(self) -> list:
        if(self.list[self.ptr] == '('):
            self.ptr += 1
            self.GetIdList()
        elif(self.list[self.ptr] ==')'):
            return
        else:
            L1 = GETLIST(self.list[self.ptr])
            self.ptr += 1
            if(self.list[self.ptr] == 'AND'):
                self.ptr += 1
                L2 = self.GetIdList()
                return Lex.AND(L1, L2)

    def AND(L1:list, L2:list) -> list:


if __name__ == '__main__':
    a = Lex('AA AND  (FFF )SK')