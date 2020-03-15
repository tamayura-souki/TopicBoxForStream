import sys
import json
import tkinter as tk

from TopicBox import TopicBox

# ----
# コメントのIDを取得する部分書く
# ----

config = json.load(open("config.json", 'r', encoding='utf-8', errors='ignore'))
tb = TopicBox(config)
tb.main()