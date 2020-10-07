import sys
import traceback
import re
import tkinter as tk

def main(config):
    root = tk.Tk()
    root.title("配信のURLを入力")
    root.geometry("330x50")

    def ok():
        config["users_add"] = users_add.get()
        config["vote_lim"] = vote_lim.get()
        config["video_id"] = txt.get()
        if '/' in config["video_id"]:
            config["video_id"] = re.search(
                r"[\?\&]v=([^&]+)", config["video_id"]
            )
            if config["video_id"] is None:
                # logger.error("Invalid video id")
                return None

            config["video_id"] = config["video_id"].group(1)
        root.destroy()

    def end():
        root.destroy()
        sys.exit(0)

    lbl = tk.Label(text='URL')
    lbl.place(x=10, y=10)

    txt = tk.Entry()
    txt.place(x=40, y=10)
    txt.insert(tk.END, config["video_id"])

    enter_btn = tk.Button(text="Ok", command=ok)
    enter_btn.place(x=170, y=5)

    users_add = tk.BooleanVar()
    users_add.set(config["users_add"])
    tk.Checkbutton(
        text="users_add", variable=users_add, indicatoron=False
    ).place(x=200, y=10)

    vote_lim = tk.BooleanVar()
    vote_lim.set(config["vote_lim"])
    tk.Checkbutton(
        text="vote_lim", variable=vote_lim, indicatoron=False
    ).place(x=270, y=10)

    root.protocol("WM_DELETE_WINDOW", end)
    root.mainloop()

    return config