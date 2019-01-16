import numpy

class Maze:
    def __init__(self, size, start, finish):
        self.adj_matrix = numpy.full((size, size), False)
        self.start = start
        self.finish = finish
        self.adj_matrix[0, start] = True
        self.adj_matrix[size-1, finish] = True



    def addNode(height, width):
        adj_matrix[height, width] = True
            
"""     class Node: 
    def __init__(self, width, height):
        self.width = width
        self.height = height
"""
    
