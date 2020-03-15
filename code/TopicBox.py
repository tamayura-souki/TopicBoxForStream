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

        self.choice_dicts = []
        for i in range(self.box_config["topic_num"]):
            choice_frame = ttk.Frame(self.root, borderwidth=1, relief=tk.GROOVE)
            choice_frame.pack(ipadx=5, ipady=5, expand=1, side=tk.TOP)

            line_d = {}
            tk.Label(choice_frame, text=f"No.{i+1}:", font=font)\
                .pack(expand=1, side=tk.LEFT)

            line_d["topic"] = tk.StringVar()
            tk.Label(choice_frame, textvariable=line_d["topic"], font=font, width=22)\
                .pack(expand=1, side=tk.LEFT)

            line_d["votes_n"] = tk.StringVar()
            tk.Label(choice_frame, textvariable=line_d["votes_n"], font=font, width=5)\
                .pack(expand=1, side=tk.LEFT)

            line_d["is_check"] = tk.BooleanVar()
            tk.Checkbutton(choice_frame, variable=line_d["is_check"])\
                .pack(expand=1, side=tk.LEFT)

            self.choice_dicts.append(line_d)

        # 1番下の部分
        self.bottom = {}
        self.bottom["frame"] = ttk.Frame(self.root)
        self.bottom["frame"].pack(expand=1, fill=tk.BOTH, side=tk.TOP)
        self.bottom["all_votes_n"] = tk.Label(self.bottom["frame"], font=font, relief=tk.GROOVE)
        self.bottom["all_votes_n"].pack(expand=1, fill=tk.BOTH, side=tk.LEFT)
        self.bottom["start"] = tk.Button(self.bottom["frame"], command=self.start, text="Start", font=font, borderwidth=5)
        self.bottom["start"].pack(expand=1, fill=tk.BOTH, padx=5, pady=5, side=tk.LEFT)

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
            self.choice_dicts[i]["votes_n"].set(self.counter[i])

        self.bottom["start"]["text"] = "Start"
        self.bottom["start"]["command"] = self.start

    def start(self):
        for i in range(self.box_config["topic_num"]):
            if(self.box_config["topic_num"] >= len(self.topics)):
                continue

            if(self.choice_dicts[i]["is_check"].get()):
                del self.topics[i]

        self.reset()

        self.bottom["start"]["text"] = "Stop"
        self.bottom["start"]["command"] = self.stop

    def reset(self):
        self.counter = [0] * self.box_config["topic_num"]
        self.votes_n = 0

        random.shuffle(self.topics)

        for i in range(self.box_config["topic_num"]):
            self.choice_dicts[i]["topic"].set(f"「{self.topics[i]}」")
            self.choice_dicts[i]["votes_n"].set("???")
            self.choice_dicts[i]["is_check"].set(False)

        self.bottom["all_votes_n"]["text"] = f"投票数:{self.votes_n}"

    def main(self):
        self.root.mainloop()
        self.livechat.terminate()