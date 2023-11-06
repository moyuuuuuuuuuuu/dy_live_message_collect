from tkinter import Toplevel, Frame, Label
from tkinter.ttk import Progressbar
import time


class Progress:
    def __init__(
            self,
            master=None,
            text="加载中",
            bg="gray",
            fg="white",
            mode="indeterminate",
            geometry=None
    ):
        progress_window = Toplevel(master=master)
        self.progress_window = progress_window
        progress_window.overrideredirect(True)
        # 自定义标题栏
        title_bar = Frame(progress_window, bg="gray")
        title_bar.pack(fill="x")
        # 创建标题栏标签
        title_label = Label(title_bar, text=text, bg=bg, fg=fg)
        title_label.pack(side="left", padx=10)
        if geometry:
            progress_window.geometry(geometry)

        # 创建进度条
        progress_bar = Progressbar(progress_window, length=200, mode=mode)
        progress_bar.pack(pady=20)
        progress_bar.start()

    def update_progress(progress_bar):
        while True:
            progress_bar['value'] += 1
            progress_bar.update()
            time.sleep(0.05)

    def close(self):
        self.progress_window.destroy()
