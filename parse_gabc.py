#!/usr/bin/env python3

import os
import re

GABC_DIR = "gabc"
MELODY_DIR = "melody"

NOTE_VALUES = {
    "z": -5,  # sol
    "a": -3,  # la
    "B": -2,  # si bemol
    "b": -1,  # si
    "c": 0,  # do
    "D": 1,  # re bemol
    "d": 2,
    "E": 3,  # mi bemol
    "e": 4,
    "f": 5,
    "G": 6,  # sol bemol
    "g": 7,
    "H": 8,  # la bemol
    "h": 9,
    "I": 10,  # si bemol
    "i": 11,
    "j": 12,  # do
    "K": 13,  # re bemol
    "k": 14,  # re
    "l": 16,  # mi
    "m": 17,  # fa
    "n": 19,  # sol
    "o": 21,  # la
    "p": 23,  # si
}
NOTE_SEQUENCE = [
    "z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p"
]
FLAT_SEQUENCE_1 = [
    "E", "G", "I", "K"
]
FLAT_SEQUENCE_2 = [
    "B", "D"
]
INVERSE_NOTE_VALUES = {v: k for k, v in NOTE_VALUES.items()}
CLEF_TRANSPOSE = {
    "f3": -2,
    "c4": 0,
    "c3": 2,
    "c2": 4,
}
FLAT_CLEF_LOCATION = {
    "4": "i",
    "3": "g",
    "2": "e",
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


def transpose_note(original_note, transpose_by):
    if original_note in "._":
        return(original_note)

    if original_note in NOTE_SEQUENCE:
        note_sequence = NOTE_SEQUENCE
    elif original_note in FLAT_SEQUENCE_1:
        transpose_by //= 2
        note_sequence = FLAT_SEQUENCE_1
    elif original_note in FLAT_SEQUENCE_2:
        transpose_by //= 2
        note_sequence = FLAT_SEQUENCE_2
    else:
        raise KeyError("Unknown note {}!!".format(original_note))

    original_value = note_sequence.index(original_note)
    new_value = original_value + transpose_by
    if new_value < 0:
        raise ValueError("Note {} transposed by {} has gone off the scale!!".format(
            original_note, transpose_by))
    new_note = note_sequence[new_value]
    return(new_note)


files = [
    filename for filename in os.listdir(GABC_DIR)
    if not filename.startswith(".")]

for filename in files:
    print(filename)
    with open("{}/{}".format(GABC_DIR, filename), "r") as infile:
        gabc = infile.read()

    if "%%" not in gabc:
        print("WARNING!! No %% found in {}.".format(filename))
        continue

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
    # sort the clef out
    clef = clef.replace("(", "").replace(")", "")
    if not re.search(r"^[cf]b?[234]$", clef):
        print("WARNING!!! Unknown clef {}. Skipping {}.".format(clef, filename))
        continue
    if clef[1] == "b":
        flat_clef = True
        clef = clef.replace("b", "")
    else:
        flat_clef = False
    # filter out non-neumes (e.g. breaks)
    neumes = filter(lambda x: re.search(HAS_NOTES, x), neumes)
    # check whether transposition will need to take place an octave up
    # not sure if still needed, now that I've just added more notes to
    # the bottom of the scale
    cleaned = []
    for neume in neumes:
        # remove code for horizontal curly braces, etc., that
        # appear above the staff
        neume = re.sub("\[.*?\]", "", neume)
        # remove non-note and non-length characters from neumes
        for char in "()'~vr<>/! ,;:`zZ":
            neume = neume.replace(char, "")
        # don't bother with neumes which are just funny custodes
        if re.search(r"^.\+$", neume):
            continue
        # check whether this neume is actually a new clef
        if re.search(r"^[cf]b?[234]$", neume):
            clef = neume
            if clef[1] == "b":
                flat_clef = True
                clef = clef.replace("b", "")
            else:
                flat_clef = False
            continue
        # remove any numbers
        for char in "0123456789":
            neume = neume.replace(char, "")
        # replace quilismae with episemata
        neume = neume.replace("w", "_")
        # place bunched episemata adjacent to the notes they affect
        neume = re.sub(r"(\.)(?=_)", "_", neume)
        neume = re.sub(r"_\.", ".", neume)
        neume = juggle_around_episemata(neume, r"_")
        neume = juggle_around_episemata(neume, r"\.")
        # flats
        if flat_clef:
            to_flatten = [FLAT_CLEF_LOCATION[clef[-1]]]
            for natural in to_flatten:
                natural_value = NOTE_VALUES[natural]
                flat = INVERSE_NOTE_VALUES[natural_value - 1]
                neume = neume.replace(natural, flat)
        elif "x" in neume:
            to_flatten = set(re.findall("(.{1})(?=x)", neume))
            for natural in to_flatten:
                first_piece, *rest = neume.split(natural + "x")
                rest = "".join(rest)
                natural_value = NOTE_VALUES[natural]
                flat = INVERSE_NOTE_VALUES[natural_value - 1]
                neume = first_piece + rest.replace(natural, flat)
        # naturals
        if "y" in neume:
            to_flatten = set(re.findall("(.{1})(?=y)", neume))
            for natural in to_flatten:
                first_piece, *rest = neume.split(natural + "y")
                rest = "".join(rest)
                natural_value = NOTE_VALUES[natural]
                flat = INVERSE_NOTE_VALUES[natural_value - 1]
                neume = first_piece + rest.replace(flat, natural)
        # key signatures
        try:
            transpose_by = CLEF_TRANSPOSE[clef]
        except KeyError:
            raise KeyError("Unknown clef {} in file {}.".format(clef, filename))

        if transpose_by:
            # print(neume)
            neume = "".join(
                transpose_note(note, transpose_by)
                for note in neume
            )

        cleaned.append(neume)

    melody = "".join(cleaned)

    outfilename = re.sub(r"\.gabc$", "", filename)
    with open("{0}/{1}".format(mode_dir, outfilename), "w") as outfile:
        outfile.write(melody)
