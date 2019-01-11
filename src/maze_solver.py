import argparse
from PIL import Image


def main():
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("InputMaze")
    # parser.add_argument("OutputMaze")
    args = parser.parse_args()
    print(args.InputMaze)
    '''
    try:
        myimage = Image.open("/media/james/SlowBigMan/MazeSolving/Mazes/Daedelus/3x3.png")
    except:
        print("Error with image")
        exit()

    myimage = myimage.convert("RGB")
    width, height = myimage.size
    for x in range(width):
        for y in range(height):
            r,g,b = myimage.getpixel((x,y)) 

            if r==g==b and r==255:
                myimage.putpixel((x,y),(51,102,255))

    myimage.save("/media/james/SlowBigMan/MazeSolving/new.png")
    

    print("JOB DONE")




main()