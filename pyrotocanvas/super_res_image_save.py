#!/usr/bin/env python
__author__ = "Adrian Rosebrock, Jake Gustafson"
import argparse
import time
import os
import sys
try:
    import cv2
except ImportError:
    sys.stderr.write("You must install OpenCV for Python or run this"
                     " using a venv with OpenCV.\n")
    exit(1)
myName = os.path.split(__file__)[-1]

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-m", "--model", required=True,
                help="path to super resolution model")
ap.add_argument("-i", "--image", required=True,
                help=("path to input image we want to resize"))
ap.add_argument("-o", "--output", required=True,
                help=("path to output image after scaling"))
args = vars(ap.parse_args())

# extract the model name and model scale from the file path
modelName = args["model"].split(os.path.sep)[-1].split("_")[0].lower()
modelScale = args["model"].split("_x")[-1]
modelScale = int(modelScale[:modelScale.find(".")])

# Initialize OpenCV's super resolution DNN object, load the super
# resolution model from disk, and set the model name and scale
print("[INFO] loading super resolution model: {}"
      "".format(args["model"]))
print("[INFO] model name: {}".format(modelName))
print("[INFO] model scale: {}".format(modelScale))
sr = cv2.dnn_superres.DnnSuperResImpl_create()
sr.readModel(args["model"])
sr.setModel(modelName, modelScale)

# Load the input image from disk and display its spatial dimensions.
image = cv2.imread(args["image"])
outPath = args["output"]
print("[INFO] w: {}, h: {}".format(image.shape[1], image.shape[0]))

# Use the super resolution model to upscale the image, timing how
# long it takes.
start = time.time()
upscaled = sr.upsample(image)
end = time.time()
print("[INFO] super resolution took {:.6f} seconds"
      "".format(end - start))

# Show the spatial dimensions of the super resolution image.
print("[INFO] w: {}, h: {}".format(upscaled.shape[1],
      upscaled.shape[0]))

# Resize the image using standard bicubic interpolation.
# start = time.time()
# bicubic = cv2.resize(image, (upscaled.shape[1], upscaled.shape[0]),
#           interpolation=cv2.INTER_CUBIC)
# end = time.time()
# print("[INFO] bicubic interpolation took {:.6f} seconds"
#       "".format(end - start))

# Show the original input image, bicubic interpolation image, and
# super resolution deep learning output.
# cv2.imshow("Original", image)
# cv2.imshow("Bicubic", bicubic)
# cv2.imshow("Super Resolution", upscaled)
# cv2.waitKey(0)
sys.stderr.write('[{}] writing "{}"'.format(myName, outPath))
cv2.imwrite(outPath, upscaled)
