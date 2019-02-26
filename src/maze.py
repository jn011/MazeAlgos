from PIL import Image
class Maze:
    def __init__(self, height, start, finish,myimage):
        self.height = height
        self.start = start
        self.finish = finish
        self.myimage = myimage

    # Checks if a given pixel is a node 
    # (junction, dead end, corner) excludes start/end
    def isNode(self, height, width):
        if self.pixelIsBlack(height, width):
            return False
        
        blackpixelsaround = 0

        if self.aboveIsBlack(height, width):
            blackpixelsaround = blackpixelsaround + 1
            if self.leftIsBlack(height, width):
                return True
        
        if self.belowIsBlack(height, width):
            blackpixelsaround = blackpixelsaround + 1
            if self.rightIsBlack(height, width):
                return True
        
        if self.leftIsBlack(height, width):
            blackpixelsaround = blackpixelsaround + 1
            if self.belowIsBlack(height, width):
                return True
        
        if self.rightIsBlack(height, width):
            blackpixelsaround = blackpixelsaround + 1
            if self.aboveIsBlack(height, width):
                return True
        
        # If there are 3 black walls around a
        # white pixel then there is a dead end
        if blackpixelsaround == 3:
            return True
        
        # If there are less than or equal to 1 black wall 
        # around a white pixel then there is a junction
        if blackpixelsaround <=1:
            return True

    # Checks if a given pixel is black
    def pixelIsBlack(self, height, width):
        r,g,b = self.myimage.getpixel((width, height))
        if r==g==b and r==0:
            return True
        else:
            return False

    # Checks if a the pixel above a given pixel is black
    def aboveIsBlack(self, height, width):
        if self.pixelIsBlack(height-1, width):
            return True
        else:
            return False

    # Checks if a the pixel below a given pixel is black
    def belowIsBlack(self, height, width):
        if self.pixelIsBlack(height+1, width):
            return True
        else:
            return False

    # Checks if a the pixel left a given pixel is black
    def leftIsBlack(self, height, width):
        if self.pixelIsBlack(height, width-1):
            return True
        else:
            return False

    # Checks if a the pixel right a given pixel is black
    def rightIsBlack(self, height, width):
        if self.pixelIsBlack(height, width+1):
            return True
        else:
            return False
