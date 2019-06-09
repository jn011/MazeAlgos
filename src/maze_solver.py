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
        myimage = Image.open("/media/james/SlowBigMan/MazeSolving/mazes/Daedelus/6x6.png")
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

    print("MH: " + str(maze.mazeheight) + "  MW: " + str(maze.mazewidth))
    
    for x in range(0,maze.mazeheight):
        for y in range (0,maze.mazewidth):
            nodeNum = maze.translateFromHeightWidthToNodeNumber(x,y)
            print(str(x) + ", " + str(y) + ":\t" + str(nodeNum) + "\t (h,w):\t " + str(maze.translateFromNodeNumberToHeightWidth(nodeNum)))
            
    
    # print("0,0: " + str(maze.translateToNodeNumber(0,0)))
    # print("1,4: " + str(maze.translateToNodeNumber(1,4)))
    # print("3,4: " + str(maze.translateToNodeNumber(3,4)))
    # print("12,12: " + str(maze.translateToNodeNumber(12,12)))

main()