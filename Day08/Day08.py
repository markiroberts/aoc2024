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

# MultiProcessing Pool - on intel i9 runs with 32 processes.  Each process works on a single example.  Order of
#                        results not imporant.
# Dynamic Enumeration - using Enum functional API - this was probably a mistake, think simpler list would have been better

import pandas as pd
import csv 
import re
import enum
import math
from enum import Enum
from multiprocessing import Pool

DOPART01 = True
FOLDER = '.\\Day08\\'

#..........
#..........
#..........
#....a.....
#..........
#.....a....
#..........
#..........
#..........
#..........

class Antenna():
    count = 0
    signal = None
    x = y = None
    index = None

    def __init__(self, y: int, x:int, signal: str):
        self.signal = signal
        self.y = y
        self.x = x
        self.index = Antenna.count
        Antenna.count += 1

def dist(point1, point2):
    dx = abs(point2[0] - point1[0])
    dy = abs(point2[1] - point1[1])
    dist2 = (dx ** 2) + (dy ** 2)
    dist = math.sqrt(dist2)
    return(dist)

class Map():
    array = []
    antennaList = []
    antennaSignals = []
    signal_strength = dict()
    antinodes = dict()

    def __init__(self):
        self.array = []

    def append(self, row):
        self.array.append(row)

    def addAntinode(self, antinode):
        if antinode not in self.antinodes:
            self.antinodes[antinode] = antinode

    def addAntenna(self, antenna: Antenna):
        self.antennaList.append(antenna)
        if antenna.signal not in self.antennaSignals:
            self.antennaSignals.append(antenna.signal)

    def listAntennaBySignal(self, signal):
        list = [x for x in self.antennaList if x.signal == signal]
        for z in list:
            yield(z)

    def getSignalStrength(self, antenna: Antenna, y:int, x:int):
        strength = self.signal_strength[antenna.index][y][x]
        return(strength)


    def setSignalStrength(self, antenna: Antenna):
        signal_strength_array = []
        for row in range(len(self.array)):
            signal_strength_row = []
            for col in range(len(self.array[row])):
                dx = abs(col - antenna.x)
                dy = abs(row - antenna.y)
                dist = math.sqrt(dx**2 + dy**2)
                signal_strength_row.append(dist)
            signal_strength_array.append(signal_strength_row)
        self.signal_strength[antenna.index] = signal_strength_array


    def __str__(self):
        string = "Map\n"
        for row in self.array:
            row_string = ""
            for x in row:
                row_string = row_string + x
            row_string = f"{row_string}\n"
            string = string + row_string
        string = string + "\n"
        string = string + "Antenna\n"
        for x in self.antennaSignals:
            string = string + "Signal : " + x + "\n"
            for a in self.antennaList:
                if a.signal == x:
                    string = string + f"{a.index} y:{a.y} x:{a.x}\n"
        return(string)
    

def loadDay08(file):
    map = Map()
    with open(file,'r') as csvfile: 
        for line in csvfile:
            line = line.strip()
            row = [char for char in line]
            map.append(row)

    for y in range(len(map.array)):
        for x in range(len(map.array[y])):
            char = map.array[y][x]
            if ( char >= '0' and char <= '9' ) or ( char >= 'a' and char <= 'z' ) or ( char >= 'A' and char <= 'Z' ):
                antenna = Antenna(y, x, char)
                map.addAntenna(antenna)
                map.setSignalStrength(antenna)
    
    return(map)
            
if __name__ == '__main__':
    file01 = FOLDER + 'trial08stage01.csv'
    file01 = FOLDER + 'day08stage01.csv'
    if DOPART01:
        print("Doing Part 01")

    map = loadDay08(file01)
    print(map)

    for signals in map.antennaSignals:
        for ant1 in map.listAntennaBySignal(signals):
            for ant2 in map.listAntennaBySignal(signals):
                if ant1 != ant2:
                    dx = ant1.x - ant2.x
                    dy = ant1.y - ant2.y
                    pt1 = (ant1.y + dy, ant1.x + dx)
                    pt_ant1 = (ant1.y, ant1.x)
                    pt_ant2 = (ant2.y, ant2.x)
                    for mul in range(-50,50):
                        pt1 = (ant1.y + (dy*mul), ant1.x + (dx*mul))    
                        if pt1[0] >= 0 and pt1[0] < len(map.array) and pt1[1] >= 0 and pt1[1] < len(map.array[0]):
                            dist1 = dist(pt1, pt_ant1)
                            dist2 = dist(pt1, pt_ant2)
                            if (dist1 == (dist2 * 2)) or (dist2 == (dist1 * 2)):
                                map.addAntinode(pt1)
                        pt1 = (ant2.y + (dy*mul), ant2.x + (dx*mul))
                        if pt1[0] >= 0 and pt1[0] < len(map.array) and pt1[1] >= 0 and pt1[1] < len(map.array[0]):
                            dist1 = dist(pt1, pt_ant1)
                            dist2 = dist(pt1, pt_ant2)
                            if (dist1 == (dist2 * 2)) or (dist2 == (dist1 * 2)):
                                map.addAntinode(pt1)
    print("Part 1")
    print(f"Antinodes: {len(map.antinodes)}")

    print("Part 2")
    map.addAntinodes = dict()

    for signals in map.antennaSignals:
        for ant1 in map.listAntennaBySignal(signals):
            for ant2 in map.listAntennaBySignal(signals):
                if ant1 != ant2:
                    dx = ant1.x - ant2.x
                    dy = ant1.y - ant2.y
                    pt1 = (ant1.y + dy, ant1.x + dx)
                    pt_ant1 = (ant1.y, ant1.x)
                    pt_ant2 = (ant2.y, ant2.x)
                    for mul in range(-50,50):
                        pt1 = (ant1.y + (dy*mul), ant1.x + (dx*mul))
                        if pt1[0] >= 0 and pt1[0] < len(map.array) and pt1[1] >= 0 and pt1[1] < len(map.array[0]):
                            map.addAntinode(pt1)
                        pt1 = (ant2.y + (dy*mul), ant2.x + (dx*mul))
                        if pt1[0] >= 0 and pt1[0] < len(map.array) and pt1[1] >= 0 and pt1[1] < len(map.array[0]):
                            map.addAntinode(pt1)

    print(f"Antinodes: {len(map.antinodes)}")
                            

 