import libs
import re

class Lex:
    def __init__(self, query:str):
        self.list = query.replace('(', ' ( ').replace(')', ' ) ').split()
        print(self.list)

if __name__ == '__main__':
    a = Lex('AA AND  (FFF )SK')