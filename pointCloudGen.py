from PIL import Image
import pathlib
import math
import numpy as np

def colour_to_depth(colour):
    #Find out what depth looks like when we get the image
    visual_exaggeration_factor = 5 # Use this to make it more obviously "paper like"
    return np.mean(colour / 255) * visual_exaggeration_factor 

#Assumed Image taken from directly above, and the coolour relates to the depth
def get_point_cloud(inputImage, outputFileName, scale):
    im = Image.open(pathlib.Path(inputImage))
    outputFile = open(outputFileName,"w")
    pix = im.load()
    # Downscale for speed reasons (its pretty computationally expensive and slow if you go past ~200x200)
    downscale = ((int)(im.width*scale), (int)(im.height*scale))
    pix = np.array(im.resize(downscale).getdata())
    for x in range(downscale[0]):
        for y in range(downscale[1]):
            outputFile.write(str(x)+','+str(y)+','+str(colour_to_depth(pix[x + y * downscale[0]]))+'\n')
    outputFile.close()
    im.close()
