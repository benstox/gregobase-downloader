#!/usr/bin/env python3

import os
import re

GABC_DIR = "gabc"
MELODY_DIR = "melody"

NOTE_VALUES = {
    "c": 0,  # do
    "d": 2,
    "w": 3,  # mi bemol
    "e": 4,
    "f": 5,
    "g": 7,
    "h": 9,
    "!": 10,  # si bemol
    "i": 11,
    "j": 12,  # do
    "k": 14,  # re
    "l": 16,  # mi
    "m": 17,  # fa
    "n": 19,  # sol
}
INVERSE_NOTE_VALUES = {v: k for k, v in NOTE_VALUES.items()}
CLEF_TRANSPOSE = {
    "f3": 3,  # not really true?
    "c3": 3,
    "c4": 0
}
HAS_NOTES = r"[cdefghijklmn]+"


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
    # lower case
    gabc = gabc.lower()
    # get the clef and lose the text
    clef, *neumes = re.findall(r"\(.*?\)", gabc)
    # filter out non-neumes (e.g. breaks)
    neumes = filter(lambda x: re.search(HAS_NOTES, x), neumes)
    for neume in neumes:
        # remove non-note and non-length characters from neumes
        for char in "()'~v":
            neume = neume.replace(char, "")
        # replace quilismae with episemata
        neume = neume.replace("w", "_")
        # place bunched episemata adjacent to the notes they affect
        matches = re.finditer(r"_{2,}", neume)
        for match in matches:
            start, end = match.span()
            n_episemata = end - start
            end -= n_episemata

    melody = gabc

    outfilename = re.sub(r"\.gabc$", "", filename)
    with open("{0}/{1}".format(mode_dir, outfilename), "w") as outfile:
        outfile.write(melody)
