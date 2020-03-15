from typing import List, Dict

import random
import tkinter as tk
from tkinter import ttk

from pytchat import LiveChat

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG, filename="log.txt")


class TopicBox:
    def __init__(self, config_dict):
        self.ui_config  = config_dict["UI_config"]
        self.box_config = config_dict["TopicBoxConfig"]

        self.counter = [0] * self.box_config["topic_num"]
        self.votes_n = 0
        self.topics  = self.box_config["initial_topic"]

        self.create_ui()
        self.reset()

        self.livechat = LiveChat(video_id=self.box_config["video_id"], callback=self.process_chat)

    def create_ui(self):
        self.root = tk.Tk()
        self.root.title(self.ui_config["title"])
        self.root.geometry(self.ui_config["window_size"])

        font = (
            self.ui_config["font"]["family"],
            self.ui_config["font"]["size"]
        )

        # 1列分の要素 択の数だけつくる
        self.line_frame = ttk.Frame(self.root)
        self.line_frame.grid(row=0)
        self.line_dicts = []
        for i in range(self.box_config["topic_num"]):
            line_d = {}
            tk.Label(self.line_frame, text=f"No.{i+1}:", font=font)\
                .grid(row=i, column=0)

            line_d["topic"] = tk.StringVar()
            tk.Label(self.line_frame, textvariable=line_d["topic"], font=font, width=15)\
                .grid(row=i, column=1)

            line_d["votes_n"] = tk.StringVar()
            tk.Label(self.line_frame, textvariable=line_d["votes_n"], font=font, width=4)\
                .grid(row=i, column=2)

            line_d["is_check"] = tk.BooleanVar()
            tk.Checkbutton(self.line_frame, variable=line_d["is_check"])\
                .grid(row=i, column=3)

            self.line_dicts.append(line_d)

        # 1番下の部分
        self.bottom = {}
        self.bottom["frame"] = ttk.Frame(self.root)
        self.bottom["frame"].grid(row=1)
        self.bottom["all_votes_n"] = tk.Label(self.bottom["frame"], font=font)
        self.bottom["all_votes_n"].grid(row=0, column=0)
        self.bottom["start"] = tk.Button(self.bottom["frame"], command=self.start, text="Start", font=font)
        self.bottom["start"].grid(row=0, column=1)

    def process_chat(self, chatdata):
        for c in chatdata.items:
            if "/add" in c.message:
                self.topics.append(c.message.strip("/add").strip())
                continue

            for i in range(self.box_config["topic_num"]):
                n = c.message.count(str(i+1))
                self.counter[i] += n
                self.votes_n += n

            self.bottom["all_votes_n"]["text"] = f"投票数:{self.votes_n}"

    def stop(self):
        for i in range(self.box_config["topic_num"]):
            self.line_dicts[i]["votes_n"].set(self.counter[i])

        self.bottom["start"]["text"] = "Start"
        self.bottom["start"]["command"] = self.start

    def start(self):
        for i in range(self.box_config["topic_num"]):
            if(self.box_config["topic_num"] >= len(self.topics)):
                continue

            if(self.line_dicts[i]["is_check"].get()):
                del self.topics[i]

        self.reset()

        self.bottom["start"]["text"] = "Stop"
        self.bottom["start"]["command"] = self.stop

    def reset(self):
        self.counter = [0] * self.box_config["topic_num"]
        self.votes_n = 0

        random.shuffle(self.topics)

        for i in range(self.box_config["topic_num"]):
            self.line_dicts[i]["topic"].set(f"「{self.topics[i]}」")
            self.line_dicts[i]["votes_n"].set("???")
            self.line_dicts[i]["is_check"].set(False)

        self.bottom["all_votes_n"]["text"] = f"投票数:{self.votes_n}"

    def main(self):
        self.root.mainloop()
        self.livechat.terminate()