from tkinter import *
import math
import os

screenReduce = .9

class Application(Frame):
    def getChoice(self, choice):


    def buttonSetup(self, sw, sh):
        # QUIT button
        self.QUIT = Button(self, text = "Quit", command = self.quit, bg = "#9bc6b0", fg = "black", width = 10, height = 2, bd = 0, activebackground = "#2c5942")
        self.QUIT.pack(side = BOTTOM)

        # Drop down to load a file
        self.files_and_dirs = [file for file in os.listdir("books/") if os.path.isdir(file) or file.endswith(('TXT', 'txt'))]
        self.files_and_dirs.sort()
        self.var = StringVar()
        self.var.set(self.files_and_dirs[0])
        self.loadFile = OptionMenu(self, self.var, *self.files_and_dirs)
        self.loadFile.config(bg = "#9bc6b0", fg = "black", width = 10, height = 2, bd = 0)
        self.loadFile.pack()

        # Click once choice is in drop down menu.
        self.choose = Button(self, text = "Load txt", command = lambda: self.getChoice(self.var.get()), bg = "#9bc6b0", fg = "black", width = 10, height = 2, bd = 0, activebackground = "#2c5942")
        self.choose.pack(side = BOTTOM)

    def createWidgets(self):
        sw = root.winfo_screenwidth()
        sh = root.winfo_screenheight()
        self.buttonSetup(sw, sh)

    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

root = Tk()
app = Application(master = root)
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(str(math.floor(screen_width * screenReduce)) + "x" + str(math.floor(screen_height * screenReduce)))
root.configure(background="#2c5942")
app.mainloop()
root.destroy()
