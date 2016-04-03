import re
import numpy

def read_pgm(filename, byteorder='>'):
    """Return image data from a raw PGM file as numpy array.

    Format specification: http://netpbm.sourceforge.net/doc/pgm.html

    """
    with open(filename, 'rb') as f:
        buffer = f.read()
    try:
        header, width, height, maxval = re.search(
            b"(^P5\s(?:\s*#.*[\r\n])*"
            b"(\d+)\s(?:\s*#.*[\r\n])*"
            b"(\d+)\s(?:\s*#.*[\r\n])*"
            b"(\d+)\s(?:\s*#.*[\r\n]\s)*)", buffer).groups()
    except AttributeError:
        raise ValueError("Not a raw PGM file: '%s'" % filename)
    return numpy.frombuffer(buffer,
                            dtype='u1' if int(maxval) < 256 else byteorder+'u2',
                            count=int(width)*int(height),
                            offset=len(header)
                            ).reshape((int(height), int(width)))
import glob
def listImages(path):
    return glob.glob(path+"*.pgm")
import csv

class UrbachCrater():
    def __init__(self,row):
        x,y,r = row[0],row[1],row[2]
        self.x=float(x)
        self.y=float(y)
        self.r=float(r)
    def __str__(self):
        return "x: %f,y: %f,r: %f"%(self.x,self.y,self.r)

def getImageId(image):
    words = image.split("/")
    imageName = words[len(words)-1]
    return imageName.split("tile")[1].split(".")[0]

    
def readGroundTruth(image):
    folder_gt = "CraterDataset/bandeira2010_gt/"
    
    imageId = getImageId(image)
    imageGt = folder_gt+imageId+"_gt.csv"
    print (imageGt)
    craters = []
    with open(imageGt, 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            crater = UrbachCrater(row)

            print (crater)
            craters.append(crater)
    # print (craters)
if __name__ == "__main__":
    from matplotlib import pyplot,figure
    urbachDatasetPath = "CraterDataset/urbach2009_tile_images/"
    # print name of files
    images = listImages(urbachDatasetPath)
    for image in images:
        readGroundTruth(image)
        exit()


    print (images)
    pyplot.figure()
    image = read_pgm(urbachDatasetPath+"tile1_24.pgm", byteorder='<')
    pyplot.imshow(image, pyplot.cm.gray)
    pyplot.figure()
    image = read_pgm(urbachDatasetPath+"tile1_24s.pgm", byteorder='<')
    pyplot.imshow(image, pyplot.cm.gray)
    pyplot.show()