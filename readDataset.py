
import urbachUtil
 # import saveImage3,loadImage

if __name__ == "__main__":
	
	urbachDatasetPath = urbachUtil.path 
	# print name of files
	images = urbachUtil.listImages()
	for imageAbsPath in images:
		imageName = urbachUtil.getImageName(imageAbsPath)
		print imageName 
		image = urbachUtil.read_pgm(imageAbsPath, byteorder='<')
		imageInfo = urbachUtil.saveImageInProject(image,imageName)
		# read craters
		craters = urbachUtil.readGroundTruth(imageAbsPath)
		cratersData,cratersRec = urbachUtil.extractCraters(image,craters)
		urbachUtil.saveExamplesCrater(cratersData,cratersRec,imageInfo)

		# urbachUtil.plotImgs(craterImages)
		# urbachUtil.plotCraters(image,craters)
		exit()


	# print (images)
	# pyplot.figure()

	# image = read_pgm(urbachDatasetPath+"tile1_24.pgm", byteorder='<')
	# plotCraters(image,crates)
	# pyplot.imshow(image, pyplot.cm.gray)
	# pyplot.figure()
	# image = read_pgm(urbachDatasetPath+"tile1_24s.pgm", byteorder='<')
	# pyplot.imshow(image, pyplot.cm.gray)
	# pyplot.show()