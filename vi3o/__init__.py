"""
:mod:`vi3o` ---  VIdeo and Image IO
====================================
"""

# Rebuild mjpg.c every time..
import os, sys
dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
if os.system("cd {} && python build_mjpg.py".format(dir)):
    sys.exit(1)

__version_info__ = (0, 6, 0)
__version__ = '.'.join(str(i) for i in __version_info__)

# FIXME: Turn into a Video base class that documents the interface

def Video(filename, grey=False):
    """
    Creates a *Video* object representing the video in the file *filename*.
    See Overview above.
    """
    if filename.endswith('.mkv'):
        from vi3o.mkv import Mkv
        return Mkv(filename, grey)
    elif filename.endswith('.mjpg'):
        from vi3o.mjpg import Mjpg
        return Mjpg(filename, grey)
    else:
        from vi3o.opencv import CvVideo
        return CvVideo(filename, grey)


def _get_debug_viewer(name):
    from vi3o.debugview import DebugViewer
    if name not in DebugViewer.named_viewers:
        DebugViewer.named_viewers[name] = DebugViewer(name)
    return DebugViewer.named_viewers[name]


def view(img, name='Default', scale=False, pause=None):
    """
    Show the image *img* (a numpy array) in the debug viewer window named *name*.
    If *scale* is true the image intensities are rescaled to cover the 0..255
    range. If *pause* is set to True/False, the viewer is paused/unpaused after the
    image is displayed.
    """
    _get_debug_viewer(name).view(img, scale, pause=pause)

def viewsc(img, name='Default', pause=None):
    """
    Calls :func:`vi3o.view` with *scale=True*.
    """
    view(img, name, True, pause)

def flipp(name='Default', pause=None):
    """
    After :func:`vi3o.flipp` is called, subsequent calls to :func:`vi3o.view` will no
    longer display the images directly. Instead they will be collected and concatinated.
    On the next call to :func:`vi3o.flipp` all the collected images will be displayed.
    If *pause* is set to True/False, the viewer is paused/unpaused after the
    image is displayed.
    """
    _get_debug_viewer(name).flipp(pause)

from vi3o.sync import SyncedVideos
from vi3o.cat import VideoCat, VideoGlob
