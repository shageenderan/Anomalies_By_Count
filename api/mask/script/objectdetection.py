# Local file imports
from mask.samples.coco import coco
from mask.mrcnn import utils
import mask.mrcnn.model as modellib

# External library imports
import os, sys
import cv2
import numpy as np
import tensorflow as tf
import requests
import uuid
import math

"""
This file consists of the major server logic to be performed such as the object detection and anomaly detection algorithms
"""

# Batch size to be processed by the GPU at once
batch_size = 1

# Location constant variables
ROOT_DIR = os.path.join(os.getcwd(), "mask")
MODEL_DIR = os.path.join(ROOT_DIR, "logs")
COCO_MODEL_PATH = os.path.join(ROOT_DIR, "mask_rcnn_coco.h5")
VIDEO_DIR = os.path.join(os.getcwd(), "videos")
VIDEO_SAVE_DIR = os.path.join(os.getcwd(), "output")

# Class IDs defined by the COCO datasets
class_names = [
    'BG', 'person', 'bicycle', 'car', 'motorcycle', 'airplane',
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
    'teddy bear', 'hair drier', 'toothbrush'
]

# Key value pair of video content types
fileExtensions = {
    "x-flv": ".flv",
    "mp4": ".mp4",
    "quicktime": ".mov",
    "x-msvideo": ".avi",
    "x-ms-wmv": ".wmv",
    "avi": ".avi",
    "msvideo": ".avi"
}


# Function to load all the models for Mask RCNN
def load_models():
    config = tf.ConfigProto()
    config.inter_op_parallelism_threads = 1

    #################################### MODEL STUFF ####################################
    # To find local version
    sys.path.append(os.path.join(ROOT_DIR, "samples/coco/"))

    # If COCO models dont exist, download it. If necessary directories dont exist, create them
    if not os.path.exists(COCO_MODEL_PATH):
        utils.download_trained_weights(COCO_MODEL_PATH)
    if not os.path.exists(VIDEO_DIR):
        os.makedirs(VIDEO_DIR)
    if not os.path.exists(VIDEO_SAVE_DIR):
        os.makedirs(VIDEO_SAVE_DIR)

    class InferenceConfig(coco.CocoConfig):
        GPU_COUNT = 1
        IMAGES_PER_GPU = batch_size

    config = InferenceConfig()
    config.display()

    global model
    # Create model object in inference mode.
    model = modellib.MaskRCNN(mode="inference", model_dir=MODEL_DIR, config=config)

    # Load weights trained on MS-COCO
    model.load_weights(COCO_MODEL_PATH, by_name=True)


def random_colors(N):
    """
        generate random mask and bounding box colours for writing onto image frames
    """
    np.random.seed(1)
    colors = [tuple(255 * np.random.rand(3)) for _ in range(N)]
    return colors


def apply_mask(image, mask, color, alpha=0.5):
    """
        apply mask to image
    """
    for n, c in enumerate(color):
        image[:, :, n] = np.where(
            mask == 1,
            image[:, :, n] * (1 - alpha) + alpha * c,
            image[:, :, n]
        )
    return image


def display_instances(image, boxes, masks, ids, names, scores):
    global COUNT_WINDOW
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
    COUNT_WINDOW[(FRAME_COUNT - 1) % WINDOW_SIZE] = people_count
    anomaly, ema, diff = has_anomaly(people_count)
    ALL_COUNT.append(people_count)

    # Write necessary information to the image frame
    image = cv2.putText(image, 'People counted: {}'.format(people_count),
                        (10, 30), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 255, 255), 2)
    image = cv2.putText(image, 'EMA: {}'.format(ema),
                        (10, 50), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 255, 255), 2)
    image = cv2.putText(image, 'EMA DIFFERENCE: {}'.format(diff),
                        (10, 70), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 255, 255), 2)
    # If anomaly exists, write to iamge frame
    if anomaly:
        image = cv2.putText(image, 'ANOMALY DETECTED',
                            (10, 160), cv2.FONT_HERSHEY_COMPLEX, 0.7, (10, 10, 100), 2)
    return image, people_count, anomaly


# Function to detect anomalies based on current and previous information
def has_anomaly(curr_count):
    global ALL_COUNT, EMAS, COUNT_WINDOW, ANOMALIES, DIFFERENCES

    # Count number of objects in window
    num_count = sum(x is not None for x in COUNT_WINDOW)

    # If there is exactly 1 object in window, means no previous data as current count is appended to window beforehand.
    # Return False
    if num_count == 1:
        EMAS.append(curr_count)
        DIFFERENCES.append(0)
        return False, curr_count, 0

    # Calculate Exponential Moving Average
    ema = calc_ema(curr_count, EMAS[-1], num_count)

    # Difference in EMAs is an absolute value since EMA can increase or reduce
    difference = abs(ema - EMAS[-1])
    EMAS.append(ema)
    DIFFERENCES.append(difference)

    # Calculate current threshold for anomaly detection
    threshold = calc_threshold(num_count)

    # If EMA difference exceeds threshold, anomaly exists. Else, no anomaly
    if difference > threshold:
        ANOMALIES.append(len(ALL_COUNT))
        return True, ema, difference
    else:
        return False, ema, difference


# Function to calculate anomaly detection threshold
def calc_threshold(n):
    global MIN_THRESHOLD

    # Starting from 0.65, degrades to 0.3. Reasoning is because early in the window, an anomaly should be a sharp
    # difference in EMAs such as from 1 to 3 which would result in an EMA difference of 0.67. Degrades by 0.05 for each
    # EMA in window
    threshold = 0.5 - (0.05 * (n - 3))
    if threshold >= MIN_THRESHOLD:
        return threshold
    return MIN_THRESHOLD


# Exponential Moving Average (https://www.investopedia.com/terms/e/ema.asp)
def calc_ema(curr_count, prev_ema, n):
    # print(curr_count, prev_ema)
    smoothing = 2 / (1 + n)
    return curr_count * smoothing + prev_ema * (1 - smoothing)


def sum_list(lst):
    filtered = list(filter(lambda x: x is not None, lst))
    return sum(filtered)


# Function to be called by queued tasks for existing video files
def object_detection_file(file_name, video_id):
    path = os.path.join(VIDEO_DIR, file_name)
    object_detection(path, video_id)


# Function to be called by queued tasks for URL video files that need to be downloaded
def object_detection_url(url, video_id):
    # Generate a random UUID to name the videos. Does not guarantee uniqueness but significantly reduces clashing.
    randomGuid = str(uuid.uuid4())

    # Get content-type of video file and determines correct file extension
    req = requests.get(url)
    content_type = req.headers['content-type'].split('/')[-1]
    ext = fileExtensions[content_type]

    path = os.path.join(VIDEO_DIR, randomGuid + ext)
    with open(path, 'wb') as f:
        f.write(req.content)

    object_detection(path, video_id)


def object_detection(file_location, video_id):
    from app.models import Frame, Video
    # Get video file
    capture = cv2.VideoCapture(str(file_location))

    save_dir = os.path.join(VIDEO_SAVE_DIR, str(video_id))
    # Create directory for output
    try:
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
    except OSError:
        print('Error: Creating directory of data')

    global FRAME_COUNT, WINDOW_SIZE, COUNT_WINDOW, THRESHOLD, ALL_COUNT, EMAS, ANOMALIES, DIFFERENCES, MIN_THRESHOLD

    FRAME_COUNT = 0                     # Keeps track of the current frame no.
    WINDOW_SIZE = 20                    # Size of the sliding window
    COUNT_WINDOW = [None]*WINDOW_SIZE   # Sliding window - people count values are stored in this array in a sliding window manner
    MIN_THRESHOLD = 0.3                 # Minimum threshold for determining an anomaly
    ALL_COUNT = []                      # Array containing the people counted for every frame in a video
    EMAS = []                           # Array containing the ema for ever frame in a video
    DIFFERENCES = []                    # Array containing the difference in ema between two adjacent frames in a video. Used only for graphing purposes
    ANOMALIES = []                      # Array containing all frame no. where an anomaly had been detected, if empty then no anomaly has been detected

    #################################### Setting up parameters ####################################
    frames = []
    seconds = 0.5  # this variable controls the interval between frames being analyzed, i.e. 0.5 -> every 0.5 seconds a frame is analyzed, 2 -> every 2 seconds a frame is analyzed
    fps = math.ceil(capture.get(cv2.CAP_PROP_FPS))  # Gets the frames per second of video
    multiplier = int(round(fps * seconds))
    success = True
    #################################### Setting up parameters ####################################

    # While there exist a next frame.
    while success:
        # Get current frame_id
        frame_id = int(round(capture.get(1)))
        success, frame = capture.read()

        # If the frame id is a multiple of the multiplier, we want to capture the frame. This ensures that we only
        # capture a predetermined number of frames per second
        if frame_id % multiplier == 0:
            FRAME_COUNT += 1
            frames.append(frame)
            if len(frames) == batch_size:
                # Run object detection using loaded model
                results = model.detect(frames, verbose=0)

                # For each object detected, run function to write onto image frames
                for i, item in enumerate(zip(frames, results)):
                    frame = item[0]
                    r = item[1]
                    frame, people_counted, anomaly = display_instances(
                        frame, r['rois'], r['masks'], r['class_ids'], class_names, r['scores']
                    )

                    # Write frame to a JPG image
                    frame_number = FRAME_COUNT + i - batch_size
                    name = '{0}.jpg'.format(frame_number)
                    name = os.path.join(save_dir, name)
                    cv2.imwrite(name, frame)

                    # Write a new Frame object to database
                    timestamp = frame_number * seconds
                    video = Video.objects.get(pk=video_id)
                    f = Frame(video=video, frame_number=frame_number, timestamp=timestamp, count=people_counted,
                              anomaly=anomaly)
                    f.save()
                # Clear the frames array to start the next batch
                frames = []
    capture.release()
    print("Anomalies found in frames:{}".format(ANOMALIES))
    print("Processing completed. Written to {}".format(save_dir))


# Function to check if a video file with the given file name already exists in video directory
def check_video_exists(file_name):
    video_path = os.path.join(VIDEO_DIR, file_name)
    if os.path.exists(video_path):
        return True
    else:
        return False
