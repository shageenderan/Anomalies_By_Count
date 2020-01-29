# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from IPython import get_ipython

# %% [markdown]
# # People Count to JSON
# 
# Writes the number of people counted in each frame of a video to a json file

import os
import sys
import random
import math
import numpy as np
import skimage.io
import matplotlib
import matplotlib.pyplot as plt
from math import log

# Root directory of the project
ROOT_DIR = os.path.abspath("../")
MASK_DIR = os.path.join(ROOT_DIR, "mask")
# Import Mask RCNN
sys.path.append(MASK_DIR)  # To find local version of the library

from mrcnn import utils
import mrcnn.model as modellib
# Import COCO config
# sys.path.append(os.path.join(ROOT_DIR, "samples/coco/"))  # To find local version
import coco

get_ipython().run_line_magic('matplotlib', 'inline')

# Directory to save logs and trained model
MODEL_DIR = os.path.join(ROOT_DIR, "logs")

# Local path to trained weights file
COCO_MODEL_PATH = os.path.join(MASK_DIR, "mask_rcnn_coco.h5")
# Download COCO trained weights from Releases if needed
if not os.path.exists(COCO_MODEL_PATH):
    utils.download_trained_weights(COCO_MODEL_PATH)

# %% [markdown]
# ## Configurations
# 
# We'll be using a model trained on the MS-COCO dataset. The configurations of this model are in the ```CocoConfig``` class in ```coco.py```.
# 
# For inferencing, modify the configurations a bit to fit the task. To do so, sub-class the ```CocoConfig``` class and override the attributes you need to change.

class InferenceConfig(coco.CocoConfig):
    # Set batch size to 1 since we'll be running inference on
    # one image at a time. Batch size = GPU_COUNT * IMAGES_PER_GPU
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1

config = InferenceConfig()
config.display()

# %% [markdown]
# ## Create Model and Load Trained Weights
# Create model object in inference mode.
model = modellib.MaskRCNN(mode="inference", model_dir=MODEL_DIR, config=config)

# Load weights trained on MS-COCO
model.load_weights(COCO_MODEL_PATH, by_name=True)


# %%
# COCO Class names
# Index of the class in the list is its ID. For example, to get ID of
# the teddy bear class, use: class_names.index('teddy bear')
class_names = ['BG', 'person', 'bicycle', 'car', 'motorcycle', 'airplane',
               'bus', 'train', 'truck', 'boat', 'traffic light',
               'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird',
               'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear',
               'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie',
               'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
               'kite', 'baseball bat', 'baseball glove', 'skateboard',
               'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup',
               'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
               'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
               'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed',
               'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote',
               'keyboard', 'cell phone', 'microwave', 'oven', 'toaster',
               'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors',
               'teddy bear', 'hair drier', 'toothbrush']


# %%
import cv2
VIDEO_DIR = os.path.join(ROOT_DIR, "videos")
capture = cv2.VideoCapture(os.path.join(VIDEO_DIR, "earthquake_6.mp4"))

# Defining Constants 
FRAME_COUNT = 0

# Defining Variables
frames = []
seconds = 0.5   # this variable controls the interval between frames being analyzed, i.e. 0.5 -> every 0.5 seconds a frame is analyzed, 2 -> every 2 seconds a f                    rame is analyzed 
fps = capture.get(cv2.CAP_PROP_FPS) # Gets the frames per second
multiplier = fps * seconds
success = True
batch_size = 1

# %% [markdown]
# ## Run People Counting
counted_data = []
while success:
    frameId = int(round(capture.get(1)))
    success, frame = capture.read()
    if frame is None:
        break
    if frameId % multiplier == 0:
        frames.append(frame)
        if len(frames) == batch_size:
            results = model.detect(frames, verbose=0)
            print('FRAME_COUNT :{0}'.format(FRAME_COUNT))
            FRAME_COUNT += 1
            for i, item in enumerate(zip(frames, results)):
                frame = item[0]
                r = item[1]
                people_counted = list(r['class_ids']).count(1)
                counted_data.append({"count": people_counted})
            # Clear the frames array to start the next batch
            frames = []        
print("Done Counting")  
capture.release()


# %% [markdown]
# ## Write count to json file
import json
DATA_FILE_DIR = os.path.join(ROOT_DIR, "data_files")
with open(os.path.join(DATA_FILE_DIR, 'people_count.json'), 'w+') as outfil:
    json.dump(counted_data, outfil)

# %%
