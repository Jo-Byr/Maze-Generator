# -*- coding: utf-8 -*-
"""
Created on Sat Nov 27 10:06:05 2021

@author: jonat
"""


from tkinter import Tk, Button, Canvas, RAISED, SUNKEN
from random import choice
from algorithmA import Tree, Result


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
        self.unit= unit
        self.wall_width = wall_width
        
        self.stack = Stack()
        
        #Converting the size of the maze from blocks to pixels
        self.h = 2*wall_width + h*unit + (h-1)*wall_width
        self.w = 2*wall_width + w*unit + (w-1)*wall_width
        
        self.canvas = Canvas(self.root, height = self.h, width = self.w, bg = "white",highlightthickness  = 0)
        self.canvas.pack()
        
        
        self.close_button = Button(self.root, text="Close", command = self.root.destroy)
        self.close_button.pack()
        
        self.new_button = Button(self.root, text="New maze", command = self.new)
        self.new_button.pack()
        
        #Options buttons and vars        
        self.start_button = Button(self.root, text = "Choose starting point")
        self.start_button.configure(command = self.start_switch)
        self.start_button.pack()
        
        self.end_button = Button(self.root, text = "Choose ending point")
        self.end_button.configure(command = self.end_switch)
        self.end_button.pack()
        
        self.new()
        
        
    def new(self):
        self.canvas.delete('all')
        
        #Matrix and variables for pathfinding
        self.path = [] #Holds the result of the pathfinding
        
        #Matrix of the maze used in algorithmA.py
        self.matrix = [[[0 for k in range(4)]for i in range(w)]for j in range(h)]
        for j in range(w):
            self.matrix[0][j] = [1,0,0,0]
            self.matrix[h-1][j] = [0,0,1,0]
            
        for i in range(h):
            self.matrix[i][0] = [0,0,0,1]
            self.matrix[i][w-1] = [0,1,0,0]
            
        self.matrix[0][0] = [1,0,0,1]
        self.matrix[0][w-1] = [1,1,0,0]
        self.matrix[h-1][0] = [0,0,1,1]
        self.matrix[h-1][w-1] = [0,1,1,0]
        
        #Generating the borders
        self.canvas.create_rectangle(0,0,wall_width,self.h,fill='black')
        self.canvas.create_rectangle(0,0,self.w,wall_width,fill='black')
        self.canvas.create_rectangle(0,self.h - wall_width,self.w,self.h,fill='black')
        self.canvas.create_rectangle(self.w - wall_width,0,self.w,self.h,fill='black')
        
        #Path-finding vars
        self.started = 0
        self.start_x = None
        self.start_y = None
        self.ended = 0
        self.end_x = None
        self.end_y = None
        self.choose_start = 0
        self.choose_end = 0
        self.start_button.config(relief = RAISED)
        self.end_button.config(relief = RAISED)
        
        #Iinitializing the stack
        self.stack.Push([0,0,h-1,w-1])
        self.next_step()
        
        
    def next_step(self):
        #Constructs the maze step-by-step
        while not(self.stack.isEmpty()):
            args = self.stack.Pop()
            Room(self,args[0],args[1],args[2],args[3],self.unit,self.wall_width)
            
            
    def options(self,event):
        """
        This functions handles the click inputs of the user :
            choosing or deleting a starting point
            choosing or deleteing an ending point
        """
        #Using winfo instead of event.x and event.y because these methods return incorrect values when pressing a button
        true_x = self.root.winfo_pointerx() - self.root.winfo_rootx()
        true_y = self.root.winfo_pointery() - self.root.winfo_rooty()
        
        x,y = true_x//(self.unit+self.wall_width),true_y//(self.unit+self.wall_width)
        x1 = x*(self.unit+self.wall_width) + self.wall_width + 1
        y1 = y*(self.unit+self.wall_width) + self.wall_width + 1
        x2 = x1 + self.unit -1
        y2 = y1 + self.unit -1
        
        if event.num == 1:
            #Left click
            if self.choose_start and self.started == 0 and (0 <= true_x <= self.w) and (0 <= true_y <= self.h):
                #Left click in the canvas without already having a starting point creates a new one
                self.started = 1
                self.canvas.create_rectangle(x1,y1,x2,y2, fill="red",outline = '')
                
                self.start_x = x
                self.start_y = y
                
                if x == self.end_x and y == self.end_y:
                    #If the user chooses the starting point as the position of the current ending point, we update the latter
                    self.end_x = None
                    self.end_y = None
                    self.ended = 0
                
            if self.choose_end and self.ended == 0 and (0 <= true_x <= self.w) and (0 <= true_y <= self.h):
                #Left click in the canvas without already having a ending point creates a new one
                self.ended = 1
                self.canvas.create_rectangle(x1,y1,x2,y2, fill="blue",outline = '')
                
                self.end_x = x
                self.end_y = y
                
                if x == self.start_x and y == self.start_y:
                    #If the user chooses the ending point as the position of the current starting point, we update the latter
                    self.start_x = None
                    self.start_y = None
                    self.started = 0
                
        
        if event.num == 3 or event.num == 2:
            #Right click
            if self.choose_start and self.started == 1 and x == self.start_x and y == self.start_y:
                #Right click on the starting point deletes it
                self.started = 0
                self.canvas.create_rectangle(x1,y1,x2,y2, fill="white",outline = '')
                
                self.start_x = None
                self.start_y = None
                self.pathfinding(1)
                
            if self.choose_end and self.ended == 1 and x == self.end_x and y == self.end_y:
                #Right click on the ending point deletes it
                self.ended = 0
                self.canvas.create_rectangle(x1,y1,x2,y2, fill="white",outline = '')
                
                self.end_x = None
                self.end_y = None
                self.pathfinding(1)
                
        if self.started and self.ended:
            self.path = Result(Tree(self.matrix,[self.start_x,self.start_y],[self.end_x,self.end_y])).result
            self.pathfinding(0)
            
            
    def pathfinding(self,clean):
        """
        This functions calls the pathfinding method developped in algortihmA.py and displays its result
        """
        for node in self.path:
            if (node[0] != self.start_x or node[1] != self.start_y) and (node[0] != self.end_x or node[1] != self.end_y):
                x1 = self.wall_width + node[0] * (self.wall_width + self.unit) +1
                x2 = x1 + self.unit - 1
                y1 = self.wall_width + node[1] * (self.wall_width + self.unit) + 1
                y2 = y1 + self.unit - 1
                
                if clean == 0:
                    self.canvas.create_rectangle(x1,y1,x2,y2,fill = "gray",outline = "")
                else:
                    self.canvas.create_rectangle(x1,y1,x2,y2,fill = "white",outline = "")

            
    def start_switch(self):
        """
        This functions changes the value of the variables choose_start and started, and the style of the start button
        """
        self.choose_end = 0
        self.end_button.config(relief = RAISED)
        if self.choose_start == 0:
            self.start_button.config(relief = SUNKEN)
            self.choose_start = 1
        else:
            self.start_button.config(relief = RAISED)
            self.choose_start = 0
        
        
    def end_switch(self):
        """
        This functions changes the value of the variables choose_end and ended, and the style of the end button
        """
        self.choose_start = 0
        self.start_button.config(relief = RAISED)
        if self.choose_end == 0:
            self.end_button.config(relief = SUNKEN)
            self.choose_end = 1
        else:
            self.end_button.config(relief = RAISED)
            self.choose_end = 0
    
    
    
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
                
                #Updating the A* matrix
                for x in range(self.xt,self.xb+1):
                    if x !=xh:
                        self.maze.matrix[yw][x][2] = 1
                        self.maze.matrix[yw+1][x][0] = 1
                        
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
            
                #Updating the A* matrix
                for y in range(self.yt,self.yb+1):
                    if y != yh:
                        self.maze.matrix[y][xw][1] = 1
                        self.maze.matrix[y][xw+1][3] = 1
                        
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
                self.maze.stack.Push([self.xt,self.yt,self.xb,yw])
                
            else:
                #Vertical wall - left room
                self.maze.stack.Push([xw+1,self.yt,self.xb,self.yb])
                self.maze.stack.Push([self.xt,self.yt,xw,self.yb])
            
            
            
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
        
        

h,w,unit,wall_width = 20,20,20,5
root = Tk()
maze = Maze(root,h,w,unit,wall_width)
root.bind("<Button-1>",maze.options)
root.bind("<Button-2>",maze.options)
root.bind("<Button-3>",maze.options)
root.mainloop()