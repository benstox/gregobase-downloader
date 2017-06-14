#!/usr/bin/env python3

import json
import os


folder = "melody"
melodies = {}
for mode in range(1, 9):
	melodies[mode] = {}
	mode_folder = "{}/mode_{}".format(folder, mode)
	files = [filename for filename in os.listdir(mode_folder) if not filename.startswith(".")]
	for filename in files:
		with open("{}/{}".format(mode_folder, filename), "r") as f:
			melody = f.read()

		melodies[mode][filename] = melody

with open("melodies.json", "w") as outfile:
	outfile.write(json.dumps(melodies))
