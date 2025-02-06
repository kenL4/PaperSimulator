from PIL import Image
import pathlib

def colour_to_depth(colour):
    return colour[0] #Find out what depth looks like when we get the image

#Assumed Image taken from directly above, and the coolour relates to the depth
def get_point_cloud(inputImage, outputFileName):
    im = Image.open(pathlib.Path(inputImage))
    outputFile = open(outputFileName)
    pix = im.load()
    print(im.size)
    for x in range(im.size[0]):
        for y in range(im.size[1]):
            outputFile.write(str(x)+','+str(y)+','+str(colour_to_depth(pix[x,y]))+'\n')
    outputFile.close()
    im.close()
