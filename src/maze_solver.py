import argparse
import os 
import time 
from PIL import Image
from maze import Maze

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_maze")
    parser.add_argument("algo_type")
    args = parser.parse_args()    

    # open given maze.png, if there is an error opening exit.
    try:
        myimage = Image.open(args.input_maze)
    except:
        print("Error finding/opening image")
        exit()

    algo_type = str(args.algo_type).lower()
    if algo_type != "bfs" and algo_type != "a*":
        print("Invalid pathfinding algorithm entered")
        exit()

    # Convert image to RGB for path highlighting.
    myimage = myimage.convert("RGB")

    print("Maze Loaded Successfully!")
    
    # It should be noted that mazes inputted into the programs 
    # for testing will be the same dimension height and width, will need to be improved later 

    maze = Maze(myimage)
    maze.findAllNodes()
    maze.buildAdjList()
    print("Maze adjacency list built!")

    if algo_type == "bfs":
        maze.bfsPathFinder()
    else:
        maze.astarPathFinder()
    
    # Save final image in current working directory, conclude program
    cwd = os.getcwd()
    myimage.save(str(cwd+"/completed_maze.png"))

    print("Path found in your maze! \nImage Saved in current directory as: " + cwd + "/completed_maze.png")

# Times the running of main function
start_time = time.time()
main()
print("Runtime: --- %s seconds ---" % (round(time.time() - start_time,2)))
