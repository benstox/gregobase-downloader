#!/usr/bin/env python3
import json
import os

OUTPUT_DIR_BASE = "markov"
ORDER_RANGE = range(2, 6)

with open("melodies.json", "r") as f:
    melodies = json.load(f)

for order in ORDER_RANGE:
    for mode, mode_melodies in melodies.items():
        output_dir = "{}/{}".format(OUTPUT_DIR_BASE, mode)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        output_filename = "{}/order_{}.json".format(output_dir, order)
        # initials
        initials = [melody[:order] for melody in mode_melodies.values()]

        # chains
        chains = {}
        for melody in mode_melodies.values():
            num_links = len(melody) - order
            for i in range(num_links):
                key = melody[i:order+i]
                value = melody[order+i]
                if key in chains:
                    chains[key].append(value)
                else:
                    chains[key] = [value]

        # finals
        finals = [melody[-order:] for melody in mode_melodies.values()]

        # output
        output = {
            "initials": initials,
            "chains": chains,
            "finals": finals,
        }
        with open(output_filename, "w") as outfile:
            json.dump(output, outfile)
