#This load flag into domain.
#Should probably be somewhere else.
import os

class FlagLoader(object):

    def CodeLoader(self):
        try:
            with open("country\A-Liste_UTF-16.txt", "r", encoding='utf-16') as codeList:
                self.code = [l.split() for l in codeList.readlines()]
            for x in range(0,196):
                self.code[x][1:len(self.code[x])] = [''.join(self.code[x][1:len(self.code[x])])]
            codeList.close()
        except FileNotFoundError:
            print(' File does NOT exist')

    def getCodeList(self):
        return self.code