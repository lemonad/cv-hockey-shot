import glob
import os
import subprocess

import yaml

from ..common.Datafiles import get_all_paths, get_paths, get_session_names
from ..common.AppData import AppSettings, TestData, VideoData
from .extract_keyframes import ExtractKeyframes

session_names = get_session_names()
for session_name in session_names:
    print("Deleting training frames for session {:s}...".format(session_name))
    for imfile in glob.glob("dataset/hit/{:s}*".format(session_name)):
        os.remove(imfile)
    for imfile in glob.glob("dataset/not_hit/{:s}*".format(session_name)):
        os.remove(imfile)

    print("Extracting training frames from session {:s}...".format(session_name))
    for p in get_paths("MOV", session_name, training=True, testing=True):
        print("Reading videodata from {0}".format(p))

        ex = ExtractKeyframes(p, silent=True)
        if not ex.setup():
            print("Failed to setup frame extraction")
            sys.exit(-1)
        ex.quantify()
