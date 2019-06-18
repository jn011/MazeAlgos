from PIL import Image
from collections import deque
import numpy as np
import sys

class Maze:
    #store start and finish as translatedNodeNum for ease of use with adjacency matrix
    def __init__(self, myimage):
        self.mazewidth, self.mazeheight = myimage.size
        self.myimage = myimage
        self.nodelist = []
        self.adjmatrix = np.full((self.mazeheight*self.mazeheight, self.mazeheight*self.mazeheight), False, dtype=bool)
        self.start = None
        self.finish = None
    
    def findStart(self):
        for y in range(self.mazewidth):
            r,g,b = self.myimage.getpixel((y,0)) 
        # Set pixel as start if white in first row of pixels
            if r==g==b and r==255:
                    self.addToNodeList(0,y)
                    self.start = self.translateFromHeightWidthToNodeNumber(0,y)

    def findEnd(self):
        for y in range(self.mazewidth):
            r,g,b = self.myimage.getpixel((y,self.mazeheight-1)) 
        # Set pixel as finish if white in last row of pixels. 
            if r==g==b and r==255:
                    self.addToNodeList(self.mazeheight-1,y)
                    self.finish = self.translateFromHeightWidthToNodeNumber(self.mazeheight-1,y)

    # Loop through image and find all nodes and add to NodeList
    def findAllNodes(self):
        self.findStart()
        
        for x in range(1, self.mazeheight-1):
            for y in range(self.mazewidth):
                if self.isNode(x,y):
                    self.addToNodeList(x,y)

        self.findEnd()
    
    # Adds a node to the NodeList
    def addToNodeList(self, height, width):
        self.nodelist.append(self.translateFromHeightWidthToNodeNumber(height,width))

    #Builds adjacency matrix from nodelist
    def buildAdjMatrix(self):
        for currentnode in self.nodelist:            
            for previousnode in self.nodelist[0:self.nodelist.index(currentnode)]:
                if(self.isAdjacent(currentnode,previousnode)):
                    self.setAdjacentInAdjMatrix(currentnode,previousnode) 

    #Sets two node numebrs as adjacent in adjacency matrix
    def setAdjacentInAdjMatrix(self, node1, node2):
        self.adjmatrix[node1][node2] = True
        self.adjmatrix[node2][node1] = True
    
    #Takes an inputted nodes position in terms of height and width and finds its node number  
    def translateFromHeightWidthToNodeNumber(self, height, width): 
        nodeNum = (self.mazewidth * height) + width
        return nodeNum

    #takes a translated node number and converts to given image height and width
    def translateFromNodeNumberToHeightWidth(self, nodeNumber):
        height = nodeNumber // self.mazeheight
        width = nodeNumber % self.mazeheight
        return [height,width]

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

    #Takes in two Node Numbers and checks adjacency between the two nodes
    def isAdjacent(self,node1, node2):
        node1height,node1width = self.translateFromNodeNumberToHeightWidth(node1)
        node2height,node2width = self.translateFromNodeNumberToHeightWidth(node2)

        # simple case (one pixel above or below)
        if(node1height == node2height - 1 or node2height == node1height - 1 ):
            if(node1width == node2width):
                return True

        if (node1height == node2height):
            #Same height node1 to node2 adjacency check
            if(node1width < node2width):
                for pixelwidth in range(node1width,node2width):
                    if(self.pixelIsBlack(node1height,pixelwidth)):
                        return False

                return True
            #Same height node2 to node1 adjacency check
            elif(node2width < node1width):
                for pixelwidth in range(node2width,node1width):
                    if(self.pixelIsBlack(node1height,pixelwidth)):
                        return False

                return True

        if (node1width == node2width):
            # Same width node1 height to node2 adjacency check
            if (node1height< node2height):
                for pixelheight in range(node1height,node2height):
                    if(self.pixelIsBlack(pixelheight,node1width)):
                        return False
                
                return True
            # Same width node2 height to node1 adjacecny check
            elif(node2height < node1height):
                for pixelheight in range(node2height,node1height):
                    if(self.pixelIsBlack(pixelheight,node1width)):
                        return False
                
                return True

        return False

    def bfsPathFinder(self):
        #Get number of possible nodes and intialize visited as False
        numNodes = len(self.adjmatrix)
        visited = np.full(numNodes, False, dtype=bool)

        # Queue for BFS 
        visited[self.start] = True
        nodes = deque([self.start])

        parent = {}
        while (nodes):
            #pop node from queue 
            currentnode = nodes.popleft()
            
            #Find and check children of current node, if not visited enqueue and set node visited
            for i in range(1,numNodes):
                if (not visited[i]):
                    if (self.adjmatrix[currentnode][i]):
                        visited[i] = True
                        nodes.append(i)
                        parent[i] = currentnode

        # backtrace from parent nodes and build path from parents dictionary
        path = [self.finish]
        while path[-1] != self.start:
            path.append(parent[path[-1]])
            path.reverse()

        # Trim path 
        endofpath = path.index(self.finish) + 1
        path = path[0:endofpath]
        self.drawPath(path)



    def drawPath(self, path):
        for i in range(len(path)):

            # current nodes height, width 
            currentheight, currentwidth = self.translateFromNodeNumberToHeightWidth(path[i])
            
            #Draw a path from previous node to this node, start drawing on second element in path
            if (self.start == path[i]):
                continue
            else:
                
                #parent height and width 
                parentheight, parentwidth = self.translateFromNodeNumberToHeightWidth(path[i-1]) 
                
                # horizontal path, when a parent is to the (1)left or (2)right of current node 
                if (currentheight == parentheight):
                    if (parentwidth < currentwidth):
                        for w in range(parentwidth, currentwidth + 1):
                            self.markPixelAsRed(currentheight, w)
                    else:
                        for w in range(currentwidth, parentwidth + 1):
                            self.markPixelAsRed(currentheight, w)
                # vertical path, when a parent is (1)above or (2)below the current node 
                elif (currentwidth == parentwidth):
                    if (parentheight < currentheight):
                        for h in range(parentheight, currentheight):
                            self.markPixelAsRed(h, currentwidth)
                    else:
                        for h in range(currentheight, parentheight):
                            self.markPixelAsRed(h, currentwidth)

                #Mark pixel of mazes end node if reached as red
                if (self.translateFromHeightWidthToNodeNumber(currentheight,currentwidth) == path[-1]):
                    self.markPixelAsRed(currentheight, currentwidth)


    def markPixelAsRed(self, height, width):
        self.myimage.putpixel((width,height),(247,47,47))

    def markPixelAsBlue(self, height, width):
        self.myimage.putpixel((width,height),(51,102,255))

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