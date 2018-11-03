"""
Detect canvas goal corners using SIFT and FLANN matching.
Optional Kalman filter stabilization.

TODO: When homography is skipped, next correct step should not use 1 * timestep.

"""
import cv2
import numpy as np
import yaml

from .KalmanPoint import KalmanPoint


class CanvasDetector:
    MIN_MATCH_COUNT = 10

    CANVAS_WIDTH = 2499
    CANVAS_HEIGHT = 1440
    CANVAS_GOAL_TOP_OFFSET = 171
    CANVAS_GOAL_BOTTOM_OFFSET = 50
    CANVAS_GOAL_LEFT_OFFSET = 331
    CANVAS_GOAL_RIGHT_OFFSET = 338

    CANVAS_EXTEND_TOP = 125
    CANVAS_EXTEND_BOTTOM = 35
    CANVAS_EXTEND_LEFT = 225
    CANVAS_EXTEND_RIGHT = 225

    def __init__(self, stencil_path, timestep=None):
        self.stencil_path = stencil_path
        # Setup Kalman filters.
        if timestep:
            self.use_kalman_filters = True
            pn = 0.1
            pndt = 0.1
            mn = 10
            self.ul_corner_kalman_filter = KalmanPoint(
                timestep,
                process_noise_cov=np.array([pn, pn, pndt, pndt], "float32"),
                measurement_noise_cov=np.array([mn, mn], "float32"),
            )
            self.ur_corner_kalman_filter = KalmanPoint(
                timestep,
                process_noise_cov=np.array([pn, pn, pndt, pndt], "float32"),
                measurement_noise_cov=np.array([mn, mn], "float32"),
            )
            self.lr_corner_kalman_filter = KalmanPoint(
                timestep,
                process_noise_cov=np.array([pn, pn, pndt, pndt], "float32"),
                measurement_noise_cov=np.array([mn, mn], "float32"),
            )
            self.ll_corner_kalman_filter = KalmanPoint(
                timestep,
                process_noise_cov=np.array([pn, pn, pndt, pndt], "float32"),
                measurement_noise_cov=np.array([mn, mn], "float32"),
            )
        else:
            self.use_kalman_filters = False

        # Initiate SIFT detectors
        self.sift_frame = cv2.xfeatures2d.SIFT_create(
            nfeatures=0,
            nOctaveLayers=3,
            contrastThreshold=0.04,
            edgeThreshold=10,
            sigma=1.4,
        )

        # Stencil
        stencil_image = cv2.imread(self.stencil_path)
        stencil_gray = cv2.cvtColor(stencil_image, cv2.COLOR_RGB2GRAY)
        self.stencil_shape = stencil_gray.shape
        # Use a different SIFT detector for the stencil since they
        # use different configurations.
        sift_stencil = cv2.xfeatures2d.SIFT_create(
            nfeatures=0,
            nOctaveLayers=3,
            contrastThreshold=0.04,
            edgeThreshold=10,
            sigma=1.6,
        )
        self.stencil_keypoints, self.stencil_descriptors = \
                sift_stencil.detectAndCompute(stencil_gray, None)

    def find_goal_corners(self, fullframe):
        gray_fullframe = cv2.cvtColor(fullframe, cv2.COLOR_RGB2GRAY)

        # find the image keypoints and descriptors with SIFT
        kp2, des2 = self.sift_frame.detectAndCompute(gray_fullframe, None)

        # print(des2.type())
        # print(self.stencil_descriptors.type())
        # if self.stencil_descriptors.dtype != np.float32:
        #     self.stencil_descriptors = self.stencil_descriptors.astype(np.float32)
        # if des2.dtype != np.float32:
        #     des2 = des2.astype(np.float32)

        # bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)
        matches = bf.match(des2, self.stencil_descriptors)
        # Sort matches by distance. Best come first.
        matches = sorted(matches, key=lambda x: x.distance)

        # FLANN_INDEX_KDTREE = 0
        # index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        # search_params = dict(checks=50)
        # flann = cv2.FlannBasedMatcher(index_params, search_params)
        # matches = flann.knnMatch(self.stencil_descriptors, des2, k=2)

        # store all the good matches as per Lowe's ratio test.
        # for m in matches:
        #     print(m.distance)
        # print("-------")

        good = matches[:20]
        # good = []
        # for m, n in matches:
        #     if m.distance < (2.0 * n.distance):
        #         good.append(m)

        corners = None
        if len(good) > self.MIN_MATCH_COUNT:
            src_pts = np.float32(
                [self.stencil_keypoints[m.trainIdx].pt for m in good]
            ).reshape(-1, 1, 2)
            dst_pts = np.float32([kp2[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)

            M, mask = cv2.findHomography(
                src_pts, dst_pts, cv2.RANSAC, 3.0, None, maxIters=2000, confidence=0.995
            )
            # matchesMask = mask.ravel().tolist()
            if np.linalg.det(M[0:2, 0:2]) > 0:
                corners = self.get_goal_corners_from_homography(M)

        if corners is not None:
            if not self.use_kalman_filters:
                return np.int32(corners)

            # Get updated corner coordinates from Kalman filters.
            kf_ul = self.ul_corner_kalman_filter.predict()
            kf_ll = self.ll_corner_kalman_filter.predict()
            kf_lr = self.lr_corner_kalman_filter.predict()
            kf_ur = self.ur_corner_kalman_filter.predict()
            corners_pred = np.array([kf_ul, kf_ll, kf_lr, kf_ur])

            # Update Kalman filters.
            self.ul_corner_kalman_filter.correct(corners[0])
            self.ll_corner_kalman_filter.correct(corners[1])
            self.lr_corner_kalman_filter.correct(corners[2])
            self.ur_corner_kalman_filter.correct(corners[3])
            return np.int32(corners_pred)
        elif self.use_kalman_filters:
            print(
                "Not enough matches are found - %d/%d but okay since using "
                "Kalman filter." % (len(good), self.MIN_MATCH_COUNT)
            )
            # Use corner coordinates from Kalman filters.
            kf_ul = self.ul_corner_kalman_filter.predict()
            kf_ll = self.ll_corner_kalman_filter.predict()
            kf_lr = self.lr_corner_kalman_filter.predict()
            kf_ur = self.ur_corner_kalman_filter.predict()
            return np.int32(np.array([kf_ul, kf_ll, kf_lr, kf_ur]))
        else:
            print(
                "Not enough matches are found - %d/%d"
                % (len(good), self.MIN_MATCH_COUNT)
            )
            return None

    def get_goal_corners_from_homography(self, M):
        h, w = self.stencil_shape
        h_pixels_per_mm = h / self.CANVAS_HEIGHT
        w_pixels_per_mm = w / self.CANVAS_WIDTH
        top_offset = self.CANVAS_GOAL_TOP_OFFSET * h_pixels_per_mm
        bottom_offset = self.CANVAS_GOAL_BOTTOM_OFFSET * h_pixels_per_mm
        left_offset = self.CANVAS_GOAL_LEFT_OFFSET * w_pixels_per_mm
        right_offset = self.CANVAS_GOAL_RIGHT_OFFSET * w_pixels_per_mm

        top_offset -= self.CANVAS_EXTEND_TOP * h_pixels_per_mm
        bottom_offset -= self.CANVAS_EXTEND_BOTTOM * h_pixels_per_mm
        left_offset -= self.CANVAS_EXTEND_LEFT * h_pixels_per_mm
        right_offset -= self.CANVAS_EXTEND_RIGHT * h_pixels_per_mm

        pts = np.float32(
            [
                [left_offset, top_offset],
                [left_offset, h - 1 - bottom_offset],
                [w - 1 - right_offset, h - 1 - bottom_offset],
                [w - 1 - right_offset, top_offset],
            ]
        ).reshape(-1, 1, 2)
        dst = cv2.perspectiveTransform(pts, M)
        ul = dst[0][0]
        ll = dst[1][0]
        lr = dst[2][0]
        ur = dst[3][0]
        return np.array([ul, ll, lr, ur])

    def reset(self):
        if not self.use_kalman_filters:
            return
        self.ul_corner_kalman_filter.restart()
        self.ll_corner_kalman_filter.restart()
        self.lr_corner_kalman_filter.restart()
        self.ur_corner_kalman_filter.restart()
