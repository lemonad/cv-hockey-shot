"""
Handles per video data and data that is used for testing.

"""
import yaml

from .Dimension import Dimension
from .KeyFrame import KeyFrame
from .Point import Point
from .Rect import Rect


class AppSettings:
    """User sets/selects these values in the settings of the application."""

    def __init__(self, settings={}):
        pass

    def save(self):
        data = {"app_settings": {}}
        return yaml.dump(data)


class VideoData:
    """Data that we expect the application to provide for us."""

    # TODO Add frame rate, video dimensions, etc.

    _number_of_shots = 0
    _target_pixel_points = [None, None, None, None, None]
    _targets = []
    # Sound frames set automatically when quantifying, adjusted 1.5
    # seconds before shot hits canvas:
    #     {'start': frame_equivalent_to_hit_frame_minus_1.5_seconds,
    #      'end': frame_equivalent_to_hit_frame_plus_1.5_seconds}
    _sound_frames = []
    _frame_rate = None
    _first_frame = None
    _last_frame = None
    _rotation90 = None
    # Inner size of goal posts in centimeters.
    _goal_inner_size_in_cm = Dimension(183, 122)
    _target_offsets_in_cm = [
        Point(11.5, 91),
        Point(11.5, 21),
        Point(171.5, 21),
        Point(171.5, 91),
        Point(91.5, 101),
    ]
    # Upper left, lower right.
    _crop = [None, None]
    # Upper left, upper right, lower right, lower left.
    _goal_corners = [None, None, None, None]

    def __init__(self, data={}):
        if "frame_rate" in data:
            self.set_frames_per_second(data["frame_rate"])
        if "first_frame" in data:
            self.set_first_frame(data["first_frame"])
        if "last_frame" in data:
            self.set_last_frame(data["last_frame"])
        if "rotation90" in data:
            self.set_rotation90(data["rotation90"])
        if "number_of_shots" in data:
            self.set_number_of_shots(data["number_of_shots"])
        if "goal_corners" in data:
            assert len(data["goal_corners"]) == 4
            self.set_goal_corners(data["goal_corners"])
        if "target_coords" in data:
            assert len(data["target_coords"]) == 5
            for n, coord in enumerate(data["target_coords"]):
                self.set_pixel_point_for_target(n + 1, coord)
        if "targets" in data:
            if self.number_of_shots != 0 and len(data["targets"]) == 0:
                print(
                    "No targets defined -- add these directly in the yaml "
                    "file, after having added all shots."
                )
            if len(data["targets"]) != self.number_of_shots:
                print(
                    "All targets not defined -- add these directly in the yaml " "file."
                )
            for n, tno in enumerate(data["targets"]):
                self.set_target_for_shot(n, tno)
        if "target_offsets_in_cm" in data:
            assert len(data["target_offsets_in_cm"]) == 5
            for i, offset in enumerate(data["target_offsets_in_cm"]):
                self.set_target_offset_in_cm(i + 1, offset)
        if "goal_inner_size_in_cm" in data:
            self.set_goal_inner_dimensions_in_cm(data["goal_inner_size_in_cm"])
        if "sound_frames" in data:
            assert len(data["sound_frames"]) == self.number_of_shots
            for n, sf in enumerate(data["sound_frames"]):
                self.set_shot_sound_frame_for_shot(n, sf["start"], sf["end"])
        if "crop" in data:
            assert len(data["crop"]) == 2
            self.set_upper_left_crop(data["crop"][0])
            self.set_lower_right_crop(data["crop"][1])

    @property
    def number_of_shots(self):
        """Number of shots to analyze during this video."""
        return self._number_of_shots

    def set_number_of_shots(self, n):
        """Update number of shots to analyze during this video."""
        self._number_of_shots = n

    @property
    def frames_per_second(self):
        """Video frame rate."""
        return self._frame_rate

    def set_frames_per_second(self, fps):
        """Set video frame rate."""
        self._frame_rate = fps

    @property
    def first_frame(self):
        """First video frame to use."""
        return self._first_frame

    def set_first_frame(self, frame_no):
        """Set first video frame to use."""
        self._first_frame = frame_no

    @property
    def last_frame(self):
        """Last video frame to use."""
        return self._last_frame

    def set_last_frame(self, frame_no):
        """Set last video frame to use."""
        self._last_frame = frame_no

    @staticmethod
    def rotation_to_rotation90(rotation):
        assert rotation % 90 == 0
        return rotation // 90

    @property
    def rotation90(self):
        """Rotation in multiples of 90 by which the orientation of the
        video becomes correct."""
        return self._rotation90

    def set_rotation90(self, rotation90):
        """Set rotation / orientation."""
        self._rotation90 = rotation90

    def get_target_for_shot(self, index_0_based):
        """Get the target number (1-5) for the (n-1)'th shot."""
        if index_0_based in range(len(self._targets)):
            return self._targets[index_0_based]
        else:
            return None

    def get_targets_for_all_shots(self):
        """Get the target numbers (1-5) for all shots."""
        return self._targets

    def set_target_for_shot(self, index_0_based, target_number):
        """Set the target number (1-5) for the (n-1)'th shot."""
        l = len(self._targets)
        if l < index_0_based + 1:
            delta = l - index_0_based + 1
            self._targets.extend([None] * delta)
        self._targets[index_0_based] = target_number

    def get_shot_sound_frame_for_shot(self, index_0_based):
        """Get the frames enclosing the video frames to analyze
        for the (n-1)'th shot."""
        if index_0_based < 0 or index_0_based >= len(self._sound_frames):
            return None
        return (
            self._sound_frames[index_0_based]["start"],
            self._sound_frames[index_0_based]["end"],
        )

    def get_all_shot_sound_frames(self):
        """Get the shot sound frames for all shots."""
        return self._sound_frames

    def set_shot_sound_frame_for_shot(self, index_0_based, start_frame, end_frame):
        """Set the frame enclosing frames to analyze for the (n-1)'th shot."""
        l = len(self._sound_frames)
        if l < index_0_based + 1:
            delta = l - index_0_based + 1
            self._sound_frames.extend([None] * delta)
        self._sound_frames[index_0_based] = {"start": start_frame, "end": end_frame}

    def get_pixel_point_for_target(self, index_1_based):
        """Get the target point in pixels (with perspective) for target 1-5.

        The user is expected to point these out as exactly as possible,
        perhaps even having these identified per shot if we can do it
        automatically.
        """
        return self._target_pixel_points[index_1_based - 1]

    def get_all_target_pixel_points(self):
        """Get all target pixel points."""
        tpp = []
        for point in self._target_pixel_points:
            tpp.append(point)
        return tpp

    def get_all_target_pixel_points_as_tuples(self):
        """Get all target pixel points as tuples."""
        tpp = []
        for point in self._target_pixel_points:
            tpp.append(point.as_tuple())
        return tpp

    def set_pixel_point_for_target(self, index_1_based, coords):
        self._target_pixel_points[index_1_based - 1] = coords

    def get_shot_number(self, frame_number):
        """Find shot number (0-based) based on a frame number."""
        shot_number = 0
        for shot_frame in self._sound_frames:
            if frame_number < shot_frame["start"]:
                break
            shot_number += 1
        return max(shot_number, 1) - 1

    def set_sound_frames_from_hit_frames(self, hit_frames):
        self._sound_frames = []
        sorted_hit_frames = sorted(hit_frames)
        for n, hit_frame in enumerate(sorted_hit_frames):
            start_frame = max(
                self._first_frame, int(hit_frame - self._frame_rate * 1.5)
            )
            end_frame = min(self._last_frame, int(hit_frame + self._frame_rate * 1.5))
            self.set_shot_sound_frame_for_shot(n, start_frame, end_frame)
        last_end_frame = 0
        for n in range(len(sorted_hit_frames)):
            (sf, ef) = self.get_shot_sound_frame_for_shot(n)
            if last_end_frame >= sf:
                print("Warning: overlapping sound frames.")
            last_end_frame = ef

    @property
    def goal_inner_dimensions_in_cm(self):
        return self._goal_inner_size_in_cm

    def set_goal_inner_dimensions_in_cm(self, dimensions):
        self._goal_inner_size_in_cm = dimensions

    def get_target_offset_in_cm(self, index_1_based):
        """Offset from upper left corner of goal post for a specific
        target (1-5)."""
        return self._target_offsets_in_cm[index_1_based - 1]

    def set_target_offset_in_cm(self, index_1_based, point):
        self._target_offsets_in_cm[index_1_based - 1] = point

    def get_all_target_offsets_in_cm(self):
        """Get all target offsets."""
        tl = []
        for offset in self._target_offsets_in_cm:
            tl.append(offset)
        return tl

    def get_all_target_offsets_in_cm_as_tuples(self):
        """Get all target offsets as tuples."""
        tl = []
        for offset in self._target_offsets_in_cm:
            tl.append(offset.as_tuple())
        return tl

    def get_crop_coords(self):
        return (self._crop[0], self._crop[1])

    @property
    def crop_width(self):
        """Width of the area we crop the canvas to."""
        width = self._crop[1].x - self._crop[0].x
        assert width > 0
        return width

    @property
    def crop_height(self):
        """Height of the area we crop the canvas to."""
        height = self._crop[1].y - self._crop[0].y
        assert height > 0
        return height

    @property
    def upper_left_crop(self):
        return self._crop[0]

    @property
    def lower_right_crop(self):
        return self._crop[1]

    def set_upper_left_crop(self, point):
        self._crop[0] = point

    def set_lower_right_crop(self, point):
        self._crop[1] = point

    def set_goal_corners(self, corners):
        self._goal_corners[0] = corners[0]
        self._goal_corners[1] = corners[1]
        self._goal_corners[2] = corners[2]
        self._goal_corners[3] = corners[3]

    def get_goal_corner_coords(self):
        return [
            self._goal_corners[0],
            self._goal_corners[1],
            self._goal_corners[2],
            self._goal_corners[3],
        ]

    @property
    def upper_left_goal_corner(self):
        return self._goal_corners[0]

    @property
    def upper_right_goal_corner(self):
        return self._goal_corners[1]

    @property
    def lower_right_goal_corner(self):
        return self._goal_corners[2]

    @property
    def lower_left_goal_corner(self):
        return self._goal_corners[3]

    def save(self):
        data = {
            "video_data": {
                "target_offsets_in_cm": self.get_all_target_offsets_in_cm(),
                "goal_inner_size_in_cm": self.goal_inner_dimensions_in_cm,
                "frame_rate": self.frames_per_second,
                "first_frame": self.first_frame,
                "last_frame": self.last_frame,
                "rotation90": self.rotation90,
                "number_of_shots": self.number_of_shots,
                "targets": self.get_targets_for_all_shots(),
                "target_coords": self.get_all_target_pixel_points(),
                "sound_frames": self.get_all_shot_sound_frames(),
                "crop": self.get_crop_coords(),
                "goal_corners": self.get_goal_corner_coords(),
            }
        }
        return yaml.dump(data)


class TestData:
    """Reference data we can use when testing.

    DON'T RELY ON THIS FOR ANYTHING BUT TESTING!
    """

    # n: {'coord': Point(x, y), 'miss': False, 'bounce': False}
    _hits = {}
    _keyframes = {}
    _extracted = {}

    def __init__(self, data={}):
        if "hits" in data:
            self._hits = data["hits"]
        if "keyframes" in data:
            self._keyframes = data["keyframes"]
        if "extracted" in data:
            self._extracted = data["extracted"]

    def get_keyframe_type(self, frame_number):
        """get keyframe type of a frame."""
        if frame_number not in self._keyframes:
            return KeyFrame.NOT_KEYFRAME
        else:
            return self._keyframes[frame_number]["type"]

    def set_keyframe(self, frame_number, kftype):
        """Add/remove/update keyframe."""
        if kftype is KeyFrame.NOT_KEYFRAME:
            if frame_number in self._keyframes:
                del self._keyframes[frame_number]
        else:
            self._keyframes[frame_number] = {"type": kftype}

    def get_number_of_hit_frames(self):
        return len(self._hits)

    def get_hit_frame_for_shot(self, index_0_based):
        """When the puck actually hits the canvas for the (n-1)'t shot."""
        if index_0_based < 0 or index_0_based >= len(self._hits):
            return None
        hit_list = sorted(self._hits.keys())
        return hit_list[index_0_based]

    def get_all_hit_frames(self):
        """Get all hit frames (not necessarily sorted)."""
        frame_list = []
        for f in self._hits:
            frame_list.append(f)
        return frame_list

    def get_hit_point_for_shot(self, index_0_based):
        """Where the puck actually hits the canvas for the (n-1)'th shot."""
        hit_list = sorted(self._hits.keys())
        return self._hits[hit_list[index_0_based]]["coord"]

    def add_hit_point(self, frame_number, coord):
        """Add/update a hit point on a video frame with a given coordinate."""
        miss = False
        bounce = False
        if frame_number in self._hits:
            miss = self._hits[frame_number]["miss"]
            bounce = self._hits[frame_number]["bounce"]
        self._hits[frame_number] = {"coord": coord, "miss": miss, "bounce": bounce}

    def remove_hit_point(self, frame_number):
        """Removes a hit point for a specific frame, if one exists."""
        del self._hits[frame_number]

    def get_shot_number(self, frame_number):
        """Find shot number (0-based) based on a frame number."""
        shot_number = 0
        for hit_frame in sorted(self._hits.keys()):
            if frame_number < hit_frame:
                break
            shot_number += 1
        return max(shot_number, 1) - 1

    def get_hit_coord_for_frame(self, frame_number):
        """Get the coordinates for a hit frame, if applicable."""
        if frame_number in self._hits:
            return self._hits[frame_number]["coord"]
        else:
            return None

    def is_hit_frame(self, frame_number):
        """Returns true if the given frame is specified as a hit."""
        return frame_number in self._hits

    def is_miss_frame(self, frame_number):
        if frame_number in self._hits and "miss" in self._hits[frame_number]:
            return self._hits[frame_number]["miss"]
        else:
            return False

    def is_bounce_frame(self, frame_number):
        if frame_number in self._hits and "bounce" in self._hits[frame_number]:
            return self._hits[frame_number]["bounce"]
        else:
            return False

    def toggle_miss(self, frame_number):
        if frame_number in self._hits:
            miss = True
            if "miss" in self._hits[frame_number]:
                miss = not self._hits[frame_number]["miss"]
            self._hits[frame_number]["miss"] = miss

    def toggle_bounce(self, frame_number):
        if frame_number in self._hits:
            bounce = True
            if "bounce" in self._hits[frame_number]:
                bounce = not self._hits[frame_number]["bounce"]
            self._hits[frame_number]["bounce"] = bounce

    def get_surrounding_hit_frames(self, frame_number):
        ordered_frames = sorted(self._hits.keys())
        hit_index = None
        for ix, frame in enumerate(ordered_frames):
            hit_index = ix
            if frame_number <= frame:
                break

        if hit_index is None:
            return (None, None, None)

        current_hit_frame = ordered_frames[hit_index]

        if hit_index > 0:
            prev_hit_frame = ordered_frames[hit_index - 1]
        else:
            prev_hit_frame = None

        if hit_index < (len(ordered_frames) - 1):
            next_hit_frame = ordered_frames[hit_index + 1]
        else:
            next_hit_frame = None

        return (prev_hit_frame, current_hit_frame, next_hit_frame)

    def get_extracted_data(self, frame_number):
        """Get data on extracted frame."""
        if frame_number in self._extracted:
            return self._extracted[frame_number]
        else:
            return None

    def set_extracted_data(self, frame_number, frame_rect, goal_corners):
        """Add/update data on extracted frame."""
        self._extracted[frame_number] = {
                "frame": frame_rect,
                "goal_corners": goal_corners,
                }

    def save(self):
        data = {
                "test_data": {
                    "hits": self._hits,
                    "keyframes": self._keyframes,
                    "extracted": self._extracted
                    }
                }
        return yaml.dump(data)
