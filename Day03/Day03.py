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


import pandas as pd
import csv 
import re

DOPART01 = True 
DOPART02 = True
FOLDER = '.\\'

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


if __name__ == '__main__':
    file01 = FOLDER + 'trial.csv'
    file01 = FOLDER + 'day03stage01.csv'
    inputstring = ""
    with open(file01,'r') as csvfile: 
        for x in csvfile:
            inputstring += x

    if DOPART01:
        print("Part 01")
        print(f"Part 01: inputstring\n{inputstring}")
        total = compute_sum(inputstring)
        print(f"Part 01 Total: {total}")

    if DOPART02:
        print("Part 02")

        file02 = FOLDER + 'trial03pt02.csv'
#        file02 = FOLDER + 'day03stage01.csv'
        
        inputstring = ""
        with open(file02,'r') as csvfile: 
            for x in csvfile:
                inputstring += x
            
        print(f"Part 02: inputstring\n{inputstring}")

        finddont = "don\'t\(\)"
        finddo = "do\(\)"
        findmul = "mul\(\d+,\d+\)"
        print(finddont)

        match_donts = [(m.start(0), m.end(0)) for m in re.finditer(finddont, inputstring)]
        match_dos = [(m.start(0), m.end(0)) for m in re.finditer(finddo, inputstring)]

        match_donts_start = [(m[0]) for m in match_donts]
        match_donts_end = [(m[1]) for m in match_donts]
        match_dos_start = [(m[0]) for m in match_dos]
        match_dos_end = [(m[1]) for m in match_dos]

        print(match_donts, match_donts_start)
        print(match_dos)

        do = True
        dont = False
        newinput = ""

        for x in range(len(inputstring)):
            char = inputstring[x]
            if ( do and x in match_donts_start ):
                dont = True
                do = False
            
            if ( dont and x in match_dos_start ):
                do = True
                dont = False

            if dont:
                char = '.'

            newinput = newinput + char

        print(f"Removed don't - do\n{newinput}")
        total = compute_sum(newinput)

        print(f"Part 02 Total: {total}")
