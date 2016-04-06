
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
import csv
import os
import re
import numpy
import sys
sys.path.append('../../svmCraters/trainingDataSetUI')
import imageCtrl
import imageUtil
import classCtrl
import exampleCtrl
from projectCtrl import getProject
from marsSchema import initDB

path = "CraterDataset%surbach2009_tile_images%s"%(os.sep,os.sep)
initDB()
project = getProject("Craters")


def listImages():
    return glob.glob(path+"*.pgm")

def plotImgs(imgs):
    fig, ax = plt.subplots()
    ax.imshow( imgs[710],plt.cm.gray)
    fig, ax = plt.subplots()
    ax.imshow( imgs[754],plt.cm.gray)
    fig, ax = plt.subplots()
    ax.imshow( imgs[700],plt.cm.gray)
    plt.show()

class UrbachCrater():
    def __init__(self,row):
        x,y,r = row[0],row[1],row[2]
        self.x=float(x)
        self.y=float(y)
        self.r=float(r)/2.0
    def __str__(self):
        return "x: %f,y: %f,r: %f"%(self.x,self.y,self.r)
    def getCropRec(self,image):
        r2 = self.r*2
        sizes = classCtrl.getExampleSizes(None)
        sizes.append(256)
        sizes.append(512)
        i = 0
        while (r2>sizes[i]) :
            # print r2
            # print i
            # print sizes[i]
            i+=1
        w = sizes[i]
        craterRec =  [self.x-w/2,self.y-w/2,w,w]
        craterData = imageUtil.cropImage(image,craterRec[0],craterRec[1],craterRec[2],craterRec[3])
        if(craterData.shape != (w,w)):
            return None,None
        return craterData,craterRec
        

def saveImageInProject(imageData,imgName):
    # print project.outputImageFolder
    imageInfo = imageCtrl.saveImage(project,imageData,imgName,None)
    # print "success save "
    # print imageInfo
    return imageInfo
def saveExamplesCrater(examplesData,examplesRec,imageInfo):
    taggedClass = classCtrl.getClass("craters")
    print "Saving examples "+taggedClass.name
    # exit()
    for i in range(len(examplesData)):
        exampleData = examplesData[i]
        exampleRec = examplesRec[i]
        
        exampleInfo = exampleCtrl.saveExample(taggedClass,project,imageInfo,exampleRec,exampleData)


from matplotlib import pyplot as plt

def extractCraters(image,craters):
    listCraterImgs = []
    listCraterRecs = []
    for crater in craters:
        craterImg,craterRec = crater.getCropRec(image) 
        if(craterImg!=None):
            listCraterImgs.append(craterImg)
            listCraterRecs.append(craterRec)
            print craterImg.shape
            print len(listCraterImgs)-1
    print image.shape
    return listCraterImgs,listCraterRecs

def plotCraters(img,craters):
    fig, ax = plt.subplots()
    ax.imshow(img,plt.cm.gray)
    for i in range(len(craters)):
        c = craters[i]
        circle1=plt.Circle((c.x,c.y),c.r,color='r',fill=False)
        fig.gca().add_artist(circle1)
    
    plt.show()
def getImageName(imageAbsPath):
    words = imageAbsPath.split(os.sep)
    imageName = words[len(words)-1]
    return imageName

def getImageId(image):
    imageName = getImageName(image)
    return imageName.split("tile")[1].split(".")[0]

def readGroundTruth(image):
    folder_gt = "CraterDataset%sbandeira2010_gt%s"%(os.path.sep,os.sep)
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
    return craters
