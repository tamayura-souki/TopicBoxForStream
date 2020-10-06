import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG, filename="log.txt")

import tkinter as tk
from tkinter import ttk
from typing import NamedTuple

class TopicElm(NamedTuple):
    topic:tk.StringVar
    votes_n:tk.StringVar
    is_check:tk.BooleanVar

class Bottom(NamedTuple):
    frame:ttk.Frame
    all_votes_n:tk.Label
    start:tk.Button