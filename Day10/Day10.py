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
from matplotlib import cm
import numpy as np

DOPART01 = True
DOPART02 = True
FOLDER = '.\\Day10\\'

#...0...
#...1...
#...2...
#6543456
#7.....7
#8.....8
#9.....9
#
# 1. can only move NSEW (not diagonal)
# 2. each step height increases by 1
# 3. branching at most 3 for each square
# 4. trail heads (start positions) all have height 0
# 5. the value of a trail head is number of height 9 squares which
#    can be reached
# 6. multiple goals.. so want to explore whole map
#    not just find the fastest route to any 9
#
# Thoughts:
# be nice to visualise in 3d?
# 

class Map():

    def __init__(self):
        self.sizex = self.sizey = self.size = 0
        self.height = []
        self.trailHeads = []
        self.goalroute = {}

    def __str__(self):
#        response = f"Disk\nLength: {self.length}\nCapacity: {len(self.disk)}\n"
        response = ""
        for y in range(self.sizey):
            for x in range(self.sizex):
                value = self.height[y][x]
                response = response + f"{value}"
            response = response + "\n"
        return(response)
    
    def listOfNaN(self, Z):
        result = []
        for index, x in enumerate(Z):
            if not x.is_integer():
                result.append(index)
        return result
    
    def findTrailHeads(self):
        for y in range(self.sizey):
            for x in range(self.sizex):
                z = self.height[y][x]
                if z == 0:
                    pos = (x,y)
                    self.trailHeads.append(pos)
        for x in self.trailHeads:
            print (x)

    def scoreTrailHeads01(self):
        headGoalPairs = {}
        for x in self.trailHeads:
            goals = []
            for r in self.goalroute:
                if self.goalroute[r][0] == x:
                    goal = self.goalroute[r][-1]
                    if goal not in goals:
                        goals.append(goal)
            headGoalPairs[x] = goals
        score = 0
        for h in self.trailHeads:
            headScore = len(headGoalPairs[h])
            print (f"Head: {h}  Destinations : {headScore}")
            score += headScore
        print (f"Total Score Part 01 : {score}")

    def scoreTrailHeads02(self):
        score = 0
        for x in self.trailHeads:
            headScore = 0
            for r in self.goalroute:
                if self.goalroute[r][0] == x:
                    headScore += 1
            print (f"Head: {x}  Routes : {headScore}")
            score += headScore
        print (f"Total Score Part 02 : {score}")
        

    def getneighbours(self, x: int, y:int ):
        if x > 0:
            yield x-1,y
        if x < ( self.sizex - 1 ):
            yield x+1,y
        if y > 0:
            yield x,y-1
        if y < ( self.sizey - 1 ):
            yield x,y+1


    def findGoalRoutes(self):
        goalroute = {}
        for index, h in enumerate(self.trailHeads):
            route = {}
            routes = len(route)
            route[routes] = [h]

            boFoundBranchCurrentRoute = True
            boFoundBranchAnyRoute = True

            while(boFoundBranchAnyRoute):
                nextroutes = {}
                boFoundBranchAnyRoute = False

                for current_route_index in route:
                    current_route = route[current_route_index]
                    position = current_route[-1]  # end of the route
                    x = position[0]
                    y = position[1]
                    branches = []
                    z = int(self.height[y][x])
                    findz = z + 1
                    boFoundBranchCurrentRoute = True

#                    while(boFoundBranchCurrentRoute):
#                        boFoundBranchCurrentRoute = False

                    for b in self.getneighbours(x,y):
                        xb = b[0]
                        yb = b[1]
                        zb = int(self.height[yb][xb])
                        print(xb, yb, zb)
                        if ( zb == findz ):
                            branches.append(b)

                    if len(branches) > 0:  # if found a next step
                        boFoundBranchCurrentRoute = True
                        boFoundBranchAnyRoute = True
                        for b in branches:
                            newroute = current_route.copy()
                            newroute.append(b)
                            newroutes = len(nextroutes)
                            nextroutes[newroutes] = newroute
                            xb = b[0]
                            yb = b[1]
                            zb = int(self.height[yb][xb])
                            if zb == 9:
                                goalroutes = len(self.goalroute)
                                self.goalroute[goalroutes] = newroute
                
                route = nextroutes
        print(f"Found: {len(self.goalroute)} goal routes")







    def draw(self):
        x_list = []
        y_list = []
        c_list = []

        plt.style.use('_mpl-gallery')

        # Make data
        X = np.arange(0, self.sizex, 1)
        Y = np.arange(0, self.sizey, 1)

        X, Y = np.meshgrid(X, Y, indexing="xy")
        Z = -1 * np.empty(X.shape)
        for index, (x, y) in enumerate(zip(X.flatten(), Y.flatten())):
            z = self.height[y][x]
            if z != '.':
                Z[y][x] = int(z)
            else:
                Z[y][x] = -1

     #   index = [i for i in X X[i] == np.nan]
        # Plot the surface
        fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

        for goal in self.goalroute:
            route = self.goalroute[goal]

    #    route1 = [(0,3),(1,3),(2,3),(3,3),(3,2),(3,1),(3,0),(4,0),(5,0),(6,0)]
            xx = np.empty(len(route),)
            yy = np.empty(len(route),)
            zz = np.empty(len(route),)
            for i, (x,y) in enumerate(route):
                xx[i] = x
                yy[i] = y
                zz[i] = self.height[y][x]

            ax.plot(xx, yy, zz, c='r', marker='o')
        
        ax.plot_surface(X, Y, Z, vmin=Z.min() * 2, cmap=cm.coolwarm)
        ax.set_zlim(0,20)

        ax.set(xticklabels=[],
            yticklabels=[],
            zticklabels=[])
        
        for trailHead in self.trailHeads:
            head = trailHead
            xx = [head[0], head[0]]
            yy = [head[1], head[1]]
            zz = [0,1]
            ax.plot(xx, yy, zz, c='g', marker='o', scalex=True, scaley=True, linewidth=4)
#        plt.clf()
#        plt.scatter(x, y, c=c, s=0.2)
#        plt.xlim([0, 400])
#        plt.ylim([0, 250])
#        plt.pause(0.05)
        plt.show()

    def loadDay10(self, file):
        self.sizex = 0
        self.sizey = 0

        with open(file,'r') as csvfile: 
            for line in csvfile:
                line = line.strip()
                row_sizex = len(line)
                if row_sizex > self.sizex:
                    self.sizex = row_sizex
                row = [char for char in line]
                for index, h in enumerate(row):
                    if h == '.':
                        row[index] = -1
                    else:
                        row[index] = int(h)
                self.height.append(row)
                self.sizey += 1
            
if __name__ == '__main__':
    file01 = FOLDER + 'trial10stage01.csv'
    file01 = FOLDER + 'day10stage01.csv'
    if DOPART01:
        print("Doing Part 01")
        map = Map()
        map.loadDay10(file01)
        print(map)
        map.findTrailHeads()
        map.findGoalRoutes()
        map.scoreTrailHeads01()
        map.scoreTrailHeads02()
 #       map.draw()


 