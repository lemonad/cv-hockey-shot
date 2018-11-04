from enum import Enum
import os
import re
import sys

import cv2
import numpy as np

class FrameType(Enum):
    HIT = 1
    NOT_HIT = 2
    MAYBE = 3
    BOUNCE_HIT = 4

def out_filename(folder, frame_type, base, frame_no):
    if frame_type == FrameType.HIT:
        category = 'hit'
    else:
        category = 'not_hit'
    return './%s/%s/%s_%d.png' % (folder, category, base, frame_no)

if len(sys.argv) <= 1:
    print("Usage: %s [videofile1 videofile2 …]" % sys.argv[0])
    sys.exit(0)


cv2.namedWindow('out', cv2.WINDOW_AUTOSIZE)

filenames = []
for i in range(1, len(sys.argv)):
    filenames.append(sys.argv[i])

for filename in filenames:
    print("file: %s" % filename)
    rotate_flag = False
    crop = None
    start_frame = None
    end_frame = None
    num_frames = 0
    frame_type = None

    head, tail = os.path.split(filename)
    base, ext = tail.split('.')
    if head:
        head += "/"
    data_filename = head + base + '.frames'
    video_filename = head + base + '.' + ext

    print("Reading videodata from {0}".format(data_filename))
    try:
        with open(data_filename) as df:
            lines = df.readlines()
    except FileNotFoundError:
        print("No associated frames file found: %s" % data_filename)
        lines = []
        continue

    # Input video.
    cap = cv2.VideoCapture(video_filename)
    if cap is None or not cap.isOpened():
        print("Could not open video {:s}.".format(video_filename))
        break

    video_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    video_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    print("Video information")
    print("-----------------")
    print("FPS: {:f}".format(fps))
    print("Relative position: {:f}".format(
        cap.get(cv2.CAP_PROP_POS_AVI_RATIO)))
    print("Width {:d} x Height {:d}".format(video_width, video_height))
    print("")

    for line in lines:
        comment_index = line.find('#')
        if comment_index >= 0:
            line = line[:comment_index]

        line = line.strip()

        if not line:
            continue

        m_crop = re.match('^Crop\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)$', line)
        m_frames = re.match('^(\d+)-*(\d+|) ([XH\?])$', line)
        if m_crop:
            crop = [int(m_crop[1]), int(m_crop[2]), int(m_crop[3]),
                    int(m_crop[4])]
            continue
        elif m_frames:
            start_frame = int(m_frames[1])
            try:
                end_frame = int(m_frames[2])
            except ValueError:
                end_frame = start_frame

            if m_frames[3] == 'X':
                frame_type = FrameType.NOT_HIT
            elif m_frames[3] == 'H':
                frame_type = FrameType.HIT
            elif m_frames[3] == '?':
                # frame_type = FrameType.MAYBE
                continue
            else:
                print("Error: Unknown frame type '%c'." % m_frames[3])

        # Fast forward to start frame.
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame - 1)

        for fno in range(start_frame, end_frame + 1):
            ret, fullframe = cap.read()
            if not ret:
                print("Error: Premature end of file!")
                break

            # Rotate video if necessary.
            if rotate_flag:
                fullframe = np.rot90(fullframe, -1)

            frame = fullframe[crop[1]:crop[3], crop[0]:crop[2]]
            b, g, r = cv2.split(frame)
            # gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            edges = cv2.Canny(r, 10, 20)
            # cv2.imshow('out', edges)

            outname = out_filename('dataset', frame_type, base, fno)
            params = (cv2.IMWRITE_JPEG_QUALITY, 80,
                      cv2.IMWRITE_PNG_COMPRESSION, 8)
            cv2.imwrite(outname, edges, params)

    cap.release()

cv2.destroyAllWindows()
