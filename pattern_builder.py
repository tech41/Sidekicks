# pattern_builder: Tool for creating spell patterns and reading/writing to the Sidekicks CSV
import tkinter as tk

class Square(tk.Button):
    def __init__(self, master):
        self.counter = 0
        self.colorList = ["white", "blue", "green", "yellow"]
        initColorIdx = 0
        tk.Button.__init__(self, master, bg=self.colorList[initColorIdx], command=self.update_color) # could also use super().__init__()
        #tk.Button.__init__(self, master, bg=initColor) # could also use super().__init__()
        self.config(height = 2, width = 5)

    def update_color(self):
        counter = self.counter;
        counter += 1
        if counter > 3:
            counter = 0
        self.config(bg = self.colorList[counter])
        self.counter = counter

class PatternFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        

class PatternBuilderTool:
    def __init__(self, master):
        self.master = master
        master.title("Sidekicks: Pattern Builder")
        master.geometry('1000x500')

        self.label = tk.Label(master, text="Simple pattern")
        self.label.pack()
        
        #self.square = tk.Button(master, height = 2, width = 5)
        self.square = Square(master)
        self.square.pack()

        
root = tk.Tk()
patternBuilder = PatternBuilderTool(root)
root.mainloop()