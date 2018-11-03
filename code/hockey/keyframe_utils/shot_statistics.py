import subprocess

import yaml

from ..common.Datafiles import get_all_paths, get_paths, get_session_names
from ..common.AppData import AppSettings, TestData, VideoData

session_names = get_session_names()
for session_name in session_names:
    shots = 0
    not_misses = 0
    misses = 0
    not_miss_bounces = 0

    print("Collecting data from session {0}".format(session_name))
    for p in get_paths("yaml", session_name, training=True, testing=True):
        # print("Reading videodata from {0}".format(p))
        stream = open(p, "r")
        data = yaml.load(stream)
        testdata = TestData(data["test_data"])

        frames = testdata.get_all_hit_frames()
        for f in frames:
            shots += 1
            if testdata.is_miss_frame(f):
                misses += 1
            elif testdata.is_bounce_frame(f):
                not_miss_bounces += 1
            else:
                not_misses += 1

    print(
        "Shots: {:d}, hits: {:d}, excluded: {:d} (misses: {:d}, bounces: {:d})".format(
            shots, not_misses, misses + not_miss_bounces, misses, not_miss_bounces
        )
    )
