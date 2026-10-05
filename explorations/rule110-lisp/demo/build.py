"""Assemble glider_event_engine.html from page.html, engine.js and the data
files (scenes.json from extract_scenes.py; three_events.json from
data/tm_three_v2_gas.log)."""
import json
import os

here = os.path.dirname(os.path.abspath(__file__))


def read(name):
    with open(os.path.join(here, name)) as fh:
        return fh.read()


page = read("page.html").replace("/*ENGINE*/", read("engine.js"))
scenes = json.loads(read("scenes.json"))
page = page.replace("/*SCENES*/", json.dumps({k: {"cells": v["cells"], "T": v["T"]}
                                             for k, v in scenes.items()}))
page = page.replace("/*EVENTS*/", read("three_events.json").strip())
with open(os.path.join(here, "glider_event_engine.html"), "w") as fh:
    fh.write(page)
print(f"glider_event_engine.html: {len(page)} bytes")
