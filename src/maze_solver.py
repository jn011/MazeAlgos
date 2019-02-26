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
        myimage = Image.open("/media/james/SlowBigMan/MazeSolving/mazes/Daedelus/16x16.png")
    except:
        print("Error with image")
        exit()

    # Convert image to RGB for path highlighting.
    myimage = myimage.convert("RGB")
    width, height = myimage.size

    for y in range(width):
            r,g,b = myimage.getpixel((y,0)) 
        # Set pixel as start if white in first row of pixels
            if r==g==b and r==255:
                    start = y
                    myimage.putpixel((y,0),(51,102,255))

    for y in range(width):
            r,g,b = myimage.getpixel((y,height-1)) 
        # Set pixel as finish if white in last row of pixels. 
            if r==g==b and r==255:
                    finish = y
                    myimage.putpixel((y,height-1),(51,102,255))
                    
    
    print(height)
    print(width)
    print(start)
    print(finish)
    maze = Maze(height, start, finish, myimage)

    # Loop through image and find all nodes except for start/end
    for x in range(1, height-1):
        for y in range(width):
            if maze.isNode(x,y):
                myimage.putpixel((y,x),(51,102,255))

    
    # Save final image, concude program.
    myimage.save("/media/james/SlowBigMan/MazeSolving/new.png")
    print("JOB DONE")

main()