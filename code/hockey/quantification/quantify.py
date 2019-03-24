"""
Tool to quantify videos. Needs opencv highgui/qt5.

Usage: python3 quantify.py [videofile]


Press keys
    1-5  mark targets
    spc  jump 1 second forward
    j    jump to next shot
    k    jump to previous shot
    h    jump 0.25 seconds forward
    l    jump 0.25 seconds backward
    m    next frame
    n    previous frame
    esc  exit and save data to new file

Use control panel to add hit points. If on a hit frame,
then button removes the current hit point.

"""

import enum
import os
import subprocess
import sys
import tempfile
import time

import cv2
# from imutils.video import FPS
import numpy as np
import yaml

from ..common.AppData import (AppSettings, TestData, VideoData)
from ..common.CanvasDetector import CanvasDetector
from ..common.Dimension import Dimension
from ..common.KeyFrame import KeyFrame
from ..common.Point import Point


class Quantify:

    @enum.unique
    class MarkState(enum.Enum):
        NONE = 1
        TARGET = 2
        HIT = 3
        UPPER_LEFT_CROP = 4
        LOWER_RIGHT_CROP = 5

    GREEN_COLOR = (0, 255, 0)
    RED_COLOR = (0, 0, 255)
    BLUE_COLOR = (255, 0, 0)
    LIGHT_BLUE_COLOR = (255, 140, 140)

    stencil_filename = 'hockey/common/canvas-stencil-adj-top-1cm.png'
    MIN_MATCH_COUNT = 10

    settings = AppSettings()
    videodata = VideoData()
    testdata = TestData()

    mark_state = MarkState.NONE
    current_goal_corners = None
    current_target = None
    current_frame_number = None
    dirty_flag = False
    redraw = True
    draw_homography = False
    show_canny = False

    def __init__(self):
        pass

    def update_status_bar(self, current_frame_number, current_shot_number):
        """Use the status bar to display information."""
        fps = self.videodata.frames_per_second

        status_str = "Shot %d: Frame %d (%.1fs). " % (current_shot_number + 1,
                                                      current_frame_number,
                                                      current_frame_number / fps)
        surrounding = \
            self.testdata.get_surrounding_hit_frames(current_frame_number)
        if surrounding[0] and surrounding[2]:
            status_str += "Hits: previous %d (%.1fs), current %d (%.1fs), next %d (%.1fs)" % (
                surrounding[0], surrounding[0] / fps,
                surrounding[1], surrounding[1] / fps,
                surrounding[2], surrounding[2] / fps)
        elif surrounding[0]:
            status_str += "Hits: previous %d (%.1fs), current %d (%.1fs)" % (
                surrounding[0], surrounding[0] / fps,
                surrounding[1], surrounding[1] / fps)
        elif surrounding[2]:
            status_str += "Hits: current %d (%.1fs), next %d (%.1fs)" % (
                surrounding[1], surrounding[1] / fps,
                surrounding[2], surrounding[2] / fps)
        elif surrounding[1]:
            status_str += "Hits: current %d (%.1fs)" % (
                surrounding[1], surrounding[1] / fps)
        else:
            status_str += "No hits recorded yet."
        cv2.displayStatusBar("image", status_str, 0)

    def click_target(self, event, x, y, flags, param):
        """Handler for setting target / hit coordinates."""
        if event == cv2.EVENT_LBUTTONDOWN:
            if (self.mark_state == self.MarkState.TARGET and
                    self.current_target != None):
                self.videodata.set_pixel_point_for_target(self.current_target,
                                                          Point(x, y))
                self.current_target = None
                self.mark_state = self.MarkState.NONE
                self.dirty_flag = True
                self.redraw = True
            elif self.mark_state == self.MarkState.HIT:
                self.dirty_flag = True
                self.redraw = True
                # if self.testdata.get_number_of_hit_frames() == 0:
                #     fps = self.videodata.frames_per_second
                #     last_frame = self.videodata.last_frame

                #     for f in range(self.current_frame_number,
                #                    # We can't usually reach the last frames
                #                    # so subtract some reasonable number.
                #                    int(last_frame - fps),
                #                    int(6 * fps)):
                #         self.testdata.add_hit_point(f, Point(x, y))
                # else:
                self.testdata.add_hit_point(self.current_frame_number,
                                            Point(x, y))
                self.videodata.set_number_of_shots(
                    self.testdata.get_number_of_hit_frames())
                self.mark_state = self.MarkState.NONE
            elif self.mark_state == self.MarkState.UPPER_LEFT_CROP:
                self.dirty_flag = True
                self.redraw = True
                self.videodata.set_upper_left_crop(Point(x, y))
                self.mark_state = self.MarkState.NONE
            elif self.mark_state == self.MarkState.LOWER_RIGHT_CROP:
                self.dirty_flag = True
                self.redraw = True
                self.videodata.set_lower_right_crop(Point(x, y))
                self.mark_state = self.MarkState.NONE

    def trackbar_changed(self, value):
        """Called when trackbar is moved."""
        pass

    def mark_hit_pressed(self, state, userdata):
        """Called when mark hit button is pressed."""
        if self.testdata.is_hit_frame(self.current_frame_number):
            self.testdata.remove_hit_point(self.current_frame_number)
            self.videodata.set_number_of_shots(
                self.testdata.get_number_of_hit_frames())
            self.dirty_flag = True
            self.redraw = True
        else:
            self.mark_state = self.MarkState.HIT

    def toggle_miss_pressed(self, state, userdata):
        """Called when toggle miss button is pressed."""
        if self.testdata.is_hit_frame(self.current_frame_number):
            self.testdata.toggle_miss(self.current_frame_number)
            self.dirty_flag = True
            self.redraw = True

    def toggle_bounce_pressed(self, state, userdata):
        """Called when toggle bounce button is pressed."""
        if self.testdata.is_hit_frame(self.current_frame_number):
            self.testdata.toggle_bounce(self.current_frame_number)
            self.dirty_flag = True
            self.redraw = True

    def accept_goal_corners_pressed(self, state, userdata):
        """Called when the accept goal corners button is pressed."""
        if self.current_goal_corners.size == 8:
            self.videodata.set_goal_corners([
                Point(self.current_goal_corners[0, 0, 0],
                      self.current_goal_corners[0, 0, 1]),
                Point(self.current_goal_corners[1, 0, 0],
                      self.current_goal_corners[1, 0, 1]),
                Point(self.current_goal_corners[2, 0, 0],
                      self.current_goal_corners[2, 0, 1]),
                Point(self.current_goal_corners[3, 0, 0],
                      self.current_goal_corners[3, 0, 1])
                ])
            self.dirty_flag = True
            self.redraw = True

    def upper_left_crop_button(self, state, userdata):
        self.mark_state = self.MarkState.UPPER_LEFT_CROP

    def bottom_right_crop_button(self, state, userdata):
        self.mark_state = self.MarkState.LOWER_RIGHT_CROP

    def toggle_homography_button(self, state, userdata):
        self.draw_homography = state
        self.redraw = True

    def toggle_canny_button(self, state, userdata):
        self.show_canny = state
        self.redraw = True

    def move_hit_button(self, state, direction):
        if not self.testdata.is_hit_frame(self.current_frame_number):
            return

        hit_coord = \
            self.testdata.get_hit_coord_for_frame(self.current_frame_number)
        x = hit_coord.x
        y = hit_coord.y

        if direction == 0:  # left
            x -= 1
        elif direction == 1:  # up
            y -= 1
        elif direction == 2:  # down
            y += 1
        else:  # right
            x += 1

        self.testdata.add_hit_point(self.current_frame_number, Point(x, y))
        self.dirty_flag = True
        self.redraw = True

    def is_keyframe_button(self, state, keyframe_type):
        if keyframe_type not in KeyFrame:
            print("Error: Keyframe button hit but invalid keyframe!")
            return
        self.testdata.set_keyframe(self.current_frame_number, keyframe_type)
        self.dirty_flag = True
        self.redraw = True

    def find_canvas(self, fullframe):
        gray_fullframe = cv2.cvtColor(fullframe, cv2.COLOR_RGB2GRAY)

        # find the image keypoints and descriptors with SIFT
        kp2, des2 = self.sift_frame.detectAndCompute(gray_fullframe, None)

        FLANN_INDEX_KDTREE = 0
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=50)

        flann = cv2.FlannBasedMatcher(index_params, search_params)

        matches = flann.knnMatch(self.stencil_descriptors, des2, k=2)

        # store all the good matches as per Lowe's ratio test.
        good = []
        for m, n in matches:
            if m.distance < (0.8 * n.distance):
                good.append(m)

        if len(good) > self.MIN_MATCH_COUNT:
            src_pts = np.float32(
                    [self.stencil_keypoints[m.queryIdx].pt for m in good]
                ).reshape(-1, 1, 2)
            dst_pts = np.float32(
                    [kp2[m.trainIdx].pt for m in good]
                ).reshape(-1, 1, 2)

            M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
            print(M)
            matchesMask = mask.ravel().tolist()

            h, w = self.stencil_shape
            h_pixels_per_mm = h / 1440
            w_pixels_per_mm = w / 2499
            top_offset = 171 * h_pixels_per_mm
            bottom_offset = 50 * h_pixels_per_mm
            left_offset = 331 * w_pixels_per_mm
            right_offset = 338 * w_pixels_per_mm

            pts = np.float32([[left_offset, top_offset],
                              [left_offset, h-1-bottom_offset],
                              [w-1-right_offset, h-1-bottom_offset],
                              [w-1-right_offset, top_offset]]).\
                reshape(-1, 1, 2)
            dst = None
            try:
                dst = cv2.perspectiveTransform(pts, M)
            except:
                return None
            else:
                return np.int32(dst)
        else:
            print("Not enough matches are found - %d/%d" % (
                len(good), MIN_MATCH_COUNT))
            return None

    def quantify(self, video_filename):
        """Main quantifier for videos."""
        print("Getting video metadata via OpenCV")
        cap = cv2.VideoCapture()
        cap.open(video_filename, cv2.CAP_FFMPEG)
        if cap is None or not cap.isOpened():
            print("Could not open video {:s}.".format(video_filename))
            return False

        video_fps = cap.get(cv2.CAP_PROP_FPS)
        video_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        video_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        video_first_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
        video_total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        video_last_frame = video_first_frame + video_total_frames - 1

        if (self.videodata.frames_per_second and
                video_fps != self.videodata.frames_per_second):
            print("Frame rate from video (%f) does not match stored "
                  "frame rate (%f)." % (video_fps,
                                        self.videodata.frames_per_second))
            return False
        else:
            self.videodata.set_frames_per_second(video_fps)

        if (self.videodata.first_frame and
                video_first_frame != self.videodata.first_frame):
            print("First frame from video (%d) does not match stored "
                  "value (%d)." % (video_first_frame,
                                   self.videodata.first_frame))
            return False
        else:
            self.videodata.set_first_frame(video_first_frame)

        if (self.videodata.last_frame and
                video_last_frame != self.videodata.last_frame):
            print("Last frame from video (%d) does not match stored "
                  "value (%d)." % (video_last_frame,
                                   self.videodata.last_frame))
            quit()
        else:
            self.videodata.set_last_frame(video_last_frame)
        print("done")

        # print("Video information")
        # print("-----------------")
        # print("FPS: {:f}".format(video_fps))
        # print("Relative position: {:f}".format(
        #     cap.get(cv2.CAP_PROP_POS_AVI_RATIO)))
        # print("Total number of frames: {:d}".format(video_total_frames))
        # print("Width {:d} x Height {:d}".format(video_width, video_height))
        # print("")

        cv2.setMouseCallback("image", self.click_target)
        cv2.startWindowThread()

        # Initiate SIFT detectors
        self.sift_frame = cv2.xfeatures2d.SIFT_create()
        # self.sift_frame = cv2.xfeatures2d.SIFT_create(
        #         nfeatures = 0,
        #         nOctaveLayers = 3,
        #         contrastThreshold = 0.04,
        #         edgeThreshold = 10,
        #         sigma = 1.6
        #         )

        # Stencil
        stencil_image = cv2.imread(self.stencil_filename)
        stencil_gray = cv2.cvtColor(stencil_image, cv2.COLOR_RGB2GRAY)
        self.stencil_shape = stencil_gray.shape
        sift_stencil = cv2.xfeatures2d.SIFT_create()
        self.stencil_keypoints, self.stencil_descriptors = \
                sift_stencil.detectAndCompute(stencil_gray, None)

        read_frame = True
        fullframe = None
        current_shot_number = 1
        self.current_goal_corners = None

        while True:
            # Escape key pressed? (Must select opencv window first.)
            code = cv2.waitKeyEx(10)
            k = chr(code & 0xff)
            if k == -1:
                pass
            if (k == chr(27) or
                    cv2.getWindowProperty('image', cv2.WND_PROP_VISIBLE) < 1):
                # Exit.
                break
            elif k == '1' or k == '2' or k == '3' or k == '4' or k == '5':
                # Mark target positions.
                num_k = ord(k) - ord('1') + 1
                if self.mark_state != self.MarkState.NONE:
                    self.current_target = None
                    self.mark_state = self.MarkState.NONE
                    cv2.displayOverlay("image", None);
                else:
                    print("Setting index", num_k)
                    self.current_target = num_k
                    self.mark_state = self.MarkState.TARGET
                    cv2.displayOverlay("image",
                                       "Mark target %d" % num_k,
                                       2000);
            elif k == 'h':
                # Reverse (equivalent to vim move left)
                # cap.set(cv2.CAP_PROP_POS_FRAMES,
                #         max(0, self.current_frame_number - 32))
                cap.set(cv2.CAP_PROP_POS_FRAMES,
                        min(self.videodata.last_frame,
                            self.current_frame_number -
                            int(0.25 * self.videodata.frames_per_second) - 2))
                read_frame = True
            elif k == 'l':
                # Fast forward (equivalent to vim move right)
                # cap.set(cv2.CAP_PROP_POS_FRAMES,
                #         min(self.videodata.last_frame,
                #             self.current_frame_number + 30))
                cap.set(cv2.CAP_PROP_POS_FRAMES,
                        min(self.videodata.last_frame,
                            self.current_frame_number +
                            int(0.25 * self.videodata.frames_per_second)))
                read_frame = True
            elif k == ' ':
                # Jump a second forward.
                cap.set(cv2.CAP_PROP_POS_FRAMES,
                        min(self.videodata.last_frame,
                            self.current_frame_number +
                            int(0.5 * self.videodata.frames_per_second)))
                read_frame = True
            elif k == 'n':
                # One frame backwards.
                cap.set(cv2.CAP_PROP_POS_FRAMES,
                        max(0, self.current_frame_number - 2))
                read_frame = True
            elif k == 'm':
                # One frame forward.
                read_frame = True
            elif k == 'k':
                # Previous shot (equivalent to vim move to previous line)
                hf = self.testdata.get_hit_frame_for_shot(
                         max(0, current_shot_number - 1))
                if hf:
                    cap.set(cv2.CAP_PROP_POS_FRAMES, hf - 1)
                    read_frame = True
            elif k == 'j':
                # Next shot (equivalent to vim move to next line)
                hf = self.testdata.get_hit_frame_for_shot(
                         min(self.videodata.number_of_shots - 1,
                             current_shot_number))
                if hf and hf <= self.current_frame_number:
                    hf = self.testdata.get_hit_frame_for_shot(
                             min(self.videodata.number_of_shots - 1,
                                 current_shot_number + 1))
                if hf:
                    cap.set(cv2.CAP_PROP_POS_FRAMES, hf - 1)
                    read_frame = True

            # Read next frame from video.
            if read_frame:
                # Get frame information from video (must do this before
                # cap.read to get zero based frame indexes.
                self.current_frame_number = int(cap.get(cv2.CAP_PROP_POS_FRAMES))

                cv2.setTrackbarPos("track1", "image",
                                   int(255 * self.current_frame_number /
                                       video_last_frame))
                read_frame = False
                self.redraw = True
                ret, fullframe_original = cap.read()
                # End of file?
                if ret:
                    if self.videodata.rotation90:
                        fullframe = np.rot90(fullframe_original,
                                             -self.videodata.rotation90)
                    else:
                        fullframe = fullframe_original

            if not self.redraw:
                continue
            self.redraw = False

            self.current_frame_number = int(cap.get(cv2.CAP_PROP_POS_FRAMES))

            # Find shot number (0-based) based on a frame number.
            current_shot_number = \
                self.testdata.get_shot_number(self.current_frame_number)

            # Set status bar string
            self.update_status_bar(self.current_frame_number,
                                   current_shot_number)
            # Make a copy we can manipulate
            frame = fullframe.copy()

            # Canny?
            if self.show_canny:
                # frame = cv2.cvtColor(cv2.Canny(frame, 20, 20),
                frame = cv2.cvtColor(cv2.Canny(frame, 50, 100),
                        cv2.COLOR_GRAY2RGB)

            # Draw inner goal.
            (ul, ur, lr, ll) = self.videodata.get_goal_corner_coords()
            if ul != None and ur != None and lr != None and ll != None:
                pts = np.array([ul.as_tuple(),
                                ur.as_tuple(),
                                lr.as_tuple(),
                                ll.as_tuple()], np.int32)
                pts = pts.reshape((-1,1,2))
                cv2.polylines(frame,
                              [pts],
                              True,
                              self.GREEN_COLOR,
                              thickness=1,
                              lineType = cv2.LINE_AA,
                              shift=0)

            # Find canvas.
            if self.draw_homography:
                goal_pts = self.canvas_detector.find_goal_corners(
                        fullframe, optional_frame_number=self.current_frame_number)
                # goal_pts = self.find_canvas(fullframe)
                if goal_pts is not None and goal_pts.size == 8:
                    self.current_goal_corners = goal_pts
                    cv2.polylines(frame, [goal_pts], True, (255, 0, 0),
                                  thickness=1, lineType=cv2.LINE_AA)
                    # midx = goal_pts[0][0] + (goal_pts[3][0] - goal_pts[0][0]) // 2
                    # midy = goal_pts[0][1] + (goal_pts[1][1] - goal_pts[0][1]) // 2
                    # print(midx, midy)
                    # cv2.floodFill(frame,
                    #               None,
                    #               (midx,midy),
                    #               (255, 255, 255),
                    #               loDiff=(94,94,94),
                    #               upDiff=(255,255,255),
                    #               flags=8 | cv2.FLOODFILL_FIXED_RANGE)
                    (grey, ul) = self.extract_keyframe(fullframe, goal_pts)
                    if grey is not None:
                        grey = cv2.equalizeHist(grey)
                        cv2.imshow('hello', grey)
                        # Setup SimpleBlobDetector parameters.
                        params = cv2.SimpleBlobDetector_Params()

                        # Change thresholds
                        params.minThreshold = 0
                        params.maxThreshold = 50

                        # Filter by Area.
                        params.filterByArea = True
                        params.minArea = 150
                        params.maxArea = 300

                        # Find dark blobs.
                        params.filterByColor = True
                        params.blobColor = 0

                        # Filter by Circularity
                        params.filterByCircularity = False
                        # params.minCircularity = 0.1

                        # Filter by Convexity
                        params.filterByConvexity = True
                        params.minConvexity = 0.5

                        # Filter by Inertia
                        params.filterByInertia = False
                        # params.minInertiaRatio = 0.01

                        # Create a detector with the parameters
                        detector = cv2.SimpleBlobDetector_create(params)
                        keypoints = detector.detect(grey) # + np.array((100,100))
                        for kp in keypoints:
                            kp.pt = (kp.pt[0] + ul[0], kp.pt[1] + ul[1])
                        frame = cv2.drawKeypoints(
                                frame,
                                keypoints,
                                np.array([]),
                                (0,0,255),
                                cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
                else:
                    self.current_goal_corners = None

            # Draw markers on hit targets.
            target_coords = self.videodata.get_all_target_pixel_points()
            for t, coords in enumerate(target_coords):
                if coords:
                    cv2.circle(frame,
                               coords.as_tuple(),
                               3, self.BLUE_COLOR, 2)
                    cv2.putText(frame,
                                "%d" % (t + 1),
                                (coords.x + 3, coords.y - 5),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.3,
                                self.BLUE_COLOR, 1)

            # Draw inner goal posts.
            # target_offsets_in_cm = self.videodata.get_all_target_offsets_in_cm()
            # tc_list = []
            # tc_list_in_cm = []
            # for coords in target_coords:
            #     if coords:
            #         tc_list.append(coords.as_tuple())
            # for coords in target_offsets_in_cm:
            #     if coords:
            #         tc_list_in_cm.append(coords.as_tuple())

            # if len(tc_list) == 5 and len(tc_list_in_cm) == 5:
            #     goal_ul = pointBaseChange(
            #         (0, 0),
            #         tc_list_in_cm,
            #         tc_list)
            #     goal_ur = pointBaseChange(
            #         (self.videodata.goal_inner_dimensions_in_cm.width, 0),
            #         tc_list_in_cm,
            #         tc_list)
            #     goal_lr = pointBaseChange(
            #         (self.videodata.goal_inner_dimensions_in_cm.width,
            #          self.videodata.goal_inner_dimensions_in_cm.height),
            #         tc_list_in_cm,
            #         tc_list)
            #     goal_ll = pointBaseChange(
            #         (0, self.videodata.goal_inner_dimensions_in_cm.height),
            #         tc_list_in_cm,
            #         tc_list)
            #     points = np.array([[goal_ul[0], goal_ul[1]],
            #                        [goal_ur[0], goal_ur[1]],
            #                        [goal_lr[0], goal_lr[1]],
            #                        [goal_ll[0], goal_ll[1]]],
            #                       dtype=np.int32)
            #     cv2.polylines(frame, [points], 1, self.RED_COLOR, 3)

            # Draw marker on current target.
            current_target = \
                self.videodata.get_target_for_shot(current_shot_number)
            if current_target is not None:
                target_coords = \
                    self.videodata.get_pixel_point_for_target(current_target)
                if target_coords:
                    cv2.circle(frame,
                               target_coords.as_tuple(),
                               15, self.GREEN_COLOR, 1)

            kf_type = self.testdata.get_keyframe_type(self.current_frame_number)
            if kf_type is KeyFrame.NOT_KEYFRAME:
                cv2.displayOverlay('image', None)
            elif kf_type is KeyFrame.HIT_EXAMPLE:
                cv2.displayOverlay('image', "Hit example")
            elif kf_type is KeyFrame.NOT_HIT_EXAMPLE:
                cv2.displayOverlay('image', "Not hit example")
            elif kf_type is KeyFrame.AMBIGUOUS_EXAMPLE:
                cv2.displayOverlay('image', "Ambiguous example")
            else:
                cv2.displayOverlay('image', "???")

            # Draw marker on hit coordinates if this is a hit frame
            if self.testdata.is_hit_frame(self.current_frame_number):
                hit_coord = \
                    self.testdata.get_hit_coord_for_frame(self.current_frame_number)

                if self.testdata.is_bounce_frame(self.current_frame_number):
                    cv2.putText(frame,
                                "b",
                                (hit_coord.x + 15, hit_coord.y + 10),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                1.2,
                                self.RED_COLOR, 2)
                if self.testdata.is_miss_frame(self.current_frame_number):
                    # Draw X.
                    cv2.line(frame,
                             (hit_coord.x - 10, hit_coord.y - 10),
                             (hit_coord.x + 10, hit_coord.y + 10),
                             self.RED_COLOR, 2)
                    cv2.line(frame,
                             (hit_coord.x - 10, hit_coord.y + 10),
                             (hit_coord.x + 10, hit_coord.y - 10),
                             self.RED_COLOR, 2)
                else:
                    # Draw O.
                    cv2.circle(frame,
                               hit_coord.as_tuple(),
                               3, self.RED_COLOR, 2)



            # Draw crop markers.
            (ul, lr) = self.videodata.get_crop_coords()
            if ul != None and lr != None:
                cv2.rectangle(frame,
                              ul.as_tuple(),
                              lr.as_tuple(),
                              self.GREEN_COLOR,
                              1,
                              lineType = cv2.LINE_8,
                              shift = 0)
            elif ul != None:
                cv2.circle(frame, ul.as_tuple(), 1, self.GREEN_COLOR, 1)
            elif lr != None:
                cv2.circle(frame, lr.as_tuple(), 1, self.GREEN_COLOR, 1)

            # Show processed image in window.
            cv2.imshow("image", frame);

        cv2.destroyWindow('image')
        cap.release()
        return True

    def setup(self, video_filename, data_filename):
        """Setup settings, videodata and testdata."""
        print("Reading videodata from {0}".format(data_filename))
        try:
            stream = open(data_filename, "r")
            data = yaml.load(stream)
        except FileNotFoundError:
            print("Not found. Using defaults.")
            data = []

        if 'app_settings' in data:
            self.settings = AppSettings(data['app_settings'])

        if 'video_data' in data:
            self.videodata = VideoData(data['video_data'])

        if 'test_data' in data:
            self.testdata = TestData(data['test_data'])

        print("done")
        self.dirty_flag = False

        print("Getting metadata from movie file.")
        rotation = subprocess.check_output(["ffprobe",
                                            "-loglevel", "error",
                                            "-select_streams", "v:0",
                                            "-show_entries", "stream_tags=rotate",
                                            "-of", "default=nw=1:nk=1",
                                            video_filename])
        if rotation:
            rotation90 = VideoData.rotation_to_rotation90(int(rotation))
            if (self.videodata.rotation90 and
                    rotation90 != self.videodata.rotation90):
                print("Rotation from video (%d) does not match stored "
                      "rotation (%d)." % (rotation90,
                                          self.videodata.rotation90))
                return False
            self.videodata.set_rotation90(rotation90)
        print("done")

        self.canvas_detector = CanvasDetector(self.stencil_filename)

        # Setup output window.
        cv2.namedWindow("image", cv2.WINDOW_NORMAL |
                                 cv2.WINDOW_GUI_EXPANDED |
                                 cv2.WINDOW_KEEPRATIO)
        cv2.moveWindow('image', 0, 0)
        cv2.resizeWindow('image', 1440, 1024)
        cv2.createTrackbar("track1", "image", 0, 255, self.trackbar_changed)
        cv2.displayOverlay("image",
                           "Press 1-5 and click to set target position",
                           4000);

        cv2.createButton("Crop (top-left)", self.upper_left_crop_button, 0,
                         cv2.QT_PUSH_BUTTON, False)
        cv2.createButton("Crop (bottom-right)", self.bottom_right_crop_button,
                         0, cv2.QT_PUSH_BUTTON, False)
        cv2.createButton("Accept goal corners",
                         self.accept_goal_corners_pressed, 0,
                         cv2.QT_PUSH_BUTTON, False)
        cv2.createButton("Canny ", self.toggle_canny_button, 0,
                         cv2.QT_CHECKBOX, False)
        cv2.createButton("Homography ", self.toggle_homography_button,
                         0, cv2.QT_CHECKBOX, False)

        cv2.createButton("⚫️ Mark hit", self.mark_hit_pressed, 0,
                         cv2.QT_PUSH_BUTTON | cv2.QT_NEW_BUTTONBAR, False)
        cv2.createButton("🚫 Miss", self.toggle_miss_pressed, 0,
                         cv2.QT_PUSH_BUTTON, False)
        cv2.createButton("➰ Bounce", self.toggle_bounce_pressed, 0,
                         cv2.QT_PUSH_BUTTON, False)
        cv2.createButton("←", self.move_hit_button, 0, cv2.QT_PUSH_BUTTON,
                         False)
        cv2.createButton("↓", self.move_hit_button, 2, cv2.QT_PUSH_BUTTON,
                         False)
        cv2.createButton("↑", self.move_hit_button, 1, cv2.QT_PUSH_BUTTON,
                         False)
        cv2.createButton("→", self.move_hit_button, 3, cv2.QT_PUSH_BUTTON,
                         False)

        cv2.createButton("Hit example", self.is_keyframe_button,
                         KeyFrame.HIT_EXAMPLE,
                         cv2.QT_PUSH_BUTTON | cv2.QT_NEW_BUTTONBAR, False)
        cv2.createButton("Not hit example", self.is_keyframe_button,
                         KeyFrame.NOT_HIT_EXAMPLE,
                         cv2.QT_PUSH_BUTTON, False)
        cv2.createButton("Ambiguous example", self.is_keyframe_button,
                         KeyFrame.AMBIGUOUS_EXAMPLE,
                         cv2.QT_PUSH_BUTTON, False)
        cv2.createButton("No example", self.is_keyframe_button,
                         KeyFrame.NOT_KEYFRAME,
                         cv2.QT_PUSH_BUTTON, False)
        return True

    def extract_keyframe(self, frame, goal_corners):
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
        if outframe.size == 0:
            return None

        return (cv2.cvtColor(outframe, cv2.COLOR_RGB2GRAY), (xmin, ymin))

    def save(self):
        if self.dirty_flag:
            # Set soundframes automatically.
            hit_frames = self.testdata.get_all_hit_frames()
            self.videodata.set_sound_frames_from_hit_frames(hit_frames)

            # new_filename = "new-videodata.yaml"
            # with open(new_filename, 'w') as outfile:
            with tempfile.NamedTemporaryFile('w') as outfile:
                print("New videodata is saved to temporary file {0}".format(outfile.name))
                outfile.write(q.settings.save())
                outfile.write(q.videodata.save())
                outfile.write(q.testdata.save())
                outfile.flush()
                subprocess.run(["colordiff", data_filename, outfile.name])
                while True:
                    try:
                        yesno = str(input("Overwrite yaml file (y/N)? "))
                    except:
                        continue

                    if yesno == 'y' or yesno == 'Y':
                        print("Saving data to {0}".format(data_filename))
                        subprocess.run(["cp", outfile.name, data_filename])
                    else:
                        print("Not saving data.")
                    break
            print("done")


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: %s [videofile]" % sys.argv[0])
        sys.exit(0)

    head, tail = os.path.split(sys.argv[1])
    base, ext = tail.split('.')
    if head:
        head += "/"
    data_filename = head + base + '.' + 'yaml'
    video_filename = head + base + '.' + ext

    q = Quantify()

    if not q.setup(video_filename, data_filename):
        sys.exit(-1)

    q.quantify(video_filename)
    q.save()
