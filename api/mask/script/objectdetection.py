import os, sys
import cv2
import numpy as np
from pathlib import Path
from mask.mrcnn import utils
import mask.mrcnn.model as modellib
import tensorflow as tf
import requests
from urllib.parse import urlparse
from mask.samples.coco import coco

# import uuid
# import mimetypes
# #import magic
# import urllib
# from winmagic import magic


batch_size = 1

ROOT_DIR = os.path.join(os.getcwd(), "mask")
MODEL_DIR = os.path.join(ROOT_DIR, "logs")
COCO_MODEL_PATH = os.path.join(ROOT_DIR, "mask_rcnn_coco.h5")
VIDEO_DIR = os.path.join(os.getcwd(), "videos")
VIDEO_SAVE_DIR = os.path.join(os.getcwd(), "output")

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


def load_models():
    config = tf.ConfigProto()
    config.inter_op_parallelism_threads = 1

    #################################### MODEL STUFF ####################################
    # To find local version
    sys.path.append(os.path.join(ROOT_DIR, "samples/coco/"))

    if not os.path.exists(COCO_MODEL_PATH):
        utils.download_trained_weights(COCO_MODEL_PATH)

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
    """take the image and results and apply the mask, box, and Label"""
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

    people_counted = list(ids).count(1)
    image = cv2.putText(image, 'People counted: {}'.format(people_counted)
                        , (10, 30), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 255, 255), 2)
    return image, people_counted


def object_detection_file(file_name, video_id):
    path = os.path.join(VIDEO_DIR, file_name)
    object_detection(path, video_id)


def object_detection_url(url, video_id):
    # randomGuid = str(uuid.uuid4())

    file_name = os.path.basename(urlparse(url).path)
    path = os.path.join(VIDEO_DIR, file_name)

    if not os.path.exists(path):
        req = requests.get(url)
        with open(path, 'wb') as f:
            f.write(req.content)

    # mime = magic.Magic(mime=True)
    # mimes = mime.from_file(fileLocation)  # Get mime type
    # ext = mimetypes.guess_all_extensions(mimes)[0]  # Guess extension
    # os.rename(fileLocation, fileLocation + ext)  # Rename file

    object_detection(path, video_id)


def object_detection(file_location, video_id):
    from app.models import Frame, Video
    frame_count = 0

    # Get video file
    capture = cv2.VideoCapture(str(file_location))

    save_dir = os.path.join(VIDEO_SAVE_DIR, str(video_id))
    # Create directory for output
    try:
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
    except OSError:
        print('Error: Creating directory of data')

    #################################### Setting up parameters ####################################
    frames = []
    seconds = 0.5  # this variable controls the interval between frames being analyzed, i.e. 0.5 -> every 0.5 seconds a frame is analyzed, 2 -> every 2 seconds a frame is analyzed
    fps = capture.get(cv2.CAP_PROP_FPS)  # Gets the frames per second
    multiplier = fps * seconds
    success = True
    #################################### Setting up parameters ####################################

    while success:
        frame_id = int(round(capture.get(1)))
        success, frame = capture.read()

        if frame_id % multiplier == 0:
            frame_count += 1
            frames.append(frame)
            if len(frames) == batch_size:
                results = model.detect(frames, verbose=0)
                for i, item in enumerate(zip(frames, results)):
                    frame = item[0]
                    r = item[1]
                    frame, people_counted = display_instances(
                        frame, r['rois'], r['masks'], r['class_ids'], class_names, r['scores']
                    )
                    frame_number = frame_count + i - batch_size
                    name = '{0}.jpg'.format(frame_number)
                    name = os.path.join(save_dir, name)
                    cv2.imwrite(name, frame)
                    timestamp = frame_number * seconds
                    video = Video.objects.get(pk=video_id)
                    f = Frame(video=video, frame_number=frame_number, timestamp=timestamp, count=people_counted)
                    f.save()
                # Clear the frames array to start the next batch
                frames = []
    capture.release()
    print("Processing completed. Written to {}".format(save_dir))


def check_video_exists(file_name):
    video_path = os.path.join(VIDEO_DIR, file_name)
    if os.path.exists(video_path):
        return True
    else:
        return False
