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

#_ga=GA1.2.1374795190.1701415040; 
# _gid=GA1.2.314749366.1733226540; 
# session=53616c7465645f5f22bc9f1fd4184fd1828df55fed38976e974abd7fa28d75d148f435b0b729052932f8355846cfff71f78ab51579fb3eab4db1fa81437d9615; _gat=1; _ga_MHSNPJKWC7=GS1.2.1733226540.19.1.1733228141.0.0.0


# uses multiple returned values from a function with definition -> tuple[type, type]
# uses if __name__ == '__main__':

import pandas as pd
import csv 

DOPARTONE = False

def checkSafety(row) -> tuple[bool, str]:
    previous = row[0]
    safe = True
    rejection_reason = []
    ascending = False
    descending = False

    for x in range(1,len(row)):
        current = row[x]
        if ( current > previous):
            if descending:
                safe = False
                rejection_reason.append("Ascending and Descending")
                break
            ascending = True

        if ( current < previous):
            if ascending:
                safe = False
                rejection_reason.append("Ascending and Descending")
                break
            descending = True

        delta = abs(current - previous)
        if delta == 0:
            safe = False
            rejection_reason.append("No change")
            break

        if delta > 3:
            safe = False
            rejection_reason.append("Change over 3")
            break

        previous = current
    return(safe, rejection_reason)

if __name__ == '__main__':
#    file = 'C:\\Users\\marki\\OneDrive\\Documents\\AI Apprentiship\\20241203 Advent of Code 2024\\aoc2024\\Day02\\trial.csv'
    file = 'C:\\Users\\marki\\OneDrive\\Documents\\AI Apprentiship\\20241203 Advent of Code 2024\\aoc2024\\Day02\\day02stage01.csv'
    inputdata = []
    with open(file,'r') as csvfile: 
        reader = csv.reader( csvfile,delimiter=' ') # change contents to floats
        for row in reader: # each row is a list
            lst = [int(d) for d in row]
            inputdata.append(lst)

    safecount = 0
    if DOPARTONE:
        for row in inputdata:
            safe, rejection_reason = checkSafety(row)

            print(row, safe, rejection_reason)
            if safe:
                safecount += 1

        print(f"Part 1 Safecount: {safecount}")


    safecount = 0

    for row in inputdata:
        safe, rejection_reason = checkSafety(row)

        print(row, safe, rejection_reason)
        if safe:
            safecount += 1
        else:
# create a second list when first try is unsafe where one of the elements is skipped
# check if this list is safe.  If it is then count the row as safe and 'break' to
# move on to the next row
            for skip in range(len(row)):
                rowmissone = row[:skip] + row[skip+1:]
                safe, rejection_reason = checkSafety(rowmissone)
                if safe:
                    safecount += 1
#                    print(row, safe, rejection_reason)
                    print(f"Skip {skip} {rowmissone} Safe")
                    break

    print(f"Part 2 Safecount: {safecount}")
