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

if __name__ == "__main__":
    from matplotlib import pyplot,figure
    urbachDatasetPath = "CraterDataset/urbach2009_tile_images/"
    # print name of files
    images = listImages(urbachDatasetPath)
    print (images)
    pyplot.figure()
    image = read_pgm(urbachDatasetPath+"tile1_24.pgm", byteorder='<')
    pyplot.imshow(image, pyplot.cm.gray)
    pyplot.figure()
    image = read_pgm(urbachDatasetPath+"tile1_24s.pgm", byteorder='<')
    pyplot.imshow(image, pyplot.cm.gray)
    pyplot.show()