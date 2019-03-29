import csv
import glob
import os
import re
import subprocess

import yaml

from ..common.AppData import AppSettings, TestData, VideoData
from ..common.Datafiles import get_all_paths, get_paths, get_session_names
from ..common.Dimension import Dimension, dimension_constructor
from ..common.KeyFrame import KeyFrame
from ..common.Point import Point, point_constructor
from ..common.Rect import Rect, rect_constructor

yaml.add_constructor(u"!Dimension", dimension_constructor, yaml.Loader)
yaml.add_constructor(u"!Point", point_constructor, yaml.Loader)
yaml.add_constructor(u"!Rect", rect_constructor, yaml.Loader)


def filename(session_date, image_name, frame_no):
    return "%s_%s_%d.png" % (session_date, image_name, frame_no)


train_csvfile = open("puck_training.csv", "w", newline="")
validation_csvfile = open("puck_validation.csv", "w", newline="")
train_writer = csv.writer(
    train_csvfile, delimiter=" ", quotechar="|", quoting=csv.QUOTE_MINIMAL
)
validation_writer = csv.writer(
    validation_csvfile, delimiter=" ", quotechar="|", quoting=csv.QUOTE_MINIMAL
)

counter = 0
session_names = get_session_names()
for session_name in session_names:
    print("Extracting training frames from session {:s}...".format(session_name))
    for path in get_paths("yaml", session_name, training=True, testing=False):
        head, tail = os.path.split(path)
        head, session = os.path.split(head)
        base, ext = tail.split(".")
        m = re.match(r"\d+", session_name)
        session_date = m.group(0)

        print("Reading videodata from {0}".format(path))
        with open(path, "r") as stream:
            data = yaml.load(stream, yaml.Loader)

        # if "app_settings" in data:
        #     settings = AppSettings(data["app_settings"])

        # if "video_data" in data:
        #     videodata = VideoData(data["video_data"])

        if "test_data" in data:
            testdata = TestData(data["test_data"])
        else:
            raise Exception("No test data")

        hit_frames = testdata.get_all_hit_frames()
        for frame_no in hit_frames:
            name = filename(session_date, base, frame_no)

            # Exclude misses and bounces.
            if (
                testdata.is_miss_frame(frame_no)
                or testdata.is_bounce_frame(frame_no)
                or testdata.get_keyframe_type(frame_no) == KeyFrame.AMBIGUOUS_EXAMPLE
            ):
                continue

            coords = testdata.get_hit_coord_for_frame(frame_no)
            data = testdata.get_extracted_data(frame_no)
            if not data:
                continue
            rect = data["frame"]
            x = coords.x - rect.xmin
            y = coords.y - rect.ymin
            norm_x = x / (rect.xmax - rect.xmin)
            norm_y = y / (rect.ymax - rect.ymin)

            counter += 1
            if (counter % 10) == 0:
                validation_writer.writerow(
                    [name, x, y, norm_x, norm_y, rect.xmin, rect.ymin]
                )
            else:
                train_writer.writerow(
                    [name, x, y, norm_x, norm_y, rect.xmin, rect.ymin]
                )

train_csvfile.close()
validation_csvfile.close()
