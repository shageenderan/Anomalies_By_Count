######################################################################################################################################################
# Not working yet, need to get ground truth from chee yiing first 
######################################################################################################################################################
# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from IPython import get_ipython

# %% [markdown]
# # Anomaly Detection Test
# 
# Testing anomaly detection on a video file

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
ROOT_DIR = os.path.abspath("../mask")

# Import Mask RCNN
sys.path.append(ROOT_DIR)  # To find local version of the library
from mrcnn import utils
import mrcnn.model as modellib
# Import COCO config
# sys.path.append(os.path.join(ROOT_DIR, "samples/coco/"))  # To find local version
import coco

get_ipython().run_line_magic('matplotlib', 'inline')

# Directory to save logs and trained model
MODEL_DIR = os.path.join(ROOT_DIR, "logs")

# Local path to trained weights file
COCO_MODEL_PATH = os.path.join(ROOT_DIR, "mask_rcnn_coco.h5")
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


# %% [markdown]
# ## Defining Drawing Functions
def safe_log(n):
    return log(n) if n != 0 else 0

def random_colors(N):
    np.random.seed(1)
    colors = [tuple(255 * np.random.rand(3)) for _ in range(N)]
    return colors


def apply_mask(image, mask, color, alpha=0.5):
    """apply mask to image"""
    for n, c in enumerate(color):
        image[:, :, n] = np.where(
            mask == 1,
            image[:, :, n] * (1 - alpha) + alpha * c,
            image[:, :, n]
        )
    return image


def display_instances(image, boxes, masks, ids, names, scores):
    global COUNT_WINDOW
    # global ALL_COUNT
    """
        take the image and results and apply the mask, box, and Label
    """
    n_instances = boxes.shape[0]
    colors = random_colors(n_instances)

    if not n_instances:
        print('NO INSTANCES TO DISPLAY')
    else:
        assert boxes.shape[0] == masks.shape[-1] == ids.shape[0]

    for i, color in enumerate(colors):
        if ids[i] == 1:
            if not np.any(boxes[i]):
                continue

            y1, x1, y2, x2 = boxes[i]
            label = names[ids[i]]
            score = scores[i] if scores is not None else None
            caption = '{} {:.2f}'.format(label, score) if score else label
            mask = masks[:, :, i]

            image = apply_mask(image, mask, color)
            image = cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
            image = cv2.putText(image, caption, (x1, y1),
                                cv2.FONT_HERSHEY_COMPLEX, 0.7, color, 2)

    people_count = list(ids).count(1)
    COUNT_WINDOW[(FRAME_COUNT-1) % WINDOW_SIZE] = people_count
    anomaly, ema, diff = has_anomaly(people_count)
    ALL_COUNT.append(people_count)
    image = cv2.putText(image, 'People counted: {}'.format(people_count), 
            (10, 30), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 255, 255), 2)
    image = cv2.putText(image, 'EMA: {}'.format(ema), 
            (10, 50), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 255, 255), 2)
    image = cv2.putText(image, 'EMA DIFFERENCE: {}'.format(diff), 
            (10, 70), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 255, 255), 2)
    if anomaly:
            image = cv2.putText(image, 'ANOMALY DETECTED', 
            (10, 160), cv2.FONT_HERSHEY_COMPLEX, 0.7, (10, 10, 100), 2)
    return image

# %% [markdown]
# ## Define Anomaly Detection Algorithm
def has_anomaly(curr_count):
    global ALL_COUNT, EMAS, COUNT_WINDOW, ANOMALIES
    num_count = sum(x is not None for x in COUNT_WINDOW)
    # num_count = len(ALL_COUNT)
    if num_count == 1:
        # not enough previous data
        EMAS.append(curr_count)
        DIFFERENCES.append(0)
        return False, curr_count, 0
    # average_count = sum_list(COUNT_WINDOW)/num_count
    # ema = calc_ema(curr_count, EMAS[-1], num_count)
    ema = calc_ema(curr_count, EMAS[-1], num_count)
    difference = abs(ema-EMAS[-1])
    EMAS.append(ema)
    # print(difference)
    DIFFERENCES.append(difference)
    threshold = calc_threshold(num_count)
    print(threshold)
    if difference > threshold:
        ANOMALIES.append(len(ALL_COUNT))
        return True, ema, difference
    else:
        return False, ema, difference

def calc_threshold(n):
    threshold = 0.5-(0.05*(n-3))
    if threshold >= MIN_THRESHOLD:
        return threshold
    return MIN_THRESHOLD

# Exponential Moving Average (https://www.investopedia.com/terms/e/ema.asp)
def calc_ema(curr_count, prev_ema, n):
    # print(curr_count, prev_ema)

    smoothing = 2/(1+n)
    return curr_count*smoothing + prev_ema*(1-smoothing)

def sum_list(lst):
    filtered = list(filter(lambda x: x is not None, lst))
    return sum(filtered)

# %% [markdown]
# ## Retrieve Raw Video File and Set Parameters
def analyze_video(test_video):
    import cv2
    VIDEO_DIR = os.path.join(ROOT_DIR, "videos")
    VIDEO_SAVE_DIR = os.path.join(VIDEO_DIR, "anomaly_tests")
    capture = cv2.VideoCapture(os.path.join(VIDEO_DIR, 'anomalies/' + test_video))
    # Create directory for output
    try:
        if not os.path.exists(VIDEO_SAVE_DIR):
            os.makedirs(VIDEO_SAVE_DIR)
    except OSError:
        print('Error: Creating directory of data')

    # Defining Constants for Anomaly Detection
    FRAME_COUNT = 0
    WINDOW_SIZE = 20
    COUNT_WINDOW = [None]*WINDOW_SIZE
    MIN_THRESHOLD = 0.3
    ALL_COUNT = []
    EMAS = []
    DIFFERENCES = []
    ANOMALIES = []

    # Defining Anomaly Detection Variables
    frames = []
    seconds = 0.5   # this variable controls the interval between frames being analyzed, i.e. 0.5 -> every 0.5 seconds a frame is analyzed, 2 -> every 2 seconds a f                    rame is analyzed 
    fps = capture.get(cv2.CAP_PROP_FPS) # Gets the frames per second
    multiplier = fps * seconds
    success = True

    # %% [markdown]
    # ## Run Video Analysis
    batch_size = 1
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
                    frame = display_instances(
                        frame, r['rois'], r['masks'], r['class_ids'], class_names, r['scores']
                    )
                    name = '{0}.jpg'.format(FRAME_COUNT + i - batch_size)
                    name = os.path.join(VIDEO_SAVE_DIR, name)
                    cv2.imwrite(name, frame)
                    print('writing to file:{0}'.format(name))
                # Clear the frames array to start the next batch
                frames = []        
    print("Done Analysis")  
    capture.release()
    print("Anomalies found in frames:{}".format(ANOMALIES))
    return ANOMALIES

# %% [markdown]
# ## Draw Count Graph
matplotlib.pyplot.plot(ALL_COUNT)
matplotlib.pyplot.ylabel("People Counted")
matplotlib.pyplot.show()

# %% [markdown]
# ## Draw EMA Graph
matplotlib.pyplot.plot(EMAS)
matplotlib.pyplot.ylabel("EMA of People Counted")
matplotlib.pyplot.show()

# %% [markdown]
# ## Draw EMA Difference Graph
matplotlib.pyplot.plot(DIFFERENCES)
matplotlib.pyplot.ylabel("EMA of People Counted")
matplotlib.pyplot.show()

# %% [markdown]
# ## Testing
# Extract all test video file names
import os
TEST_DIR = os.path.join(ROOT_DIR, "test")
TEST_VIDEO_DIR = os.path.join(TEST_DIR, "videos") 

test_videos = [f for f in os.listdir(TEST_VIDEO_DIR)]

print(test_videos)

# %% [markdown]
# Extract ground truths
def int_list(lst):
    if lst[0] == '':
        return []
    return [int(n) for n in lst]

ground_truth_file = str(os.path.join(TEST_DIR, "ground_truths.txt"))
with open(ground_truth_file, "r") as f:
    raw_data = f.read()
    raw_split = raw_data.split("\n")

    video_titles = raw_split[0::2]
    anomaly_starts = [int_list(elem.split(",")) for elem in raw_split[1::2]]

    ground_truth = dict(zip(video_titles, anomaly_starts))


# %% [markdown]
# Test each video and compare with ground truth
for video in test_videos:
    predicted_anomalies = analyze_video(video)
    print(predicted_anomalies)
    print(ground_truth[video])
    
