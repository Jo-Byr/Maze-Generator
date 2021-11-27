# -*- coding: utf-8 -*-
"""
Created on Sat Nov 27 10:06:05 2021

@author: jonat
"""


from tkinter import Tk, Button, Canvas
from random import choice,seed

seed(10)
import sys
sys.setrecursionlimit(15000)

class Maze():
    """
    An instance of this class represents the maze in its entirety
    """
    def __init__(self,root,h,w,unit,wall_width):
        """
        h and w are the height and width of the maze in number of blocks
        unit is the size in pixels of a block
        each wall is wall_width pixels wide
        """
        self.root = root
        root.title("Maze")
        self.stack = Stack()
        
        self.h = 2*wall_width + h*unit + (h-1)*wall_width
        self.w = 2*wall_width + w*unit + (w-1)*wall_width
        
        self.canvas = Canvas(self.root, height = self.h, width = self.w, bg = "white",highlightthickness  = 0)
        self.canvas.pack()
        
        
        self.close_button = Button(self.root, text="Close", command = self.root.destroy)
        self.close_button.pack()
        
        self.new_button = Button(self.root, text="New maze", command = self.new)
        self.new_button.pack()
        
        self.new()
        
    def new(self):
        self.canvas.delete("all")
        
        #Generating the borders
        self.canvas.create_rectangle(0,0,wall_width,self.h,fill='black')
        self.canvas.create_rectangle(0,0,self.w,wall_width,fill='black')
        self.canvas.create_rectangle(0,self.h - wall_width,self.w,self.h,fill='black')
        self.canvas.create_rectangle(self.w - wall_width,0,self.w,self.h,fill='black')
        
        Room(self,0,0,h-1,w-1,unit,wall_width)
    
class Room():
    def __init__(self,maze,xt,yt,xb,yb,unit,wall_width):
        """
        maze is the maze in which the room is created
        
        [xt,yt] are the top left coordinates of the top left block of the room
        [xb,yb] are the top left coordinates of the bottom right block of the room
        
        unit is the size in pixel if a block
        wall_width is the width in pixel of a wall
        """
        self.maze = maze
        
        self.xt = xt
        self.yt = yt
        self.xb = xb
        self.yb = yb
        self.unit = unit
        self.wall_width = wall_width
        
        self.create_wall()
        
    def create_wall(self):
        
        if (self.xb == self.xt or self.yb == self.yt):
            """
            In the case the room is 1 block wide or high, this room is finished and we pop the stack
            """
            if not(self.maze.stack.isEmpty()):
                arg = self.maze.stack.Pop()
                Room(self.maze,arg[0],arg[1],arg[2],arg[3],self.unit,self.wall_width)
        
        else:
            """
            In other case, we create a wall
            First we must choose an orientation : 0 is horizontal, 1 is vertical
            """
            if (self.xb - self.xt) == 1:
                #If the room is 1 block large, the wall must be horizontal
                orientation = 0
            elif (self.yb - self.yt) == 1:
                #If the room is 1 block high, the wall must be vertical
                orientation = 1
            else:
                orientation = choice([0,1])
                
            """
            Next is the position of the wall
            """
            if not(orientation):
                #Horizontal wall
                yw = choice(list(range(self.yt,self.yb))) #Ordinate in blocks of the top left corner of the wall
            
                xw1 = self.xt*(self.unit + self.wall_width)+self.wall_width #Abciss in pixels of the top left corner of the wall
                yw1 = (yw+1)*(self.unit + self.wall_width) #Ordinate in pixels of the top left corner of the wall
                xw2 = xw1 + (self.unit + self.wall_width)*(self.xb-self.xt+1) #Abciss in pixels of the bottom right corner of the wall
                yw2 = yw1 + self.wall_width #Ordinate in pixels of the bottom right corner of the wall

                xh = choice(list(range(self.xt,self.xb+1))) #Abciss in blocks of the hole in the wall

                xh1 = self.wall_width + xh*(self.unit + self.wall_width)+1 #Abciss in pixels of the top left corner of the hole
                yh1 = yw1 #Ordinate in pixels of the top left corner of the hole
                xh2 = xh1 + self.unit -1 #Abciss in pixels of the bottom right corner of the hole
                yh2 = yw2+1 #Ordinate in pixels of the bottom right corner of the hole
                
            else:
                #Vertical wall
                xw = choice(list(range(self.xt,self.xb))) #Abciss in blocks of the top left corner of the wall
            
                xw1 = (xw+1)*(self.unit + self.wall_width) #Abciss in pixels of the top left corner of the wall
                yw1 = self.yt*(self.unit + self.wall_width)+self.wall_width #Ordinate in pixels of the top left corner of the wall
                xw2 = xw1 + self.wall_width #Abciss in pixels of the bottom right corner of the wall
                yw2 = yw1 + (self.unit + self.wall_width)*(self.yb-self.yt+1) #Ordinate in pixels of the bottom right corner of the wall

                yh = choice(list(range(self.yt,self.yb+1))) #Abciss in blocks of the hole in the wall

                xh1 = xw1 #Abciss in pixels of the top left corner of the hole
                yh1 = self.wall_width + yh*(self.unit + self.wall_width) + 1 #Ordinate in pixels of the top left corner of the hole
                xh2 = xw2 + 1 #Abciss in pixels of the bottom right corner of the hole
                yh2 = yh1 + self.unit - 1 #Ordinate in pixels of the bottom right corner of the hole
            
            #Generating the wall and the hole in it
            self.maze.canvas.create_rectangle(xw1,yw1,xw2,yw2,fill="black")
            self.maze.canvas.create_rectangle(xh1,yh1,xh2,yh2,fill="white",width=0,outline = '')
            
            """
            Creating a wall separates the current room into 2
            One is the next one treated, the other is pushed in the stack
            """
            if not(orientation):
                #Horizontal wall - top room
                self.maze.stack.Push([self.xt,yw+1,self.xb,self.yb])
                Room(self.maze,self.xt,self.yt,self.xb,yw,self.unit,self.wall_width)
            else:
                #Vertical wall - left room
                self.maze.stack.Push([xw+1,self.yt,self.xb,self.yb])
                Room(self.maze,self.xt,self.yt,xw,self.yb,self.unit,self.wall_width)   
                
            
            
class Stack():
    def __init__(self):
        self.values = []
        
    def Pop(self):
        return self.values.pop()
    
    def Push(self,element):
        self.values.append(element)
        
    def isEmpty(self):
        return self.values == []
    
    def show(self):
        return(self.values)
        
        
    
h,w,unit,wall_width = 20,20,20,3
root = Tk()
maze = Maze(root,h,w,unit,wall_width)
root.mainloop()