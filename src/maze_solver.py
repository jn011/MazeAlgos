import argparse
from PIL import Image
from maze import Maze

def main():
    # example code for inputting input/output of maze.
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("InputMaze")
    # parser.add_argument("OutputMaze")
    args = parser.parse_args()
    print(args.InputMaze)
    '''

    # open given maze.png, if there is an error opening exit.
    try:
        myimage = Image.open("/media/james/SlowBigMan/MazeSolving/mazes/Daedelus/3x3.png")
    except:
        print("Error with image")
        exit()

    # Convert image to RGB for path highlighting.
    myimage = myimage.convert("RGB")
    width, height = myimage.size

    for x in range(height):
        # print(x)
        for y in range(width):
            r,g,b = myimage.getpixel((y,x)) 

        #put pixel if in first row of pixels or last row of pixels. 
            if r==g==b and r==255:
                if (x==0):
                    start = y
                    myimage.putpixel((y,x),(51,102,255))
                elif (x==height-1):
                    finish = y
                    myimage.putpixel((y,x),(51,102,255))
                    
    
    print (height)
    print( width)
    print(start)
    print(finish)
    maze = Maze(height, start, finish)
    
    # Save final image, concude program.
    myimage.save("/media/james/SlowBigMan/MazeSolving/new.png")
    print("JOB DONE")

main()