# -*- coding: utf-8 -*-
"""
Created on Sat Nov 27 20:34:55 2021

@author: jonat
"""

#https://khayyam.developpez.com/articles/algo/astar/

class Tree():
    def __init__(self,matrix,depart,arrival):
        """
        matrix is list of list of list
        It is of size n*m*4 for n lines, m columns and 4 values for North, East, South and West
        These values are at 1 if there's an obstacle, and other otherwise
        
        depart and arrival are tuples representing the depart and arrival points
        """
        self.matrix = matrix
        self.h = len(matrix)
        self.w = len(matrix[0])
        
        #Generatinga matrix of nodes (cf. below) from matrix
        self.tree = [[0 for k in range(self.w)]for i in range(self.h)]
        
        for i in range(self.h):
            for j in range(self.w):
                self.tree[i][j] = Node(self,j,i,None,matrix[i][j][0],matrix[i][j][1],matrix[i][j][2],matrix[i][j][3])
        
        self.depart = Node(self,depart[0],depart[1],None,matrix[depart[1]][depart[0]][0],matrix[depart[1]][depart[0]][1],matrix[depart[1]][depart[0]][2],matrix[depart[1]][depart[0]][3])
        self.arrival = Node(self,arrival[0],arrival[1],None,matrix[arrival[1]][arrival[0]][0],matrix[arrival[1]][arrival[0]][1],matrix[arrival[1]][arrival[0]][2],matrix[arrival[1]][arrival[0]][3])
        
        #Open and closed lists used in the A* algorithm
        self.open_list = []
        self.closed_list = [self.depart]
        
        #Node currently considered
        self.current = self.depart
        
        self.run()
        
    def run(self):
        #This method execute one step of the A* algorithm
        while self.current.x != self.arrival.x or self.current.y != self.arrival.y:
            neighbours = self.current.neighbours()   
            
            for node in neighbours:
                if node in self.closed_list:
                    pass
                elif node in self.open_list:
                    cost = ((node.x - self.current.x)**2 + (node.y - self.current.y)**2)**(1/2) + ((node.x - self.arrival.x)**2 + (node.y - self.arrival.y)**2)**(1/2)
                    if node.cost() > cost:
                        node.parent = self.current
                else:
                    node.parent = self.current
                    self.open_list.append(node)
                    
            
            best = None
            minimum = (self.h**2 + self.w**2)**(1/2)
            for node in self.open_list:
                if node.cost()<minimum:
                    best = node
                    minimum = node.cost()
        
            if best != None:
                self.open_list.remove(best)
                self.closed_list.append(best)
                self.current = best
            
        """   
        if self.current.x != self.arrival.x or self.current.y != self.arrival.y:
            self.run()
        """
    
class Result:
    def __init__(self,tree):
        """
        This class gives the result of the pathfinding, going through the research list backwards from parent to parent
        """
        self.result = []
        
        self.closed_list = tree.closed_list
        
        node = self.closed_list[-1]
        while not(node.x == tree.depart.x and node.y == tree.depart.y):
            self.result.append([node.x,node.y])
            node = node.parent  
        
class Node():
    """
    This class defines all the variables of one node of the tree
    """
    def __init__(self,tree,x,y,parent,north,east,south,west):
        self.tree = tree
        
        self.x = x
        self.y = y
        
        self.parent = parent
        
        self.north = north
        self.east = east
        self.south = south
        self.west = west
        
    def neighbours(self):
        neighbours = []
        
        if self.y>0 and self.north == 0:
            neighbours.append(self.tree.tree[self.y-1][self.x])
            
        if self.y<self.tree.h-1 and self.south == 0:
            neighbours.append(self.tree.tree[self.y+1][self.x])
            
        if self.x>0 and self.west == 0:
            neighbours.append(self.tree.tree[self.y][self.x-1])
            
        if self.x<self.tree.w-1 and self.east == 0:
            neighbours.append(self.tree.tree[self.y][self.x+1])
    
        return neighbours
    
    def cost(self):
        return ((self.x - self.parent.x)**2 + (self.y - self.parent.y)**2)**(1/2) + ((self.x - self.tree.arrival.x)**2 + (self.y - self.tree.arrival.y)**2)**(1/2)
    