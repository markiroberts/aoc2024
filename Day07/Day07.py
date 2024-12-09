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
from enum import Enum
from multiprocessing import Pool

DOPART01 = True
FOLDER = '.\\Day07\\'


if DOPART01:
    Operations = enum.Enum('Operations', {'Add': 0, 'Multiply': 1})
else:
    Operations = enum.Enum('Operations', {'Add': 0, 'Multiply': 1, 'Concatenate': 2})
    
#class Operations(Enum):
#    Add = 0
#    Multiply = 1
#    Concatenate = 2

class Example():
    answer: int = None
    values = [int]

    def __init__(self, answer:int, values):
        self.answer = answer
        self.values = values

class PossibleSolution():
    answer: int = None
    values = [int]
    operations = []
    result: int = None
    correct: bool = None

    def __str__(self):
        response = f"{self.values[0] }"
        for i in range(1, len(self.values)):
            response = response + f" {self.operations[i-1]} {self.values[i]} "
        response = response + f"= {self.result} == {self.answer} ? {self.correct} "
        return(response)



    def __init__(self, answer:int, values, operations):
        self.answer = answer
        self.values = values
        self.operations = operations

    def evaluate(self):
        self.result = self.values[0]
        for i in range(1, len(self.values)):
            value = self.values[i]
            operation = self.operations[i-1]
            if operation == Operations.Add.name:
                self.result = self.result + value
            elif operation == Operations.Multiply.name:
                self.result = self.result * value
            elif not DOPART01:
                if operation == Operations.Concatenate.name:
                    self.result = self.result 
                    value_string = f"{value}"
                    value_length = len(value_string)
                    value_power = 10 ** value_length
                    self.result = (self.result * value_power) + value
     #       elif operation == Operations.Divide.name:
     #           self.result = self.result / value
        if self.result == self.answer:
            self.correct = True
        else:
            self.correct = False

def findSolution(example):
    length = len(example.values)
    operators = length - 1
    combinations = len(Operations) ** operators
    for combination in range(combinations):
        operationList = []
        value = combination
        for operation in range(operators):
            operator = value % len(Operations)
            operatorSingleValue = [x.name for x in Operations if x.value == operator]
            operationList.extend(operatorSingleValue)
            value = int(value / len(Operations))
        possibleSolution = PossibleSolution(example.answer, example.values, operationList)
        possibleSolution.evaluate()
        if possibleSolution.correct:
            return(possibleSolution)
    return (possibleSolution)

def loadDay07(file):
    examples = []
    with open(file,'r') as csvfile: 
        for line in csvfile:
            line = line.strip()
            answer_str, values_str = line.split(": ")
            answer = int(answer_str)
            values_str = values_str.split(" ")
            values = [int(value_str) for value_str in values_str]
            example = Example(answer, values)
            examples.append(example)
    return(examples)
            
if __name__ == '__main__':
    file01 = FOLDER + 'trial07stage01.csv'
    file01 = FOLDER + 'day07stage01.csv'
    if DOPART01:
        print("Doing Part 01")
    else:
        print("Doing Part 02")

    examples = loadDay07(file01)
    for example in examples:
        print (f"{example.answer} = {example.values}")

    print("Evaluate")

    correctTotal = 0
    correctCount = 0

    with Pool() as pool:
        results = pool.map(findSolution, examples)

    for result in results:        
        if result.correct:
            print(result)
            correctTotal += result.answer
            correctCount += 1

    print(f"Correct count: {correctCount}  Correct total: {correctTotal}")