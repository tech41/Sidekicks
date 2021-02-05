# pattern_builder: Tool for creating spell patterns and reading/writing to the Sidekicks CSV
import tkinter as tk

class Square(tk.Button):
    def __init__(self, master):
        tk.Button.__init__(self, master)
        self.config(height = 2, width = 5)
        self.config(bg = "blue")

class PatternBuilderTool:
    def __init__(self, master):
        self.master = master
        master.title("Sidekicks: Pattern Builder")
        master.geometry('1000x500')

        self.label = tk.Label(master, text="Simple pattern")
        self.label.pack()
        
        #self.square = tk.Button(master, height = 2, width = 5)
        self.square = Square(master)
        self.square.config(bg = "blue")
        self.square.pack()

        
root = tk.Tk()
patternBuilder = PatternBuilderTool(root)
root.mainloop()