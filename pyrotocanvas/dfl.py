#!/usr/bin/env python
import os
import shutil

dflDir = "C:\\PortableApps\\DeepFaceLab\\DeepFaceLab_NVIDIA"
dflWorkspace = os.path.join(dflDir, "workspace")

dfl_params = {
    "source": "Choose the video with the face you want to add.",
    "destination": "Choose the video with the face you want to affect."
}

dfl_install_help_fmt = """
You must install DeepFace Lab such that {} exists.
Visit https://github.com/iperov/DeepFaceLab and scroll down to
"Releases". The magnet link requires a program such as Deluge (free)
from https://dev.deluge-torrent.org/wiki/Download.
"""

dfl_help_fmt = """
After choosing a source and destination, you must run each batch
file in {} in the numbered order.

See also:

"The DeepFaceLab Tutorial (always up-to-date)":
https://pub.dfblue.com/pub/2019-10-25-deepfacelab-tutorial

"DeepFake Tutorial: A beginners Guide with DeepFace Lab":
https://www.cinecom.net/post-production/deepfake-tutorial-beginners/
"""

def dfl_help():
    return dfl_help_fmt.format(dflDir)
    
    
def dfl_install_help():
    return dfl_install_help_fmt.format(dflDir)

def choose_dfl_param(name, videoPath):
    if videoPath is None:
        raise ValueError("videoPath was None in choose_dfl_param.")
    dfSource = os.path.join(dflWorkspace, "data_src.mp4")
    dfDest = os.path.join(dflWorkspace, "data_dst.mp4")
    copyAs = None
    if name == "destination":
        copyAs = dfDest
    elif name == "source":
        copyAs = dfSource
    else:
        raise ValueError("{} is an unknown DeepFace Lab Param--choose"
                           ": {}".format(name, dfl_params.keys()))
    if os.path.isfile(copyAs):
        os.remove(copyAs)
    shutil.copy(videoPath, copyAs)
    videoName = os.path.split(videoPath)[1]
    print("[dfl.py] * wrote {} to {}.".format(videoName, copyAs))


def choose_dfl_param_in(name, video_dir):
    if not os.path.isdir(dflWorkspace):
        print()
        print(dfl_help)
        print()
        raise RuntimeError("DeepFace Lab doesn't exist here: {}"
                           "".format(dflWorkspace))
    videoPath = None
    paths = []
    for sub in os.listdir(video_dir):
        subPath = os.path.join(video_dir, sub)
        if not subPath.lower().endswith(".mp4"):
            continue
        videoPath = subPath
        break
    if videoPath is None:
        raise ValueError("There was no .mp4 to select in {}"
                         "".format(video_dir))
    choose_dfl_param(name, videoPath)
