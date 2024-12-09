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

# uses sets and intersections
# essentially implements a bubble sort to reorder lists to valid sequences
# this may not be efficient but complex problem in less than 1 second

import pandas as pd
import csv 
import re
from enum import Enum

DOPART01 = True
DOPART02 = True
FOLDER = '.\\Day06\\'


def loadDay05(file):
    boLoadingPairs = True
    okbeforenumber = dict()
    okafternumber  = dict()
    examples = []
    with open(file,'r') as csvfile: 
        for line in csvfile:
            line = line.strip()
            if len(line) < 1: # reached the end of pairs  
                boLoadingPairs = False
                pass

            if boLoadingPairs:
                before,after = line.split("|")
                before = int(before)
                after = int(after)
                if after in okbeforenumber:
                    okbeforenumber[after].append(before)
                else:
                    okbeforenumber[after] = [before]
                if before in okafternumber:
                    okafternumber[before].append(after)
                else:
                    okafternumber[before] = [after]
            else:
                if len(line) > 1:
                    examplerow = []
                    for x in line.split(","):
                        examplerow.append(int(x))
                    examples.append(examplerow)

    return( okbeforenumber, okafternumber, examples )

class DirectionEnum(Enum):
    Up = 0
    Right = 1
    Down = 2
    Left = 3

class Direction(object):
    index = -1

    def GetDirection(self):
        return self.index


class Up(Direction):
    index = DirectionEnum.Up
    dx = 0
    dy = -1
    name = 'Up'
    char = '^'

class Right(Direction):
    index = DirectionEnum.Right
    dx = 1
    dy = 0
    name = 'Right'
    char = '>'

class Down(Direction):
    index = DirectionEnum.Down
    dx = 0
    dy = 1
    name = 'Down'
    char = 'v'

class Left(Direction):
    index = DirectionEnum.Left
    dx = -1
    dy = 0
    name = 'Left'
    char = '<'

DirectionList = [Up, Right, Down, Left]

class Guard():
    y = -1
    start_y = -1
    x = -1
    start_x = -1
    direction: DirectionEnum = None
    start_direction: DirectionEnum = None

    def __init__(self, rowindex: int, columnindex: int, direction: DirectionEnum):
        self.y = self.start_y = rowindex
        self.x = self.start_x = columnindex
        self.start_direction = self.direction = direction



def loadDay06(file):
    map = []
    with open(file,'r') as csvfile: 
        for line in csvfile:
            mapline = [char for char in line.strip()]
            map.append(mapline)
    maprowdict = dict()
    for rowindex, rowchars in enumerate(map):
        if '#' in rowchars:
            columns = [column for column, value in enumerate(rowchars) if value == '#']
            maprowdict[rowindex] = columns
        else:
            maprowdict[rowindex] = [] 
    
    mapcolumndict = dict()
    for columnindex in range (len(mapline)):
        columnchars = [rowchars[columnindex] for rowchars in map]
        if '#' in columnchars:
            rows = [row for row, value in enumerate(columnchars) if value == '#']
            mapcolumndict[columnindex] = rows
        else:
            mapcolumndict[columnindex] = [] 

    guardChars = Up.char + Right.char + Down.char + Left.char #'^>v<' #up right down left
    for rowindex, rowchars in enumerate(map):
        for columnindex, rowchar in enumerate(rowchars):
            if rowchar in guardChars:
                directionindex: DirectionEnum = guardChars.find(rowchar)
                guard = Guard(rowindex, columnindex, directionindex)

    return(map, maprowdict, mapcolumndict, guard)

if __name__ == '__main__':
    foundwords_part01 = None
    foundwords_part02 = None
    findstring01 = None
    findstring02 = None
    middlevaluetotal01 = 0
    middlevaluetotal02 = 0
    
    file01 = FOLDER + 'trial06stage01.csv'
    file01 = FOLDER + 'day06stage01.csv'

    if DOPART01:
        print("Part 01")
        directions = [Up(), Right(), Down(), Left()]        
        map, rowdict, columndict, guard = loadDay06(file01)
#        print(rowdict, columndict, guard)
#        print(directions[guard.direction])

        inLab = True
        endlessLoop = False
        steps = 1
        positions = set( )

        while(inLab and not endlessLoop):
            travelDirection: Direction = directions[guard.direction]
            position = (guard.y, guard.x)
            positions.add(position)
            if map[guard.y][guard.x] == '.':
                map[guard.y][guard.x] = travelDirection.char
            elif travelDirection.char not in map[guard.y][guard.x]:
                map[guard.y][guard.x] = map[guard.y][guard.x] + travelDirection.char
            elif steps > 1:
                endlessLoop = True
            
            dy = travelDirection.dy
            dx = travelDirection.dx

            next_x = guard.x + dx
            next_y = guard.y + dy

            if next_x >= 0 and next_x < len(columndict) and next_y >= 0 and next_y < len(rowdict):
                next_char = map[next_y][next_x]
                if next_char == '#':
                    guard.direction = ( guard.direction + 1 ) % 4
                else:
                    guard.x = next_x
                    guard.y = next_y
                    steps += 1
            else:
                inLab = False
#        for row in map:
#            for char in row:
#                charpad = char.ljust(4)
#               print(charpad, end ="")
#            print()
        print(f"Steps: {steps} Unique Cells: {len(positions)}")

    if DOPART02:
        print("Part 02")
        directions = [Up(), Right(), Down(), Left()]        
        initmap, initrowdict, initcolumndict, initguard = loadDay06(file01)
        endlesslooplist = []

        for blocky in range(len(initrowdict)):
            for blockx in range(len(initcolumndict)):
                map = [row[:] for row in initmap]
                
                columndict = initcolumndict
                rowdict = initrowdict

                guard = initguard
                guard.x = guard.start_x
                guard.y = guard.start_y
                guard.direction = guard.start_direction

                if blocky != guard.start_y or blockx != guard.start_x:
                    inLab = True
                    endlessLoop = False
                    steps = 1
                    positions = set( )
                    map[blocky][blockx] = 'O'

                    while(inLab and not endlessLoop):
                        travelDirection: Direction = directions[guard.direction]
                        position = (guard.y, guard.x)
                        positions.add(position)
                        
                        if map[guard.y][guard.x] == '.':
                            map[guard.y][guard.x] = travelDirection.char
                        elif travelDirection.char not in map[guard.y][guard.x]:
                            map[guard.y][guard.x] = map[guard.y][guard.x] + travelDirection.char
                        elif steps > 1:
                            endlessLoop = True
                        
                        dy = travelDirection.dy
                        dx = travelDirection.dx

                        next_x = guard.x + dx
                        next_y = guard.y + dy

                        if next_x >= 0 and next_x < len(columndict) and next_y >= 0 and next_y < len(rowdict):
                            next_char = map[next_y][next_x]
                            if next_char == '#' or next_char == 'O':
                                guard.direction = ( guard.direction + 1 ) % 4
                            else:
                                guard.x = next_x
                                guard.y = next_y
                                steps += 1
                        else:
                            inLab = False

                    if endlessLoop:
#                       print(f"Position y: {blocky} Position x: {blockx} Endless Loop")
                        pos = (blocky, blockx)
                        endlesslooplist.append(pos)
#                        for row in map:
#                            for char in row:
#                                charpad = char.ljust(4)
#                                print(charpad, end ="")
#                            print()

        print(f"Blockers: {len(endlesslooplist)}")
#       print(endlesslooplist)
#                    else:
#                        print(f"Position y: {blocky} Position x: {blockx} Steps: {steps} Unique Cells: {len(positions)}")