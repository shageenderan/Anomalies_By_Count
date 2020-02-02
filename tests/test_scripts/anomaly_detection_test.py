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
    import cv2
    global COUNT_WINDOW
    # global ALL_COUNT
    """
        take the image and results and apply the mask, box, and Label
    """
    n_instances = boxes.shape[0]
    colors = random_colors(n_instances)

    if not n_instances:
        pass
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
    if num_count == 1:
        # not enough previous data
        EMAS.append(curr_count)
        DIFFERENCES.append(0)
        return False, curr_count, 0
    
    # Calculate new ema
    ema = calc_ema(curr_count, EMAS[-1], num_count)

    # Calculate Difference in ema
    difference = abs(ema-EMAS[-1])
    EMAS.append(ema)
    DIFFERENCES.append(difference)

    # Calculate current threshold
    threshold = calc_threshold(num_count)

    # Check for anomaly
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
    smoothing = 2/(1+n)
    return curr_count*smoothing + prev_ema*(1-smoothing)

# %% [markdown]
# ## Retrieve Raw Video File and Set Parameters
def analyze_video(test_video, test_video_dir):
    import cv2
    VIDEO_SAVE_DIR = os.path.join(test_video_dir, ".analyzed_output")
    capture = cv2.VideoCapture(os.path.join(test_video_dir, test_video))
    # Create directory for output
    try:
        if not os.path.exists(VIDEO_SAVE_DIR):
            os.makedirs(VIDEO_SAVE_DIR)
    except OSError:
        print('Error: Creating directory of data')

    # Defining Constants for Anomaly Detection
    global FRAME_COUNT, WINDOW_SIZE, COUNT_WINDOW, MIN_THRESHOLD, ALL_COUNT, EMAS, DIFFERENCES, ANOMALIES
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
    fps = math.ceil(capture.get(cv2.CAP_PROP_FPS)) # Gets the frames per second
    multiplier = fps * seconds
    success = True

    # %% [markdown]
    # ## Run Video Analysis
    print("Starting analysis for {}...".format(test_video))
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
                # print('FRAME_COUNT :{0}'.format(FRAME_COUNT))
                FRAME_COUNT += 1
                for i, item in enumerate(zip(frames, results)):
                    frame = item[0]
                    r = item[1]
                    frame = display_instances(
                        frame, r['rois'], r['masks'], r['class_ids'], class_names, r['scores']
                    )
                    name = '{0}_{1}.jpg'.format(test_video.split(".")[0], FRAME_COUNT + i - batch_size)
                    name = os.path.join(VIDEO_SAVE_DIR, name)
                    cv2.imwrite(name, frame)
                # Clear the frames array to start the next batch
                frames = []        
    print("Done Analysis")  
    capture.release()
    return ANOMALIES

# %% [markdown]
# ## Testing
# Extract all test video file names
import os
TEST_VIDEO_DIR = os.path.join(ROOT_DIR, "videos") 
DATA_FILE_DIR = os.path.join(ROOT_DIR, "data_files") 

test_videos = [f for f in os.listdir(TEST_VIDEO_DIR) if not f.startswith('.')]

print(test_videos)

# %% [markdown]
# ## Extract ground truths
def int_list(lst):
    if lst[0] == ' ':
        return []
    return [int(n) for n in lst]

ground_truth_file = str(os.path.join(DATA_FILE_DIR, "ground_truths.txt"))
with open(ground_truth_file, "r") as f:
    raw_data = f.read()
    raw_split = raw_data.split("\n")

    video_titles = raw_split[0::2]
    anomaly_starts = [int_list(elem.split(",")) for elem in raw_split[1::2]]

    ground_truth = dict(zip(video_titles, anomaly_starts))

# %% [markdown]
# ## Define Metric functions
def calc_accuracy(tp, tn, fp, fn):
    return (tp + tn)/(tp+tn+fp+fn)

def calc_error_rate(accuracy):
    return 1-accuracy

def calc_recall(tp, fn):
    if not tp and not fn:
        return 1.0
    return tp/(tp+fn)

def calc_specificity(tn, fp):
    return tn/(tn+fp)

def calc_precision(tp, fp):
    if not tp and not fp:
        return 0.0
    return tp/(tp+fp)

def calc_false_positive_rate(tn, fp):
    return fp/(tn+fp)

def avg(lst):
    return sum(lst)/len(lst)

# %% [markdown]
# ## Test each video and compare with ground truth
# Get name of new log file
TEST_LOG_DIR = os.path.join(ROOT_DIR, "logs")
log_num = len([f for f in os.listdir(TEST_LOG_DIR)])
log_file_name = os.path.join(TEST_LOG_DIR, "log_{}.txt".format(log_num))

# Define constants for calculating averages later
ALL_ACCURACIES = []
ALL_ERROR_RATES = []
ALL_RECALL = []
ALL_SPECIFICITY = []
ALL_PRECISION = []
ALL_FPR = []
count = 0
# Start comparisions and writting 
with open(log_file_name, "w+") as outfil:
    for video in test_videos:
        try:
            global ALL_COUNT
            video_key = video.split(".")[0]
            predicted_anomalies = analyze_video(video, TEST_VIDEO_DIR)
            false_negative_list = []
            true_positive_list = []
            for truth in ground_truth[video_key]:
                correctly_predicted = False
                tmp_predicted = -1
                for predicted in predicted_anomalies:
                    if truth in predicted_anomalies:
                        correctly_predicted = True
                        predicted_anomalies.remove(predicted)
                        true_positive_list.append(predicted)
                        break
                    if abs(predicted-truth) <= 2: # 2 frames leeway = 1 seconds leeway
                        correctly_predicted = True
                        if predicted > tmp_predicted:
                            tmp_predicted = predicted
                if not correctly_predicted: 
                    false_negative_list.append(truth)
                else:
                    if tmp_predicted != -1:
                        predicted_anomalies.remove(tmp_predicted)
                        true_positive_list.append(tmp_predicted)
            false_positive_list = predicted_anomalies
            true_negative_list = [x for x in range(len(ALL_COUNT)) if x not in ground_truth[video_key] and x not in false_positive_list]
            
            true_positive = len(true_positive_list)
            true_negative = len(true_negative_list)
            false_positive = len(false_positive_list)
            false_negative = len(false_negative_list)

            accuracy_rate = calc_accuracy(true_positive, true_negative, false_positive, false_negative)
            recall = calc_recall(true_positive, false_negative)
            specificity = calc_specificity(true_negative, false_positive)
            precision = calc_precision(true_positive, false_positive)
            fpr = calc_false_positive_rate(true_negative, false_positive)

            outfil.write(video+"\n")
            outfil.write("Total Frames: {}\n[TRUE NEGATIVE] Frames correctly not predicted: {}\n".format(len(ALL_COUNT), len(true_negative_list)))
            outfil.write("[TRUE POSITIVE] Frames Correctly Predicted Anomalies: {}\n".format(true_positive_list))
            outfil.write("[FALSE NEGATIVE] Failed To Predict Anomalies At: {}\n".format(false_negative_list))
            outfil.write("[FALSE POSITIVES] Wrongly Predicted Anomalies At:{}\n".format(false_positive_list))
            outfil.write("Accuracy Rate: {}\n".format(accuracy_rate))
            outfil.write("Error Rate: {}\n".format(1-accuracy_rate))
            outfil.write("Recall/True Positive Rate: {}\n".format(recall))
            outfil.write("Specificity/True Negative Rate: {}\n".format(specificity))
            outfil.write("Precision/Positive Predictive Value: {}\n".format(precision))
            outfil.write("False Positive Rate: {}\n\n".format(fpr))

            ALL_ACCURACIES.append(accuracy_rate)
            ALL_ERROR_RATES.append(1-accuracy_rate)
            ALL_RECALL.append(recall)
            ALL_SPECIFICITY.append(specificity)
            ALL_PRECISION.append(precision)
            ALL_FPR.append(fpr)

            count += 1
            print("{}/{} done".format(count,len(test_videos)-1))
        except KeyError:
            print("Did not find ground truth for file:{}".format(video_key))
    
    outfil.write("\nAVERAGE ACCURACY RATE: {}\n".format(avg(ALL_ACCURACIES)))
    outfil.write("AVERAGE ERROR RATE: {}\n".format(avg(ALL_ERROR_RATES)))
    outfil.write("AVERAGE RECALL: {}\n".format(avg(ALL_RECALL)))
    outfil.write("AVERAGE SPECIFICITY: {}\n".format(avg(ALL_SPECIFICITY)))
    outfil.write("AVERAGE PRECISION: {}\n".format(avg(ALL_PRECISION)))
    outfil.write("AVERAGE FPR: {}\n".format(avg(ALL_FPR)))
# %%[markdown]
# ## Cleanup Files
import os, shutil
folder = os.path.join(TEST_VIDEO_DIR, ".analyzed_output")
for filename in os.listdir(folder):
    file_path = os.path.join(folder, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))

# %%
