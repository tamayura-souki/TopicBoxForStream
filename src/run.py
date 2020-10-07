import sys
import json
import tkinter as tk

from TopicBox import TopicBox
import config_main

config = json.load(open("config.json", 'r', encoding='utf-8', errors='ignore'))

config["TopicBoxConfig"] = config_main.main(config["TopicBoxConfig"])

tb = TopicBox(config)
tb.main()