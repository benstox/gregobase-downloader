#!/usr/bin/env python3

import os
import random
import re
import requests
import time

from bs4 import BeautifulSoup

OUTPUT_DIR = "gabc"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)


# 1961 Liber Usualis link
url = "https://gregobase.selapa.net/source.php?id=3"
r = requests.get(url)
s = BeautifulSoup(r.content, "lxml")

links = s.select("#content > table a")

for link in links:
    href = link.get("href").replace("chant", "download")
    id_no = href.split("id=")[1]
    name = link.text.lower()
    for char in "().,: ":
        name = name.replace(char, "_")
    filename = "{0}_{1}.gabc".format(name, id_no)
    filename = re.sub(r"(_)(?=_)", "", filename)
    url = "https://gregobase.selapa.net/{}&format=gabc".format(href)
    r = requests.get(url)
    with open("{0}/{1}".format(OUTPUT_DIR, filename), "w") as outfile:
        outfile.write(r.text)
    time.sleep(random.randrange(6))
