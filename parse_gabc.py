#!/usr/bin/env python3

import os
import re

GABC_DIR = "gabc"
MELODY_DIR = "melody"


files = [
    filename for filename in os.listdir(GABC_DIR)
    if not filename.startswith(".")]

for filename in files:
    with open("{}/{}".format(GABC_DIR, filename), "r") as infile:
        gabc = infile.read()

    meta, gabc = gabc.split("%%")

    if "mode" in meta:
        mode = re.findall(r"(?<=mode:)(.*)(?=;)", meta)[0].strip()
        for char in "; ":
            mode = mode.replace(char, "")
        if re.search(r"^[0-9]+$", mode):
            mode = "mode_" + mode
    else:
        mode = "unknown_mode"

    mode_dir = "{0}/{1}".format(MELODY_DIR, mode)
    if not os.path.exists(mode_dir):
        os.makedirs(mode_dir)

    # parse out melody data here
    melody = gabc

    outfilename = re.sub(r"\.gabc$", "", filename)
    with open("{0}/{1}".format(mode_dir, outfilename), "w") as outfile:
        outfile.write(melody)
