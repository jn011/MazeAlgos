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
    
    # It should be noted that mazes inputted into the programs 
    # for testing will be the same height x width
    maze = Maze(myimage)
    maze.findAllNodes()

    # Save final image, concude program.
    myimage.save("/media/james/SlowBigMan/MazeSolving/new.png")
    print("JOB DONE")

main()