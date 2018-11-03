"""
Tool for extracting keyframes. Needs opencv highgui/qt5.

Usage: python3 extract_keyframes.py [videofile]

"""

import enum
import os
import subprocess
import sys
import tempfile
import time

import cv2
import numpy as np
import yaml

from ..common.AppData import AppSettings, TestData, VideoData
from ..common.CanvasDetector import CanvasDetector
from ..common.KeyFrame import KeyFrame


class ExtractKeyframes:
    FRAMES_TO_SAMPLE = [-10, -5, -1, 0, 1, 2]
    NUMBER_OF_KALMAN_FILTER_FRAMES_BEFORE_HIT = abs(min(FRAMES_TO_SAMPLE)) + 20
    NUMBER_OF_FRAMES_AFTER_HIT = max(FRAMES_TO_SAMPLE)

    GREEN_COLOR = (0, 255, 0)
    RED_COLOR = (0, 0, 255)
    BLUE_COLOR = (255, 0, 0)
    LIGHT_BLUE_COLOR = (255, 140, 140)

    MIN_MATCH_COUNT = 10

    def __init__(self, path, silent=False):
        self.settings = AppSettings()
        self.videodata = VideoData()
        self.testdata = TestData()

        self.current_target = None
        self.current_frame_number = None

        self.silent = silent
        head, tail = os.path.split(path)
        head, session = os.path.split(head)
        base, ext = tail.split(".")
        if head:
            head += "/"

        self.session_name = session
        self.image_name = base
        self.data_path = head + session + "/" + base + "." + "yaml"
        self.video_path = head + session + "/" + base + "." + ext
        stencil_filename = "canvas-stencil-adj-top-1cm.png"
        self.stencil_path = "hockey/common/{:s}".format(stencil_filename)

    def save_filename(self, folder, keyframe_type, frame_no, found_hit):
        if keyframe_type == KeyFrame.AMBIGUOUS_EXAMPLE:
            return None
        elif found_hit:
            category = "hit"
        else:
            category = "not_hit"

        return "./%s/%s/%s_%s_%d.png" % (
            folder,
            category,
            self.creation_date,
            self.image_name,
            frame_no,
        )

    def quantify(self):
        """Main quantifier for videos."""
        if not self.silent:
            print("Getting video metadata via OpenCV")
        cap = cv2.VideoCapture()
        cap.open(self.video_path, cv2.CAP_FFMPEG)
        if cap is None or not cap.isOpened():
            print("Could not open video {:s}.".format(self.video_path))
            return False

        video_fps = cap.get(cv2.CAP_PROP_FPS)
        video_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        video_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        video_first_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
        video_total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        video_last_frame = video_first_frame + video_total_frames - 1

        if (
            self.videodata.frames_per_second
            and video_fps != self.videodata.frames_per_second
        ):
            print(
                "Frame rate from video (%f) does not match stored "
                "frame rate (%f)." % (video_fps, self.videodata.frames_per_second)
            )
            return False
        else:
            self.videodata.set_frames_per_second(video_fps)

        if (
            self.videodata.first_frame
            and video_first_frame != self.videodata.first_frame
        ):
            print(
                "First frame from video (%d) does not match stored "
                "value (%d)." % (video_first_frame, self.videodata.first_frame)
            )
            return False
        else:
            self.videodata.set_first_frame(video_first_frame)

        if self.videodata.last_frame and video_last_frame != self.videodata.last_frame:
            print(
                "Last frame from video (%d) does not match stored "
                "value (%d)." % (video_last_frame, self.videodata.last_frame)
            )
            quit()
        else:
            self.videodata.set_last_frame(video_last_frame)

        # print("Video information")
        # print("-----------------")
        # print("FPS: {:f}".format(video_fps))
        # print("Relative position: {:f}".format(
        #     cap.get(cv2.CAP_PROP_POS_AVI_RATIO)))
        # print("Total number of frames: {:d}".format(video_total_frames))
        # print("Width {:d} x Height {:d}".format(video_width, video_height))
        # print("")

        self.canvas_detector = CanvasDetector(self.stencil_path, 1 / video_fps)

        if not self.silent:
            cv2.startWindowThread()

        read_frame = True
        fullframe = None
        # current_shot_number = 7
        current_shot_number = 1
        found_hit = False

        while True:
            hf = self.testdata.get_hit_frame_for_shot(current_shot_number)
            if not hf:
                if not self.silent:
                    cv2.destroyWindow("image")
                cap.release()
                return
            if not self.testdata.is_miss_frame(
                hf
            ) and not self.testdata.is_bounce_frame(hf):
                current_hit_frame = hf
                break
            current_shot_number += 1

        cap.set(
            cv2.CAP_PROP_POS_FRAMES,
            current_hit_frame - self.NUMBER_OF_KALMAN_FILTER_FRAMES_BEFORE_HIT - 1,
        )
        read_frame = True

        while True:
            # Escape key pressed? (Must select opencv window first.)
            code = cv2.waitKeyEx(10)
            k = chr(code & 0xFF)
            if k == -1:
                pass
            if k == chr(27) or (
                not self.silent
                and cv2.getWindowProperty("image", cv2.WND_PROP_VISIBLE) < 1
            ):
                # Exit.
                break

            # Read next frame from video.
            if read_frame:
                # Get frame information from video (must do this before
                # cap.read to get zero based frame indexes.
                self.current_frame_number = int(cap.get(cv2.CAP_PROP_POS_FRAMES))

                if not self.silent:
                    cv2.setTrackbarPos(
                        "track1",
                        "image",
                        int(255 * self.current_frame_number / video_last_frame),
                    )
                # read_frame = False
                self.redraw = True
                ret, fullframe_original = cap.read()
                # End of file?
                if ret:
                    if self.videodata.rotation90:
                        fullframe = np.rot90(
                            fullframe_original, -self.videodata.rotation90
                        )
                    else:
                        fullframe = fullframe_original

            if not self.redraw:
                continue
            self.redraw = False

            self.current_frame_number = int(cap.get(cv2.CAP_PROP_POS_FRAMES))

            if (
                self.current_frame_number
                > current_hit_frame + self.NUMBER_OF_FRAMES_AFTER_HIT
            ):
                current_shot_number += 1
                found_hit = False
                # Don't reset the detector for each shot as the canvas position
                # should be fairly stable over time.
                # self.canvas_detector.reset()

                while True:
                    hf = self.testdata.get_hit_frame_for_shot(current_shot_number)
                    if not hf:
                        if not self.silent:
                            cv2.destroyWindow("image")
                        cap.release()
                        return
                    if not self.testdata.is_miss_frame(
                        hf
                    ) and not self.testdata.is_bounce_frame(hf):
                        current_hit_frame = hf
                        break
                    current_shot_number += 1

                # Next shot
                cap.set(
                    cv2.CAP_PROP_POS_FRAMES,
                    current_hit_frame
                    - self.NUMBER_OF_KALMAN_FILTER_FRAMES_BEFORE_HIT
                    - 1,
                )
                # cap.set(cv2.CAP_PROP_POS_FRAMES,
                #         current_hit_frame - NUMBER_OF_FRAMES_BEFORE_HIT - 1)
                read_frame = True
                continue

            # Find canvas.
            goal_corners = self.canvas_detector.find_goal_corners(fullframe)
            if goal_corners is None or goal_corners.size != 8:
                print(
                    "Could not find goal corners in frame {:d}!".format(
                        self.current_frame_number
                    )
                )
                break

            # Should we store keyframe or not?
            skip_frame = True
            # print("Hit frame is {:d}.".format(current_hit_frame))
            for f in self.FRAMES_TO_SAMPLE:
                if self.current_frame_number == (current_hit_frame + f):
                    skip_frame = False
                    break
            if skip_frame:
                # print("Skipping {:d}.".format(self.current_frame_number))
                continue
            # print("Processing {:d}.".format(self.current_frame_number))

            if self.testdata.is_hit_frame(self.current_frame_number):
                found_hit = True

            if not skip_frame:
                self.save_keyframe(
                    fullframe, goal_corners, self.current_frame_number, found_hit
                )

            if self.silent:
                continue

            frame = self.annotate_frame(
                fullframe, goal_corners, self.current_frame_number
            )

            # Show processed image in window.
            cv2.imshow("image", frame)

        cv2.destroyWindow("image")
        cap.release()
        return True

    def annotate_frame(self, fullframe, goal_corners, frame_number):
        # Make a copy we can manipulate
        frame = fullframe.copy()

        # Find shot number (0-based) based on a frame number.
        shot_number = self.testdata.get_shot_number(frame_number)

        # Draw goal.
        cv2.polylines(
            frame,
            [goal_corners],
            True,
            self.RED_COLOR,
            thickness=1,
            lineType=cv2.LINE_AA,
        )

        # Draw markers on hit targets.
        target_coords = self.videodata.get_all_target_pixel_points()
        for t, coords in enumerate(target_coords):
            if coords:
                cv2.circle(frame, coords.as_tuple(), 3, self.BLUE_COLOR, 2)
                cv2.putText(
                    frame,
                    "%d" % (t + 1),
                    (coords.x + 3, coords.y - 5),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.3,
                    self.BLUE_COLOR,
                    1,
                )

        # Draw marker on current target.
        current_target = self.videodata.get_target_for_shot(shot_number)
        if current_target is not None:
            target_coords = self.videodata.get_pixel_point_for_target(current_target)
            if target_coords:
                cv2.circle(frame, target_coords.as_tuple(), 15, self.GREEN_COLOR, 1)

        kf_type = self.testdata.get_keyframe_type(frame_number)
        if kf_type is KeyFrame.NOT_KEYFRAME:
            cv2.displayOverlay("image", None)
        elif kf_type is KeyFrame.HIT_EXAMPLE:
            cv2.displayOverlay("image", "Hit example")
        elif kf_type is KeyFrame.NOT_HIT_EXAMPLE:
            cv2.displayOverlay("image", "Not hit example")
        elif kf_type is KeyFrame.AMBIGUOUS_EXAMPLE:
            cv2.displayOverlay("image", "Ambiguous example")
        else:
            cv2.displayOverlay("image", "???")

        # Draw marker on hit coordinates if this is a hit frame
        if self.testdata.is_hit_frame(frame_number):
            hit_coord = self.testdata.get_hit_coord_for_frame(frame_number)

            if self.testdata.is_bounce_frame(frame_number):
                cv2.putText(
                    frame,
                    "b",
                    (hit_coord.x + 15, hit_coord.y + 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.2,
                    self.RED_COLOR,
                    2,
                )
            if self.testdata.is_miss_frame(frame_number):
                # Draw X.
                cv2.line(
                    frame,
                    (hit_coord.x - 10, hit_coord.y - 10),
                    (hit_coord.x + 10, hit_coord.y + 10),
                    self.RED_COLOR,
                    2,
                )
                cv2.line(
                    frame,
                    (hit_coord.x - 10, hit_coord.y + 10),
                    (hit_coord.x + 10, hit_coord.y - 10),
                    self.RED_COLOR,
                    2,
                )
            else:
                # Draw O.
                cv2.circle(frame, hit_coord.as_tuple(), 3, self.RED_COLOR, 2)

        # Draw crop markers.
        # (ul, lr) = self.videodata.get_crop_coords()
        # If ul != None and lr != None:
        #     cv2.rectangle(frame,
        #                   ul.as_tuple(),
        #                   lr.as_tuple(),
        #                   self.GREEN_COLOR,
        #                   1,
        #                   lineType = cv2.LINE_8,
        #                   shift = 0)
        # elif ul != None:
        #     cv2.circle(frame, ul.as_tuple(), 1, self.GREEN_COLOR, 1)
        # elif lr != None:
        #     cv2.circle(frame, lr.as_tuple(), 1, self.GREEN_COLOR, 1)

        cv2.putText(
            frame,
            str(frame_number),
            (5, 45),
            cv2.FONT_HERSHEY_SIMPLEX,
            2,
            self.GREEN_COLOR,
            2,
        )
        return frame

    def save_keyframe(self, frame, goal_corners, frame_number, found_hit):
        # Expand goal corners a little fade out region.
        goal_exp = np.array(
            [
                [goal_corners[0][0] - 5, goal_corners[0][1] - 5],
                [goal_corners[1][0] - 5, goal_corners[1][1] + 5],
                [goal_corners[2][0] + 5, goal_corners[2][1] + 5],
                [goal_corners[3][0] + 5, goal_corners[3][1] - 5],
            ],
            dtype=np.int32,
        )

        (rows, cols, n) = frame.shape
        maskframe = np.zeros((rows, cols, n), np.uint8)
        maskframe[:] = (255, 255, 255)
        maskframe = cv2.fillPoly(maskframe, [goal_exp], (0, 0, 0))
        # maskframe = cv2.GaussianBlur(maskframe, (21, 21), 10)
        maskframe = cv2.blur(maskframe, (11, 11))
        outframe = cv2.add(frame, maskframe)

        xmin = min(goal_exp[0][0], goal_exp[1][0])
        xmax = max(goal_exp[2][0], goal_exp[3][0])
        ymin = min(goal_exp[0][1], goal_exp[3][1])
        ymax = max(goal_exp[1][1], goal_exp[2][1])
        outframe = outframe[ymin:ymax, xmin:xmax]

        # b, g, r = cv2.split(outframe)
        # gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        # edges = cv2.Canny(r, 10, 20)
        # cv2.imshow('out', edges)

        kf_type = self.testdata.get_keyframe_type(frame_number)
        savename = self.save_filename("dataset", kf_type, frame_number, found_hit)
        if savename:
            # cv2.IMWRITE_JPEG_QUALITY, 80,
            # PNG is always lossless so compression 0-9 is just
            # a trade-off between speed and file size. 1 is fast.
            params = (cv2.IMWRITE_PNG_COMPRESSION, 1)
            cv2.imwrite(savename, outframe, params)

    def setup(self):
        """Setup settings, videodata and testdata."""
        # Get video file creation time
        creation_date_b = subprocess.check_output(
            ["exiftool", self.video_path, "-CreateDate", "-T", "-d", "%Y%m%d"]
        )
        self.creation_date = creation_date_b.decode("utf-8").strip()

        if not self.silent:
            print("Reading videodata from {0}".format(self.data_path))
        try:
            stream = open(self.data_path, "r")
            data = yaml.load(stream)
        except FileNotFoundError:
            print("Videodata not found. Using defaults.")
            data = []

        if "app_settings" in data:
            self.settings = AppSettings(data["app_settings"])

        if "video_data" in data:
            self.videodata = VideoData(data["video_data"])

        if "test_data" in data:
            self.testdata = TestData(data["test_data"])

        if not self.silent:
            print("done")
        self.dirty_flag = False

        if not self.silent:
            print("Getting metadata from movie file.")
        rotation = subprocess.check_output(
            [
                "ffprobe",
                "-loglevel",
                "error",
                "-select_streams",
                "v:0",
                "-show_entries",
                "stream_tags=rotate",
                "-of",
                "default=nw=1:nk=1",
                self.video_path,
            ]
        )
        if rotation:
            rotation90 = VideoData.rotation_to_rotation90(int(rotation))
            if self.videodata.rotation90 and rotation90 != self.videodata.rotation90:
                print(
                    "Rotation from video (%d) does not match stored "
                    "rotation (%d)." % (rotation90, self.videodata.rotation90)
                )
                return False
            self.videodata.set_rotation90(rotation90)
        if not self.silent:
            print("done")

        # Setup output window.
        if not self.silent:
            cv2.namedWindow(
                "image",
                cv2.WINDOW_NORMAL | cv2.WINDOW_GUI_EXPANDED | cv2.WINDOW_KEEPRATIO,
            )
            cv2.moveWindow("image", 0, 0)
            cv2.resizeWindow("image", 1440, 1024)
        return True


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: %s [videofile]" % sys.argv[0])
        sys.exit(0)

    ex = ExtractKeyframes(sys.argv[1], silent=False)
    if not ex.setup():
        sys.exit(-1)
    ex.quantify()
