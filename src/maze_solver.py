import argparse
import os 
import time 
from PIL import Image
from maze import Maze

def main():
    # example code for inputting input/output of maze.
    
    parser = argparse.ArgumentParser()
    parser.add_argument("InputMaze")
    # parser.add_argument("OutputMaze")
    args = parser.parse_args()
    # print(args.InputMaze)
    

    # open given maze.png, if there is an error opening exit.
    try:
        myimage = Image.open(args.InputMaze)
    except:
        print("Error finding/opening image")
        exit()

    # Convert image to RGB for path highlighting.
    myimage = myimage.convert("RGB")

    print("Maze Loaded Successfully!")
    
    # It should be noted that mazes inputted into the programs 
    # for testing will be the same dimension height and width, will need to be improved later 

    maze = Maze(myimage)
    maze.findAllNodes()
    maze.buildAdjMatrix()
    print("Graph built for maze on nodes where a decision must be made... ")
    maze.bfsPathFinder()

    # Save final image in current working directory, conclude program
    cwd = os.getcwd()
    myimage.save(str(cwd+"/completed_maze.png"))

    print("Path found in your maze! \nImage Saved in current directory as: " + cwd + "/completed_maze.png")
    print("Runtime: ")

# Times the running of main function
start_time = time.time()
main()
print("Runtime: --- %s seconds ---" % (round(time.time() - start_time,2)))
