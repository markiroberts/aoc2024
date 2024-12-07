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


# uses sets and intersections
# essentially implements a bubble sort to reorder lists to valid sequences
# this may not be efficient but complex problem in less than 1 second

import pandas as pd
import csv 
import re

DOPART01 = True
DOPART02 = True
FOLDER = 'C:\\Users\\marki\\OneDrive\\Documents\\AI Apprentiship\\20241203 Advent of Code 2024\\aoc2024\\Day05\\'


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



if __name__ == '__main__':
    foundwords_part01 = None
    foundwords_part02 = None
    findstring01 = None
    findstring02 = None
    middlevaluetotal01 = 0
    middlevaluetotal02 = 0

    if DOPART01:
        file01 = FOLDER + 'trial05stage01.csv'
        file01 = FOLDER + 'day05stage01.csv'
        
        mustBeBefore, mustBeAfter, examples = loadDay05(file01)
        print("Must be Before ", mustBeBefore)
        print("Must be After  ", mustBeAfter)
        print("Examples  ", examples)

        middlevaluetotal01 = 0

        for example in examples:
#            print(f"Example: {example}")
            exampleok = True
            for index, x in enumerate(example):
                before = set(example[:index])
                after = set(example[index:])
                if x in mustBeBefore:
                    mustBeBeforeList = mustBeBefore[x]
                else:
                    mustBeBeforeList = []

                if x in mustBeAfter:
                    mustBeAfterList = mustBeAfter[x]
                else:
                    mustBeAfterList = []

                afterIssues     = after.intersection(mustBeBeforeList)
                beforeIssues    = before.intersection(mustBeAfterList)

                if afterIssues or beforeIssues:
#                    print(f"afterIssues {afterIssues}")
#                    print(f"beforeIssues {beforeIssues}")
                    exampleok = False

            if exampleok:
                length = len(example)
                middle = int((length - 1) / 2)
                middlevalue = example[middle]
                middlevaluetotal01 += middlevalue
                print(f"Example: {example} Length: {length} Middle: {middle} Middle Value: {middlevalue}  OK")
     
            else:
                print(f"Example: {example} failed")     

        print(f"Part 01 - Middle Value Total: {middlevaluetotal01}")       
                     
    if DOPART02:
        file01 = FOLDER + 'trial05stage01.csv'
        file01 = FOLDER + 'day05stage01.csv'

        invalidexamples = []
        
        mustBeBefore, mustBeAfter, examples = loadDay05(file01)
        print("Must be Before ", mustBeBefore)
        print("Must be After  ", mustBeAfter)
        print("Examples  ", examples)

        middlevaluetotal02 = 0

        for example in examples:
#            print(f"Example: {example}")
            exampleok = True
            for index, x in enumerate(example):
                before = set(example[:index])
                after = set(example[index:])
                if x in mustBeBefore:
                    mustBeBeforeList = mustBeBefore[x]
                else:
                    mustBeBeforeList = []

                if x in mustBeAfter:
                    mustBeAfterList = mustBeAfter[x]
                else:
                    mustBeAfterList = []

                afterIssues     = after.intersection(mustBeBeforeList)
                beforeIssues    = before.intersection(mustBeAfterList)

                if afterIssues or beforeIssues:
#                    print(f"afterIssues {afterIssues}")
#                    print(f"beforeIssues {beforeIssues}")
                    exampleok = False

            if exampleok:
                print(f"Example: {example} was ok, ignored for Part 02")     
            else:
                print(f"Example: {example} failed added to invalidexamples")     
                invalidexamples.append(example)
        print("")
        print("Go thru invalid examples")

        newexamples = invalidexamples
        okexamples = 0
        while okexamples < len(newexamples):
            print()
            okexamples = 0
            invalidexamples = newexamples
            newexamples = []
            for example in invalidexamples:
#                print(f"Example: {example}")
                exampleok = True
                for index, x in enumerate(example):
                    before = set(example[:index])
                    after = set(example[index+1:])
#                    print(f"Before: {before}")
#                    print(f"Value: {x}")                
#                    print(f"After: {after}")                
                    if x in mustBeBefore:
                        mustBeBeforeList = mustBeBefore[x]
                    else:
                        mustBeBeforeList = []

                    if x in mustBeAfter:
                        mustBeAfterList = mustBeAfter[x]
                    else:
                        mustBeAfterList = []

                    afterIssues     = after.intersection(mustBeBeforeList)
                    beforeIssues    = before.intersection(mustBeAfterList)

                    if afterIssues or beforeIssues:
#                        print(f"afterIssues {afterIssues}")
#                        print(f"beforeIssues {beforeIssues}")
                        exampleok = False
                        if afterIssues:
                            beforelist = example[:index] # before
                            afterlist  =  example[index+1:] #after
                            moveaftervalue = list(afterIssues)[0]
                            afterlist.remove(moveaftervalue)
                            newlistbefore = beforelist + [moveaftervalue] + [x] + afterlist
                            newexamples.append(newlistbefore)
                            break   

                if exampleok:
                    print(f"Example: {example} was ok")  
                    okexamples += 1 
                    newexamples.append(example)  
                else:
                    print(f"Example: {example} failed")              
     
        for example in newexamples:
#            print(f"Example: {example}")
            exampleok = True
            for index, x in enumerate(example):
                before = set(example[:index])
                after = set(example[index:])
                if x in mustBeBefore:
                    mustBeBeforeList = mustBeBefore[x]
                else:
                    mustBeBeforeList = []

                if x in mustBeAfter:
                    mustBeAfterList = mustBeAfter[x]
                else:
                    mustBeAfterList = []

                afterIssues     = after.intersection(mustBeBeforeList)
                beforeIssues    = before.intersection(mustBeAfterList)

                if afterIssues or beforeIssues:
#                    print(f"afterIssues {afterIssues}")
#                    print(f"beforeIssues {beforeIssues}")
                    exampleok = False

            if exampleok:
                length = len(example)
                middle = int((length - 1) / 2)
                middlevalue = example[middle]
                middlevaluetotal02 += middlevalue
                print(f"Example: {example} Length: {length} Middle: {middle} Middle Value: {middlevalue}  OK")
     
            else:
                print(f"Example: {example} failed")     

        print(f"Part 02 - Middle Value Total: {middlevaluetotal02}")  
        print(f"Part 01 - Middle Value Total: {middlevaluetotal01}")  