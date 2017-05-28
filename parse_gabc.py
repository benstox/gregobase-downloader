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


def juggle_around_episemata(neume, episema=r"_"):
    regexp = episema + r"{2,}"
    matches = re.finditer(regexp, neume)
    for match in matches:
        neume = juggle_around_episemata_in_match(neume, match, episema)

    return(neume)


def juggle_around_episemata_in_match(neume, match, episema="_"):
    episema = str(episema).replace("\\", "")
    start, end = match.span()
    n_episemata = end - start
    for i in range(n_episemata):
        if i == 0:
            neume = neume[:start - i] + episema + neume[end:]
        else:
            neume = neume[:start - i] + episema + neume[end - n_episemata - i:]
    return(neume)


files = [
    filename for filename in os.listdir(GABC_DIR)
    if not filename.startswith(".")]

for filename in files:
    print(filename)
    with open("{}/{}".format(GABC_DIR, filename), "r") as infile:
        gabc = infile.read()

    if sum(1 for match in re.finditer("%%", gabc)) > 1:
        sections = gabc.split("%%")
        gabc = sections[-1]
        meta = "".join(sections[:-1])
    else:
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
    cleaned = []
    for neume in neumes:
        # remove non-note and non-length characters from neumes
        for char in "()'~v/!":
            neume = neume.replace(char, "")
        # replace quilismae with episemata
        neume = neume.replace("w", "_")
        # place bunched episemata adjacent to the notes they affect
        neume = juggle_around_episemata(neume, r"_")
        neume = juggle_around_episemata(neume, r"\.")
        # FIXME still have to deal with flats and key signatures
        cleaned.append(neume)

    melody = "".join(cleaned)

    outfilename = re.sub(r"\.gabc$", "", filename)
    with open("{0}/{1}".format(mode_dir, outfilename), "w") as outfile:
        outfile.write(melody)

print(flats)
