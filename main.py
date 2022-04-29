import tkinter as tk
from PIL import Image, ImageTk
import tkinter.font as FontTk
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from math import sqrt
import PIL.Image
from MyFunctions import missingVariables, ToBeReplaced, coefficients, deleteEntry

value = ''
backgroundcolor = "#33b857"


class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.myFont = FontTk.Font(family="Helvetica", size=36, weight="bold")

    def show(self):
        self.lift()


class Page1(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        global backgroundcolor
        self.label = tk.Label(self,
                              text="Please enter your equation\n equation MUST follow one of these templates:\n a*x^2+b*x+c\n a*(x-p)^2+q",
                              bg=backgroundcolor)
        self.label.configure(font=self.myFont)
        self.label.pack(side="top", fill="both", expand=True)
        self.entry1 = tk.Entry(self, bg=backgroundcolor)
        self.entry1.bind("<Return>", self.onReturn)
        self.entry1.place(x=440, y=200, height=30, width=300)

    def onReturn(self, event):
        global value, main
        value = self.entry1.get()
        MainView.drawGraph(main, None)


class Page2(Page):
    def __init__(self, *args, **kwargs):
        global value, backgroundcolor
        Page.__init__(self, *args, **kwargs)
        self.label = tk.Label(self, text="After you enter your equation\n a graph will appear on this page",
                              bg=backgroundcolor, font=self.myFont)
        self.label.pack(side="top", fill="both", expand=True)
        self.x = 0
        self.graph = 0
        self.coef = []
        self.fig = plt.figure(facecolor=backgroundcolor, figsize=(14.5, 8.15625))
        self.ax = self.fig.add_subplot(1, 1, 1)


class Page3(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.label = tk.Label(self, text='', bg=backgroundcolor, font=self.myFont)
        self.label.pack(side="top", fill="both", expand=True)
        self.givenVariables = {}
        self.namesInDict = dict.fromkeys(['a', 'b', 'c', 'p', 'q', 'x1', 'x2', 'delta'])
        self.CreateEntriesForDataInput()
        self.result = None

    def CreateEntriesForDataInput(self):
        y = 5
        x = 5
        for k in self.namesInDict:
            self.namesInDict[k] = tk.Entry(self, width=5, font=self.myFont, bg=backgroundcolor)
            self.namesInDict[k].insert(0, str(k))
            self.namesInDict[k].bind('<Button-1>', lambda event, entry=self.namesInDict[k]:
            deleteEntry(entry))
            self.namesInDict[k].bind('<Return>', lambda event, variable=self.namesInDict[k], name=str(k):
            self.editDict(variable, name))
            self.namesInDict[k].place(in_=self, x=x, y=y)
            y += 65

    def editDict(self, variable, data):
        self.givenVariables[data] = float(variable.get())
        try:
            self.result = missingVariables(self.givenVariables)
            if not self.result:
                self.label.config(text='Not enough data')
            else:
                self.result.update(self.givenVariables)
                try:
                    result = self.result
                    self.label.config(text=f"a = {result['a']}\nb = {result['b']}\nc = {result['c']}\n"
                                           f"p = {result['p']}\nq = {result['q']}\nx1 = {result['x1']}\n"
                                           f"x2 = {result['x2']}\ndelta = {result['delta']}")
                    MainView.drawGraph(main, result)
                except KeyError:
                    self.label.config(text='Not enough data')
        except NotImplementedError:
            self.label.config(text='Not enough data')


class PageS(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.label = tk.Label(self, text="Here you can change the background color\n use hex or name of a color",
                              bg=backgroundcolor, font=self.myFont)
        self.label.pack(side="top", fill="both", expand=True)
        self.entrycolor = tk.Entry(self, bg=backgroundcolor)
        self.entrycolor.bind("<Return>", self.setcolor)
        self.entrycolor.place(x=440, y=200, height=30, width=300)

    def setcolor(self, event):
        global main, backgroundcolor
        entry = self.entrycolor.get()
        self.entrycolor.delete(0, 'end')
        backgroundcolor = entry
        MainView.changecolor(main, backgroundcolor)


class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        p = Page(self)
        p1 = Page1(self)
        p2 = Page2(self)
        p3 = Page3(self)
        ps = PageS(self)

        self.p = p
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.ps = ps

        buttonframe = tk.Frame(self)
        buttonframe.config(bg="#2d7540")
        self.container = tk.Frame(self)
        buttonframe.pack(side="left", fill="y", expand=False)
        self.container.pack(side="top", fill="both", expand=True)

        self.home = ImageTk.PhotoImage(PIL.Image.open(r'icons\home.png').resize((80, 80)))
        self.graph = ImageTk.PhotoImage(PIL.Image.open(r'icons\graph.png').resize((80, 80)))
        self.equal = ImageTk.PhotoImage(PIL.Image.open(r'icons\equal.png').resize((80, 80)))
        self.settings = ImageTk.PhotoImage(PIL.Image.open(r'icons\settings.png').resize((80, 80)))

        p1.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)
        p3.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)
        ps.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)

        b1 = tk.Button(buttonframe, image=self.home, command=p1.show, bg="#2d7540",
                       relief='flat', activebackground="#33b857")
        b2 = tk.Button(buttonframe, image=self.graph, command=p2.show, bg="#2d7540",
                       relief='flat', activebackground="#33b857")
        b3 = tk.Button(buttonframe, image=self.equal, command=p3.show, bg="#2d7540",
                       relief='flat', activebackground="#33b857")
        bs = tk.Button(buttonframe, image=self.settings, command=ps.show, bg="#2d7540",
                       relief='flat', activebackground="#33b857")

        b1.pack(side="top")
        b2.pack(side="top")
        b3.pack(side="top")
        bs.pack(side="bottom")
        p1.show()

    def answers(self, coef):
        global value
        dict_with_coefs = {}
        if coef[3] is False:
            dict_with_coefs['a'] = coef[0]
            dict_with_coefs['b'] = -2 * dict_with_coefs['a'] * coef[1]
            dict_with_coefs['c'] = coef[1] ** 2 * dict_with_coefs['a'] + coef[2]
        else:
            dict_with_coefs['a'] = coef[0]
            dict_with_coefs['b'] = coef[1]
            dict_with_coefs['c'] = coef[2]
        result = missingVariables(dict_with_coefs)
        result.update(dict_with_coefs)
        self.p3.label.config(text=f"a = {result['a']}\nb = {result['b']}\nc = {result['c']}\n"
                                  f"p = {result['p']}\nq = {result['q']}\nx1 = {result['x1']}\n"
                                  f"x2 = {result['x2']}\ndelta = {result['delta']}")

    def changecolor(self, color):
        # noinspection PyBroadException
        self.p1.label.config(bg=color)
        self.p1.entry1.config(bg=color)
        self.p3.label.config(bg=color)
        self.ps.label.config(bg=color)
        self.ps.entrycolor.config(bg=color)
        for k in self.p3.namesInDict:
            self.p3.namesInDict[k].config(bg=color)
        try:
            MainView.overdrawgraph(self, color)
        except SyntaxError:
            self.p2.label.config(bg=color)

    def overdrawgraph(self, color):
        global value
        self.p2.x = np.linspace(-10, 10, 300)
        x = self.p2.x
        if self.p3.result is None:
            value = ToBeReplaced(value)
            y = eval(value)
        else:
            result = self.p3.result
            y = result['a'] * (x - result['p']) ** 2 + result['q']
        self.CreateGraph(color, x, y)

    def CreateGraph(self, color, x, y):
        self.p2.fig = plt.figure(facecolor=color, figsize=(14.5, 8.15625))
        self.p2.ax = self.p2.fig.add_subplot(1, 1, 1)
        self.p2.ax.spines['left'].set_position('center')
        self.p2.ax.spines['bottom'].set_position('zero')
        self.p2.ax.spines['right'].set_color('none')
        self.p2.ax.spines['top'].set_color('none')
        self.p2.ax.xaxis.set_ticks_position('bottom')
        self.p2.ax.yaxis.set_ticks_position('left')
        self.p2.ax.set_facecolor(color)
        plt.plot(x, y)
        plt.grid()
        graph = FigureCanvasTkAgg(self.p2.fig, master=self.p2)
        graph.draw()
        graph.get_tk_widget().place(in_=self.p2, x=-150, y=-50)

    def drawGraph(self, result):
        global value, main
        self.p2.x = np.linspace(-10, 10, 300)
        x = self.p2.x
        if result is None:
            value = ToBeReplaced(value)
            y = eval(value)
        else:
            y = result['a'] * (x - result['p']) ** 2 + result['q']
        self.CreateGraph(backgroundcolor, x, y)
        self.p2.coef = coefficients(value)
        # noinspection PyTypeChecker
        if result is None:
            MainView.answers(main, self.p2.coef)


if __name__ == "__main__":
    root = tk.Tk()
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("1280x720")
    root.config(bg="#2d7540")
    root.wm_title("Quadratic function")
    root.mainloop()
