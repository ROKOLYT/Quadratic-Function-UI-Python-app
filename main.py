import tkinter as tk
from PIL import Image, ImageTk
import tkinter.font as FontTk
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math
import re
import PIL.Image

value = ''
p2 = ''
p3 = ''
backgroundcolor = "#33b857"


def ToBeReplaced(string):
    disallowed_characters = ['sqrt', '^', ':']
    equivalent = ['math.sqrt', '**', '/']
    string = string.strip()
    for i in range(len(disallowed_characters)):
        string = string.replace(disallowed_characters[i], equivalent[i])
    return string


# noinspection PyBroadException
def coefficients():
    global value
    place_holder = value
    coef = ['', '', '', False]
    if 'x**2' in place_holder:
        # noinspection PyBroadException
        try:
            coef[1] = re.search(r'xffffff2(.*)fffx', place_holder.replace('*', 'fff'))
            coef[1] = coef[1].group(1).replace('fff', '*')
        except:
            pass
        if coef[1] is None:
            coef[1] = '1'
        if '*x' not in place_holder or len(place_holder.split('*x')) == 2:
            coef[1] = '0'

        # noinspection PyBroadException
        try:
            coef[0] = place_holder.split('*x**')[0]
            if coef[0] == place_holder:
                coef[0] = '1'
        except:
            coef[0] = '1'
        try:
            coef[2] = place_holder.split('*x')[2]
        except:
            try:
                coef[2] = place_holder.split('*x')[1]
                if '**' in coef[2] and coef[1] != '0':
                    coef[2] = '0'
                else:
                    coef[2] = coef[2].replace('**2', '')

            except:
                coef[2] = '0'
        print(coef)
        for i in range(3):
            coef[i] = eval(coef[i])
        coef[3] = True
    elif ')**2' in place_holder:
        coef[0] = eval(place_holder.split('*(x')[0])
        coef[1] = re.search(r'x(.*)bracketffffff2', place_holder.replace('*', 'fff').replace(')', 'bracket'))
        coef[1] = eval(coef[1].group(1))
        coef[1] = -coef[1]
        coef[2] = eval(place_holder.split(')**2')[1])
        print(coef)



    return coef


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
        self.label = tk.Label(self, text="Please enter your equation\n equation MUST follow one of these templates:\n a*x^2+b*x+c\n a*(x-p)^2+q", bg=backgroundcolor)
        self.label.configure(font=self.myFont)
        self.label.pack(side="top", fill="both", expand=True)
        self.entry1 = tk.Entry(self, bg=backgroundcolor)
        self.entry1.bind("<Return>", self.onReturn)
        self.entry1.place(x=440, y=200, height=30, width=300)

    def onReturn(self, event):
        global value, p2
        value = self.entry1.get()
        # noinspection PyTypeChecker
        Page2.drawGraph(p2)


class Page2(Page):
    def __init__(self, *args, **kwargs):
        global value, backgroundcolor
        Page.__init__(self, *args, **kwargs)
        self.label = tk.Label(self, text="This is page 2", bg=backgroundcolor)
        self.label.pack(side="top", fill="both", expand=True)
        self.x = 0
        self.graph = 0
        self.coef = []
        self.fig = plt.figure(facecolor=backgroundcolor, figsize=(14.5, 8.15625))
        self.ax = self.fig.add_subplot(1, 1, 1)

    def drawGraph(self):
        global value, p3
        self.x = np.linspace(-10, 10, 300)
        x = self.x
        value = ToBeReplaced(value)
        y = eval(value)
        self.fig = plt.figure(facecolor=backgroundcolor, figsize=(14.5, 8.15625))
        self.ax = self.fig.add_subplot(1, 1, 1)
        self.ax.spines['left'].set_position('center')
        self.ax.spines['bottom'].set_position('zero')
        self.ax.spines['right'].set_color('none')
        self.ax.spines['top'].set_color('none')
        self.ax.xaxis.set_ticks_position('bottom')
        self.ax.yaxis.set_ticks_position('left')
        self.ax.set_facecolor(backgroundcolor)

        plt.plot(x, y)
        plt.grid()
        graph = FigureCanvasTkAgg(self.fig, master=self)
        graph.draw()
        graph.get_tk_widget().place(in_=self, x=-150, y=-50)
        self.graph = graph
        self.coef = coefficients()
        # noinspection PyTypeChecker
        Page3.answers(p3, self.coef)


# noinspection PyBroadException
class Page3(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.label0 = tk.Label(self, text="", bg=backgroundcolor)
        self.label0.pack(side="top", fill="both", expand=True)
        self.label = tk.Label()
        self.labelVertex = tk.Label()
        self.label_placed = False

    def answers(self, coef):
        global value
        if coef[3] is False:
            a = coef[0]
            b = -2*a*coef[1]
            c = coef[1]**2*a+coef[2]
        elif coef[3] is True:
            a = coef[0]
            b = coef[1]
            c = coef[2]
        delta = b ** 2 - 4 * a * c
        if delta > 0:
            x1 = (-b - math.sqrt(delta)) / (2 * a)
            x2 = (-b + math.sqrt(delta)) / (2 * a)
            p = (x1 + x2) / 2
            q = (-delta) / (4 * a)
            print(f'Vertex ({p} , {q})')
        elif delta == 0:
            x1 = (-b) / (2 * a)
            x2 = 'n/a'
            p = x1
            q = (-delta) / (4 * a)
            print(f'Vertex ({p} , {q})')

        else:
            x1 = 'n/a'
            x2 = 'n/a'
            p = (-b) / (2 * a)
            q = (-delta) / (4 * a)
            print(f'Vertex ({p} , {q})')
        try:
            x1 = round(float(x1), 4)
        except:
            pass
        try:
            x2 = round(float(x2), 4)
        except:
            pass
        if self.label_placed is False:
            self.label = tk.Label(self, text=f'x1 = {x1} and x2 = {x2}\n delta = {delta}', bg=backgroundcolor,
                                      font=self.myFont)
            self.label.pack(side="top", fill="both", expand=True)
            self.labelVertex = tk.Label(self, text=f'Vertex ({p} , {q})', bg=backgroundcolor, font=self.myFont)
            self.labelVertex.pack(side="top", fill="both", expand=True)
            self.label_placed = True
        else:
            self.label.destroy()
            self.labelVertex.destroy()
            self.label = tk.Label(self, text=f'x1 = {x1} and x2 = {x2}\n delta = {delta}', bg=backgroundcolor,
                                      font=self.myFont)
            self.label.pack(side="top", fill="both", expand=True)
            self.labelVertex = tk.Label(self, text=f'Vertex ({p} , {q})', bg=backgroundcolor, font=self.myFont)
            self.labelVertex.pack(side="top", fill="both", expand=True)


class Page4(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.label = tk.Label(self, text='', bg=backgroundcolor)
        self.label.pack(side="top", fill="both", expand=True)
        mylist = ['x1', 'x2', 'p', 'q', 'a', 'b', 'c', 'delta', 'x', 'y']
        for i in mylist:
            i = i
            self.i = tk.Entry(self, width=5)
            self.i.insert(0, i)
            self.i.bind('<Button-1>', lambda event, entry=self.i:
                              self.deleteEntry(entry))
            self.i.pack(side="top")

    def deleteEntry(self, entry):
        entry.delete(0, 'end')


class PageS(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.label = tk.Label(self, text="This is settings page", bg=backgroundcolor, font=self.myFont)
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
        global p2, p3
        tk.Frame.__init__(self, *args, **kwargs)
        p = Page(self)
        p1 = Page1(self)
        p2 = Page2(self)
        p3 = Page3(self)
        p4 = Page4(self)
        ps = PageS(self)

        self.p = p
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4
        self.ps = ps

        buttonframe = tk.Frame(self)
        buttonframe.config(bg="#2d7540")
        self.container = tk.Frame(self)
        buttonframe.pack(side="left", fill="y", expand=False)
        self.container.pack(side="top", fill="both", expand=True)

        self.home = ImageTk.PhotoImage(PIL.Image.open('home.png').resize((80, 80)))
        self.graph = ImageTk.PhotoImage(PIL.Image.open('graph.png').resize((80, 80)))
        self.equal = ImageTk.PhotoImage(PIL.Image.open('equal.png').resize((80, 80)))
        self.settings = ImageTk.PhotoImage(PIL.Image.open('settings.png').resize((80, 80)))

        p1.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)
        p3.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)
        p4.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)
        ps.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)

        b1 = tk.Button(buttonframe, image=self.home, command=p1.show, bg="#2d7540",
                       relief='flat', activebackground="#33b857")
        b2 = tk.Button(buttonframe, image=self.graph, command=p2.show, bg="#2d7540",
                       relief='flat', activebackground="#33b857")
        b3 = tk.Button(buttonframe, image=self.equal, command=p3.show, bg="#2d7540",
                       relief='flat', activebackground="#33b857")
        b4 = tk.Button(buttonframe, text='Page 4', command=p4.show, bg="#2d7540",
                       relief='flat', activebackground="#33b857")
        bs = tk.Button(buttonframe, image=self.settings, command=ps.show, bg="#2d7540",
                       relief='flat', activebackground="#33b857")

        b1.pack(side="top")
        b2.pack(side="top")
        b3.pack(side="top")
        b4.pack(side="top")
        bs.pack(side="bottom")
        p1.show()

    def changecolor(self, color):
        global root
        self.p1.label.config(bg=color)
        self.p1.entry1.config(bg=color)
        self.p3.label0.config(bg=color)
        self.p3.label.config(bg=color)
        self.p3.labelVertex.config(bg=color)
        self.ps.label.config(bg=color)
        self.ps.entrycolor.config(bg=color)
        try:
            MainView.overdrawgraph(self, color)
        except:
            self.p2.label.config(bg=color)

    def overdrawgraph(self, color):
        global value, p3
        self.p2.x = np.linspace(-10, 10, 300)
        x = self.p2.x
        value = ToBeReplaced(value)
        y = eval(value)
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


if __name__ == "__main__":
    root = tk.Tk()
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("1280x720")
    root.config(bg="#2d7540")
    root.wm_title("Quadratic function")
    root.mainloop()
