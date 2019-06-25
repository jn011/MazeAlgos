from PIL import Image
from collections import deque
import numpy as np
import math
import queue

class Maze:
    #store start and finish as translatedNodeNum for ease of use with adjacency list
    def __init__(self, myimage):
        self.mazewidth, self.mazeheight = myimage.size
        self.myimage = myimage
        self.adjList = {}
        # self.nodelist = []
        self.start = None
        self.finish = None
    
    def findStart(self):
        for y in range(self.mazewidth):
            r,g,b = self.myimage.getpixel((y,0)) 
        # Set pixel as start if white in first row of pixels
            if r==g==b and r==255:
                self.addToNodeAdjList(0,y)
                self.start = self.translateFromHeightWidthToNodeNumber(0,y)

    def findEnd(self):
        for y in range(self.mazewidth):
            r,g,b = self.myimage.getpixel((y,self.mazeheight-1)) 
        # Set pixel as finish if white in last row of pixels. 
            if r==g==b and r==255:
                self.addToNodeAdjList(self.mazeheight-1,y)
                self.finish = self.translateFromHeightWidthToNodeNumber(self.mazeheight-1,y)

    # Loop through image and find all nodes and add to NodeList
    def findAllNodes(self):
        self.findStart()
        
        for x in range(1, self.mazeheight-1):
            for y in range(self.mazewidth):
                if self.isNode(x,y):
                    self.addToNodeAdjList(x,y)

        self.findEnd()
    
    # Add node to adjacency List
    def addToNodeAdjList(self, height, width):
        self.adjList[self.translateFromHeightWidthToNodeNumber(height,width)] = []

    # Builds adjacency list for maze
    def buildAdjList(self):
        for currentnode in self.adjList.keys():
            for previousnode in self.adjList.keys():
                if (previousnode < currentnode):
                    if(self.isAdjacent(currentnode,previousnode)):
                        self.addAjacencyToAdjList(currentnode,previousnode)
                else:
                    break

    #Add adjacent nodes to adjacency list as well as distance between points in a tuple(adjacent node, distance to node)
    def addAjacencyToAdjList(self, node1, node2):
        if (node2 not in self.adjList[node1] and node1 not in self.adjList[node2]):
            self.adjList[node1].append(node2)
            self.adjList[node2].append(node1)
    
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
        #Get number of possible nodes and intialize visited as False, finish is the final node + 1 (includes 0)
        # and the array will not have to be bigger than that
        numPossibleNodes = self.finish + 1

        # visited has to be size of numNodes x numNodes as 
        visited = np.full(numPossibleNodes + 1, False, dtype=bool)

        # Queue for BFS 
        visited[self.start] = True
        nodes = deque([self.start])

        parent = {}
        while nodes:
            #pop node from queue 
            currentnode = nodes.popleft()
            
            #Find and check children of current node, if not visited enqueue and set node visited
            for i in self.adjList[currentnode]:
                if (not visited[i]):
                    visited[i] = True
                    nodes.append(i)
                    parent[i] = currentnode

        # backtrace from parent nodes and build path from parents dictionary
        path = [self.finish]
        while path[-1] != self.start:
            path.append(parent[path[-1]])
            path.reverse()

        # Trim path from beginning to end and draw path on image
        endofpath = path.index(self.finish) + 1
        path = path[0:endofpath]
        # print(path)
        self.drawPath(path)

    # A* Search to solve path from start to end node using manhattan distance as heuristic
    def astarPathFinder(self):
        open_set = queue.PriorityQueue() #priority queue to store tuples of (score, node)
        open_set.put((0, self.start))
        came_from = {}
        # Cost so far
        g_score = {}
        came_from[self.start] = None
        g_score[self.start] = 0

        # While there are still elements in queue
        while not open_set.empty():
            current_node_priority, current_node = open_set.get()
            
            if (current_node == self.finish):
                break

            for next_node in self.adjList[current_node]:
                new_score = g_score[current_node] + self.distBetweenTwoNodes(current_node, next_node)
                if next_node not in g_score or new_score < g_score[next_node]:
                    g_score[next_node] = new_score
                    # Heuristical priority using manhattan distance
                    priority = new_score + self.manhattanDistanceBetweenTwoNodes(next_node, self.finish)
                    open_set.put((priority, next_node))
                    came_from[next_node] = current_node
        
        # Construct path from parent dictionary by backtracing from finishing nodes
        path = []

        key = self.finish
        while key is not None:
            path.append(key)
            key = came_from.get(key)

        # Reverse the path
        path.reverse() 
        self.drawPath(path)
            
    def manhattanDistanceBetweenTwoNodes(self, node1, node2):
        x1,y1 = self.translateFromNodeNumberToHeightWidth(node1)
        x2,y2 = self.translateFromNodeNumberToHeightWidth(node2)
        return abs(x1 - x2) + abs(y1 - y2)

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

    def distBetweenTwoNodes(self, node1, node2):
        node1height,node1width = self.translateFromNodeNumberToHeightWidth(node1)
        node2height,node2width = self.translateFromNodeNumberToHeightWidth(node2)
        distance = 0
        # Horizontal adjacency
        if (node1height == node2height):
            if (node1width < node2width):
                distance = node2width - node1width
            else:
                distance = node1width - node2width
        # Vertical adjacency
        elif (node1width == node2width):
            if(node1height < node2height):
                distance = node2height - node1height
            else:
                distance = node1height - node2height
        
        # Is distance to another point, change to distance between two points
        distance = distance - 1
        return distance

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