from typing import List, Dict

import random
import tkinter as tk
from tkinter import ttk

from pytchat import LiveChat

from utils import *

class TopicBox:
    def __init__(self, config_dict, is_test:bool=False):
        self.ui_config  = config_dict["UI_config"]
        self.box_config = config_dict["TopicBoxConfig"]

        self.counter = [0] * self.box_config["topic_num"]
        self.votes_n = 0
        self.topics  = self.box_config["initial_topic"]

        self.once_vote = True
        self.voted_users = []

        self.create_ui()
        self.reset()

        self.livechat = LiveChat(
            video_id=self.box_config["video_id"], callback=self.process_chat
        ) if not is_test else None

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
            choice_frame.pack(ipadx=10, ipady=10, expand=1, side=tk.TOP)

            # named tuple で書き換えかな
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
            tk.Checkbutton(choice_frame, text="除外", variable=line_d["is_check"], indicatoron=False)\
                .pack(padx=10, ipadx=10, ipady=10, expand=1, side=tk.LEFT)

            self.choice_dicts.append(line_d)

        # 1番下の部分
        # named tuple で書き換えかな
        self.bottom = {}
        self.bottom["frame"] = ttk.Frame(self.root)
        self.bottom["frame"].pack(expand=1, fill=tk.BOTH, side=tk.TOP)
        self.bottom["all_votes_n"] = tk.Label(self.bottom["frame"], font=font, relief=tk.GROOVE)
        self.bottom["all_votes_n"].pack(expand=1, fill=tk.BOTH, side=tk.LEFT)
        self.bottom["start"] = tk.Button(self.bottom["frame"], command=self.start, text="Start", font=font, borderwidth=5)
        self.bottom["start"].pack(expand=1, fill=tk.BOTH, padx=5, pady=5, side=tk.LEFT)

    def update_votes_n(self):
        self.bottom["all_votes_n"]["text"] = f"投票数:{self.votes_n}"

    def add_topic(self, topic_text:str):
        self.topics.append(topic_text)

    def get_votes(self, votes:str):
        for i in range(self.box_config["topic_num"]):
            n = votes.count(str(i+1))
            self.counter[i] += n
            self.votes_n += n
        self.update_votes_n()

    def get_avote(self, vote:str, user:str):
        if user in self.voted_users:
            return

        for i in range(self.box_config["topic_num"]):
            if not str(i+1) in vote:
                continue
            self.counter[i] += 1
            self.votes_n += 1
            self.voted_users.append(user)
            break
        self.update_votes_n()

    def process_chat(self, chatdata):
        # 先に chat list を作れば高階関数でできる?
        # if else は配列を2つに分割して
        for c in chatdata.items:
            chat = c.message
            if "/add" in chat:
                self.add_topic(chat.strip("/add").strip())

            else:
                if self.once_vote:
                    self.get_avote(chat, c.author.channelId)
                else:
                    self.get_votes(chat)

    def stop(self):
        for i in range(self.box_config["topic_num"]):
            self.choice_dicts[i]["votes_n"].set(self.counter[i])

        self.bottom["start"]["text"] = "Start"
        self.bottom["start"]["command"] = self.start

    def start(self):
        for i in range(self.box_config["topic_num"]):
            if(self.choice_dicts[i]["is_check"].get()):
                if(self.box_config["topic_num"] >= len(self.topics)):
                    self.topics[i] = "ネタ切れ"
                else:
                    self.topics.pop(i)

        self.reset()

        self.bottom["start"]["text"] = "Stop"
        self.bottom["start"]["command"] = self.stop

    def reset(self):
        self.counter = [0] * self.box_config["topic_num"]
        self.votes_n = 0
        self.voted_users = []

        random.shuffle(self.topics)

        for i in range(self.box_config["topic_num"]):
            self.choice_dicts[i]["topic"].set(f"「{self.topics[i]}」")
            self.choice_dicts[i]["votes_n"].set("???")
            self.choice_dicts[i]["is_check"].set(False)

        self.update_votes_n()

    def main(self):
        self.root.mainloop()
        if self.livechat is not None:
            self.livechat.terminate()