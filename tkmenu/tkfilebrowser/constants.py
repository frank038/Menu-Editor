# -*- coding: utf-8 -*-
"""
tkfilebrowser - Alternative to filedialog for Tkinter
Copyright 2017 Juliette Monsel <j_4321@protonmail.com>

tkfilebrowser is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

tkfilebrowser is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.


The icons are modified versions of icons from the elementary project
(the xfce fork to be precise https://github.com/shimmerproject/elementary-xfce)
Copyright 2007-2013 elementary LLC.


Constants and functions
"""


import locale
import time
import os
from math import log10

#try:
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askyesnocancel, showerror
from urllib.parse import unquote

PATH = os.path.dirname(__file__)

# ---  images
IM_HOME = os.path.join(PATH, "images", "home.png")
IM_FOLDER = os.path.join(PATH, "images", "dossier.png")
IM_FOLDER_LINK = os.path.join(PATH, "images", "dossier_link.png")
IM_NEW = os.path.join(PATH, "images", "new_folder.png")
IM_FILE = os.path.join(PATH, "images", "file.png")
IM_FILE_LINK = os.path.join(PATH, "images", "file_link.png")
IM_DRIVE = os.path.join(PATH, "images", "drive.png")
IM_RECENT = os.path.join(PATH, "images", "recent.png")
IM_RECENT_24 = os.path.join(PATH, "images", "recent_24.png")


def _(text):
    return text


SIZES = [(_("B"), 1), ("kB", 1e3), ("MB", 1e6), ("GB", 1e9), ("TB", 1e12)]

TODAY = time.strftime("%x")
YEAR = time.strftime("%Y")
DAY = int(time.strftime("%j"))


# ---  functions
def add_trace(variable, mode, callback):
    try:
        return variable.trace_add(mode, callback)
    except AttributeError:
        return variable.trace(mode[0], callback)


def remove_trace(variable, mode, cbname):
    try:
        variable.trace_remove(mode, cbname)
    except AttributeError:
        variable.trace_vdelete(mode[0], cbname)


def get_modification_date(file):
    """Return the modification date of file."""
    tps = time.localtime(os.path.getmtime(file))
    date = time.strftime("%x", tps)
    if date == TODAY:
        date = _("Today") + time.strftime(" %H:%M", tps)
    elif time.strftime("%Y", tps) == YEAR and (DAY - int(time.strftime("%j", tps))) < 7:
        date = time.strftime("%A %H:%M", tps)
    return date


def get_size(file):
    """Return the size of file."""
    size_o = os.path.getsize(file)
    if size_o > 0:
        m = int(log10(size_o) // 3)
        if m < len(SIZES):
            unit, div = SIZES[m]
        else:
            unit, div = SIZES[-1]
        size = "%s %s" % (locale.format("%.1f", size_o / div), unit)
    else:
        size = "0 " + _("B")
    return size
