#!/usr/bin/env python3

import json
import os


folder = "melody"
melodies = {}
modes = ["mode_" + str(i) for i in list(range(1, 9))] + ["p", "unknown_mode"]
for mode in modes:
    melodies[mode] = {}
    mode_folder = "{}/{}".format(folder, mode)
    filenames = [filename for filename in os.listdir(mode_folder) if not filename.startswith(".")]
    for filename in filenames:
        with open("{}/{}".format(mode_folder, filename), "r") as f:
            melody = f.read()

        melodies[mode][filename] = melody

# add some extra things to tonus peregrinus
extra_peregrinus = {
    "psalm_tone": "hIhhh_hhgIhgf.gggg_gggdffe.d.",
    "nos_qui_vivimus": "cdffgg_hIhgfghhg.",
}
for key, value in extra_peregrinus.items():
    melodies["p"][key] = value

# add snatches of Tolkien & Swann's "Namarie"
namarie = {
    "1": "jkllllkjkijhig.h.",
    "2": "l_kjkj.jkl_llmkkkk.j.",
    "3": "llll_llll_llll.llll_llmkkj.",
    "4": "jkl_llll_lmkkj.",
    "5": "ll_llllnkk.l.",
    "6": "jkl_llllpolnmjml.jkl_llllpolnmjml.jkllllkjkijhigh.e.",
    "7": "jklllll_llmkj_k_j.",
    "8": "ll_llllnkk_l_lnkk.l.",
    "9": "ll_ll_l_lllkjk_j_lkjk.j.",
}
melodies["namarie"] = namarie

# output a big json file
with open("melodies.json", "w") as outfile:
    json.dump(melodies, outfile, indent=2)
