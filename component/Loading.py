from tkinter import Label, Frame


class Loading(Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.master = master
        self.text = kw['text']
        self.start()

    def start(self):
        # 创建加载中文本
        self.label = Label(self, text=self.text)
        self.pack(padx=10, pady=10)
        # 更新加载中文本
        self.label.config(text=self.text)
        # 启动动画更新
        self.updateAnimation()

    def updateAnimation(self):
        current_text = self.label.cget("text")
        if current_text.endswith("..."):
            current_text = current_text[:-3]
        else:
            current_text += "."
        self.label.config(text=current_text)

        # 使用 after 方法设置动画更新间隔时间（毫秒）
        self.label.after(500, self.updateAnimation)
