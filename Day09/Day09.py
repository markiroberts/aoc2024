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

import pandas as pd
import csv 
import re
import enum
import math
import array
from enum import Enum
#from multiprocessing import Pool

import matplotlib.pyplot as plt
import numpy as np

DOPART01 = True
DOPART02 = True
FOLDER = '.\\Day09\\'

#['1', '2', '3', '4', '5']
#drive contents as simple array
#if lengths of 'files' increases in part 2 consider using array of tuples, (value, occurences)
#... might be smaller in size if some very long file sizes e.g. 123456 means 0 123 times then 456 blanks..
#Brute force approach worked.
#Visualised result of 'defragging' as a matplot lib graph if set graph=1 in defragging call
#used default values of parameters
#used defining __str__() function of a class to provide easy printing of values

class Drive():
    def __init__(self, size):
        self.size = size
        self.length = 0
        self.disk = [0] * size

    def append(self, data):
        self.disk[self.length] = data
        self.length += 1

    def __str__(self):
#        response = f"Disk\nLength: {self.length}\nCapacity: {len(self.disk)}\n"
        response = ""
        for x in range(self.length):
            value = self.disk[x]
            if value == None:
                value = '.'
            response = response + f"{value}"
        return(response)
    
    def draw(self):
        x_list = []
        y_list = []
        c_list = []
        for position in range(self.length):
            x = position % 400
            y = int(position / 400)
            if self.disk[position] != None:
                x_list.append(x)
                y_list.append(y)
                c_list.append(self.disk[position])
        xpos = np.array(x_list)
        ypos = np.array(y_list)
        c = np.array(c_list)
        return(xpos,ypos,c)
            

    def defragpart01(self):
        print("Defraging Part 01 - move individual blocks to free space")
        first = 0
        last = self.length - 1
        operations = 0

        while ( last > first ):
            operations = operations + 1

            while self.disk[first] != None and last > first:
                first += 1
        
            while self.disk[last] == None and last > first:
                last -= 1
            
            if (last>first):
                a = self.disk[first]
                b = self.disk[last]
                self.disk[first] = b
                self.disk[last] = a
        print()
        print(f"Complete in {operations} operations")


    def defragpart02(self,debug=False,graph=False):
        print("Defraging Part 02 - consider each files once in turn highest to lowest, move entire blocks to free space if possible")
        first = 0
        last = self.length - 1
        highestvalue = self.disk[last]
        currentvalue = highestvalue
        sourceend = last
        sourcestart = last
        targetstart = 0
        targetend = 0
        operations = 0

        while ( currentvalue > 0 ):
            operations = operations + 1
            if operations % 100 == 0 and graph:
                x,y,c = self.draw()
                plt.clf()
                plt.scatter(x, y, c=c, s=0.2)
                plt.xlim([0, 400])
                plt.ylim([0, 250])
                plt.pause(0.05)

            sourceend = last
            sourcestart = last

            while self.disk[sourceend] != currentvalue:
                sourceend -= 1

            x = sourceend
            sourcestart = sourceend

            while self.disk[x] == currentvalue:
                sourcestart = x
                x -= 1

            sourcelength = sourceend - sourcestart + 1

            targetstart = 0
            targetend = 0
            targetlength = 0
            boFoundSpace = False

 
            for x in range(sourcestart):
                if boFoundSpace == False:
                    if self.disk[x] == None:
                        targetstart = x
                        targetend = x
                        boFoundSpace = True
                else:
                    if self.disk[x] == None:    
                        targetend = x
                        targetlength =  targetend - targetstart + 1
                        if targetlength >= sourcelength:
                            break
                    else:
                        targetlength =  targetend - targetstart + 1
                        boFoundSpace = False
                        if targetlength >= sourcelength:
                            break
                
            if (targetlength >= sourcelength):
                if debug:
                    print(f"Found space: {currentvalue} Source Length: {sourcelength} Target Length : {targetlength} from: {sourcestart}-{sourceend} to {targetstart}-{targetend}")
                for z in range(sourcelength):
                    a = self.disk[sourcestart+z]
                    b = self.disk[targetstart+z]
                    if b != None:
                        print(f"Error overwriting non null {b} at {targetstart+z}")
                    self.disk[sourcestart+z] = b
                    self.disk[targetstart+z] = a
            else:
                if debug:
                    print(f"No space to move {currentvalue} Source Length: {sourcelength}")
            currentvalue -= 1

        print(f"Complete in {operations} operations")

    def checksum(self):
        print("Calculate checksum")
        checksum = 0
        for x in range(self.length):
            value = self.disk[x]
            if not value == None:
                checksum += x * value
        print(f"Checksum : {checksum}")

def loadDay09(file):
    with open(file,'r') as csvfile: 
        for line in csvfile:
            line = line.strip()
            map = [char for char in line]

    length = 10 * len(map)
    
    dataFile = True
    drive = Drive(length)
    dataValue = 0
 
    for index, count_str in enumerate(map):
        for x in range(int(count_str)):
            if dataFile:
                drive.append(data=dataValue)
            else:
                drive.append(data=None)
        if dataFile:
            dataFile = False
        else:
            dataFile = True   
            dataValue += 1    
    
    return(map, drive)
            
if __name__ == '__main__':
    file01 = FOLDER + 'trial09stage01.csv'
    file01 = FOLDER + 'day09stage01.csv'
    if DOPART01:
        print("Doing Part 01")
        map, drive = loadDay09(file01)
#       print(map)
#       print(drive)
        drive.defragpart01()
#       print(drive)
        drive.checksum()

    if DOPART02:
        print("Doing Part 02")
        map, drive = loadDay09(file01)
#       print(map)
#       print(drive)
        drive.defragpart02()
#       print(drive)
        drive.checksum()

 