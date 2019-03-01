from PIL import Image
import numpy as np
class Maze:
    class Node:
        def __init__(self, height, width):
            self.nodeheight = height
            self.nodewidth = height
            self.neighbours = [None]
            

    def __init__(self, myimage):
        self.mazewidth, self.mazeheight = myimage.size
        self.myimage = myimage
        #self.adjmatrix = np.full((self.mazeheight, self.mazewidth), False, dtype=bool)
        self.start = None
        self.finish = None
    
    def findStart(self):
        for y in range(self.mazewidth):
            r,g,b = self.myimage.getpixel((y,0)) 
        # Set pixel as start if white in first row of pixels
            if r==g==b and r==255:
                    self.start = Maze.Node(0, y)
                    self.myimage.putpixel((y,0),(51,102,255))

    def findEnd(self):
        for y in range(self.mazewidth):
            r,g,b = self.myimage.getpixel((y,self.mazeheight-1)) 
        # Set pixel as finish if white in last row of pixels. 
            if r==g==b and r==255:
                    self.finish = Maze.Node(self.mazeheight, y)
                    self.myimage.putpixel((y,self.mazeheight-1),(51,102,255))

    
    # Adds a node to the adjacency matrix
    def addNode(self, mazeheight, mazewidth):
        g=1

    # Loop through image and find all nodes
    def findAllNodes(self):
        self.findStart()
        self.findEnd()
        for x in range(1, self.mazeheight-1):
            for y in range(self.mazewidth):
                if self.isNode(x,y):
                    self.myimage.putpixel((y,x),(51,102,255))

    # Checks if a given pixel is a node 
    # (junction, dead end, corner) excludes start/end
    def isNode(self, mazeheight, mazewidth):
        if self.pixelIsBlack(mazeheight, mazewidth):
            return False
        
        blackpixelsaround = 0

        if self.aboveIsBlack(mazeheight, mazewidth):
            blackpixelsaround = blackpixelsaround + 1
            if self.leftIsBlack(mazeheight, mazewidth):
                return True
        
        if self.belowIsBlack(mazeheight, mazewidth):
            blackpixelsaround = blackpixelsaround + 1
            if self.rightIsBlack(mazeheight, mazewidth):
                return True
        
        if self.leftIsBlack(mazeheight, mazewidth):
            blackpixelsaround = blackpixelsaround + 1
            if self.belowIsBlack(mazeheight, mazewidth):
                return True
        
        if self.rightIsBlack(mazeheight, mazewidth):
            blackpixelsaround = blackpixelsaround + 1
            if self.aboveIsBlack(mazeheight, mazewidth):
                return True
        
        # If there are 3 black walls around a
        # white pixel then there is a dead end
        if blackpixelsaround == 3:
            return True
        
        # If there is less than or equal to 1 black wall 
        # around a white pixel then there is a junction
        if blackpixelsaround <=1:
            return True

    # Checks if a given pixel is black
    def pixelIsBlack(self, mazeheight, mazewidth):
        r,g,b = self.myimage.getpixel((mazewidth, mazeheight))
        if r==g==b and r==0:
            return True
        else:
            return False

    # Checks if a the pixel above a given pixel is black
    def aboveIsBlack(self, mazeheight, mazewidth):
        if self.pixelIsBlack(mazeheight-1, mazewidth):
            return True
        else:
            return False

    # Checks if a the pixel below a given pixel is black
    def belowIsBlack(self, mazeheight, mazewidth):
        if self.pixelIsBlack(mazeheight+1, mazewidth):
            return True
        else:
            return False

    # Checks if a the pixel left a given pixel is black
    def leftIsBlack(self, mazeheight, mazewidth):
        if self.pixelIsBlack(mazeheight, mazewidth-1):
            return True
        else:
            return False

    # Checks if a the pixel right a given pixel is black
    def rightIsBlack(self, mazeheight, mazewidth):
        if self.pixelIsBlack(mazeheight, mazewidth+1):
            return True
        else:
            return False

"""    class Node:
        __init__(self, mazeheight, mazewidth):
            """