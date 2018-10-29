import pandas as pd
import numpy as np
import scipy.misc
import pydicom
import glob
import sys
import os

from scipy.ndimage.interpolation import zoom

# !gitclone http s: // github.com / fizyr / keras - retinanet
# os.chdir("keras-retinanet")
# python setup.py build_ext - -inplace

DATA_DIR = "/home/radonc/Projects/kg/rsna/Data/input_png/"
ROOT_DIR = "/home/radonc/Projects/kg/rsna/Data/working/"

# I converted training set DICOMs to PNGs, it should be part of the data environment
train_pngs_dir = os.path.join(DATA_DIR, "stage_1_train_images")
test_dicoms_dir = os.path.join(DATA_DIR, "stage_1_test_images/")

# Create annotations for RetinaNet training
import pandas as pd

bbox_info = pd.read_csv(os.path.join(DATA_DIR, "stage_1_train_labels.csv"))
detailed_class_info = pd.read_csv(
    os.path.join(DATA_DIR, "stage_1_detailed_class_info.csv"))
detailed_class_info = detailed_class_info.drop_duplicates()

# To get started, we'll train on positives only
positives = detailed_class_info[detailed_class_info["class"] == "Lung Opacity"]
# Annotations file should have no header and columns in the following order:
# filename, x1, y1, x2, y2, class
positives = positives.merge(bbox_info, on="patientId")
positives = positives[["patientId", "x", "y", "width", "height", "Target"]]
positives["patientId"] = [os.path.join(train_pngs_dir, "{}.jpeg".format(_)) for _ in positives.patientId]
positives["x1"] = positives["x"]
positives["y1"] = positives["y"]
positives["x2"] = positives["x"] + positives["width"]
positives["y2"] = positives["y"] + positives["height"]
positives["Target"] = "opacity"
del positives["x"], positives["y"], positives["width"], positives["height"]

# If you want to add negatives, follow the same format as above, except put NA for x, y, width, and height
annotations = positives

# Before we save to CSV, we have to do some manipulating to make sure
# bounding box coordinates are saved as integers and not floats
# Note: This is only necessary if you include negatives in your annotations
annotations = annotations.fillna(88888)
annotations["x1"] = annotations.x1.astype("int32").astype("str")
annotations["y1"] = annotations.y1.astype("int32").astype("str")
annotations["x2"] = annotations.x2.astype("int32").astype("str")
annotations["y2"] = annotations.y2.astype("int32").astype("str")
annotations = annotations.replace({"88888": None})
annotations = annotations[["patientId", "x1", "y1", "x2", "y2", "Target"]]
annotations.to_csv(os.path.join(ROOT_DIR, "annotations.csv"), index=False, header=False)

# We also need to save a file containing the classes
classes_file = pd.DataFrame({"class": ["opacity"], "label": [0]})
classes_file.to_csv(os.path.join(ROOT_DIR, "classes.csv"), index=False, header=False)

# ImageNet pre-trained ResNet50 backbone
# Image size: 256 x 256
# Batch size: 1
# Epochs: 1
# Steps per epoch: 1,000
# Data augmentation
# !python / kaggle / working / keras - retinanet / keras_retinanet / bin / train.py - -backbone
# "resnet50" - -image - min - side
# 256 - -image - max - side
# 256 - -batch - size
# 1 - -random - transform - -epochs
# 1 - -steps
# 1000
# csv / kaggle / working / annotations.csv / kaggle / working / classes.csv
#
# # Convert model
# !python / kaggle / working / keras - retinanet / keras_retinanet / bin / convert_model.py / kaggle / working / keras - retinanet / snapshots / resnet50_csv_01.h5 / kaggle / working / keras - retinanet / converted_model.h5





