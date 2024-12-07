# create virtual environment .venv
# python -m venv .venv

# upgrade pip if necessary
# python -m pip install --upgrade pip

# activate virtual environment .venv
# .\.venv\Scripts\activate

# install required libraries
# pip install -r .\requirements.txt
# requirements.txt contains:
# numpy
# tensorflow
# keras==2.12
# matplotlib
# get errors without deprecating keras

# uninstall libraries if needed to start again..
# pip freeze > current.txt
# pip uninstall -r .\current.txt -y

# xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))
# xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))


# uses generator giving active entries in an array... could do with remove and listing all

import pandas as pd
import csv 
import re

DOPART01 = True 
DOPART02 = True
FOLDER = 'C:\\Users\\marki\\OneDrive\\Documents\\AI Apprentiship\\20241203 Advent of Code 2024\\aoc2024\\Day04\\'

def compute_sum(string) -> int:
    findstr = "mul\(\d+,\d+\)"

    muls = re.findall(findstr, string)

    finda = "\d+"
    total = 0
    for x in muls:
        a,b = re.findall(finda, x)
        a = int(a)
        b = int(b)
        print(x, a ,b)
        z = a * b
        total += z
    return(total)

class XmasWord():
 
    wordCount = 0
    def __init__(self, start_x: int, start_y: int, d_x: int, d_y: int, length: int, char: str):
        self.start_x = start_x
        self.start_y = start_y
        self.d_x = d_x
        self.d_y = d_y
        self.length = length
        self.active = True
        self.word = char
        self.index = self.wordCount
        XmasWord.wordCount += 1

    def __str__(self):
        return (f'{self.__class__.__name__}(word: {self.word} start y,x: {self.start_y, self.start_x} direction y,x: {self.d_y, self.d_x} length: {self.length} index:{self.index} active: {self.active}')

def active_indexes(thewords):
    for wx in thewords:
        if wx.active:
            yield wx.index

def loadgrid(file):
    grid = []
    inputstring = ""
    with open(file01,'r') as csvfile: 
        y = 0
        for line in csvfile:
            row = []
            x = 0
            for char in line:
                if char > ' ':
                    row.append(char)
                    x += 1
            grid.append(row)
            y += 1    
    print(f"Loaded : x: {x} y : {y} grid")
    return(y, x, grid)


if __name__ == '__main__':
    foundwords_part01 = None
    foundwords_part02 = None
    findstring01 = None
    findstring02 = None

    if DOPART01:
        words = []
        XmasWord.wordCount = 0
        file01 = FOLDER + 'trial.csv'
        file01 = FOLDER + 'day04stage01.csv'
        rows, columns, chargrid = loadgrid(file01)
        findstring01 = "XMAS"
        for y in range(rows):
            for x in range (columns):
                if chargrid[y][x] == findstring01[0]:
                    words.append(XmasWord(x,y,  -1, -1,  1,findstring01[0]))
                    words.append(XmasWord(x,y,  0,  -1,  1,findstring01[0]))
                    words.append(XmasWord(x,y,  1,  -1,  1,findstring01[0]))

                    words.append(XmasWord(x,y,  -1,  0,  1,findstring01[0]))
                    words.append(XmasWord(x,y,  1,   0,  1,findstring01[0]))
                 
                    words.append(XmasWord(x,y,  -1,  1,  1,findstring01[0]))
                    words.append(XmasWord(x,y,  0,   1,  1,findstring01[0]))
                    words.append(XmasWord(x,y,  1,   1,  1,findstring01[0]))

 
        for l in range(1, 4):
            for i in active_indexes(words):
                w = words[i]
                next_x = w.start_x + ( w.d_x * l )
                next_y = w.start_y + ( w.d_y * l )

                check_for_char = findstring01[w.length]
                if next_x < columns and next_x >= 0 and next_y < rows and next_y >= 0:
                    if check_for_char == chargrid[next_y][next_x]:
                        w.length += 1
                        w.word = w.word + check_for_char
                    else:
                        print(f"Mismatch char. Index: {i} {next_y}, {next_x}, {check_for_char}, {chargrid[next_y][next_x]}")
                        w.active = False
                else:
                    print(f"Out of bound next char. Index: {i} {next_y}, {next_x}, {check_for_char} ")                    
                    w.active = False
            print(f"Loop : {l}")
 
            foundwords = 0
        
        foundwords_part01 = 0
        for w in active_indexes(words):
            foundwords_part01 += 1
        print(f"Part01 Found {findstring01} {foundwords_part01} times")

    if DOPART02:
        words = []
        XmasWord.wordCount = 0        
        file01 = FOLDER + 'trial04pt02.csv'
        file01 = FOLDER + 'day04stage01.csv'        
        rows, columns, chargrid = loadgrid(file01)
        findstring02 = "MAS"
        for y in range (rows):
            for x in range (columns):
                if chargrid[y][x] == findstring02[1]: #A
                    words.append(XmasWord(x,y,  1,   1,  0,findstring02[1]))
                    words.append(XmasWord(x,y,  1,  -1,  0,findstring02[1]))
                    words.append(XmasWord(x,y,  -1,   1,  0,findstring02[1]))
                    words.append(XmasWord(x,y,  -1,  -1,  0,findstring02[1]))
 
        for i in active_indexes(words):
            print(f"Index: {i} of {len(words)} words")
            w = words[i]
            next_x1 = w.start_x + ( w.d_x   )
            next_y1 = w.start_y + ( w.d_y   )
            next_x2 = w.start_x - ( w.d_x   )
            next_y2 = w.start_y - ( w.d_y   )
            print(w)
            print(f"y1:{next_y1}, x1:{next_x1}")            
            print(f"y2:{next_y2}, x2:{next_x2}")
            check_for_char1 = findstring02[0] #M
            check_for_char2 = findstring02[2] #S            
            if next_x1 < columns and next_x1 >= 0 and next_y1 < rows and next_y1 >= 0:
                if next_x2 < columns and next_x2 >= 0 and next_y2 < rows and next_y2 >= 0:                    
                    if check_for_char1 == chargrid[next_y1][next_x1]:
                        if check_for_char2 == chargrid[next_y2][next_x2]:
                            w.length += 2
                            w.word = check_for_char1 + w.word + check_for_char2
                        else:
                            print(f"Mismatch char. Index: {i} y:{next_y2}, x:{next_x2}, check for char:{check_for_char2}, found char:{chargrid[next_y2][next_x2]}")
                            w.active = False                            
                    else:
                        print(f"Mismatch char. Index: {i} y:{next_y1}, x:{next_x1}, check for char:{check_for_char1}, found char:{chargrid[next_y1][next_x1]}")
                        w.active = False
                else:
                    print(f"Out of bound next char. Index: {i} y:{next_y2}, x:{next_x2}, {check_for_char2} ")        
                    w.active = False            
            else:
                print(f"Out of bound next char. Index: {i} y:{next_y1}, x:{next_x1}, {check_for_char1} ")  
                w.active = False
        
        foundwords_part02 = 0
        for w1 in active_indexes(words):
            for w2 in active_indexes(words[w1:]):
                if (w1 != w2 and words[w1].start_x == words[w2].start_x and words[w1].start_y == words[w2].start_y ):
                    foundwords_part02 += 1
                    print(words[w1])
        print(f"Part02 : Found {findstring02} {foundwords_part02} times")
        print(f"Part01 : Found {findstring01} {foundwords_part01} times")        
                
                