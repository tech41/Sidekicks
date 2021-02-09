# pattern_builder: Tool for creating spell patterns and reading/writing to the Sidekicks CSV
import tkinter as tk
import pandas                 # read/write CSV

class Square(tk.Button):
    def __init__(self, master, myRow, myCol):
        self.counter = 0
        self.colorList = ["white", "blue", "green", "yellow"]
        initColorIdx = 0
        tk.Button.__init__(self, master, bg=self.colorList[initColorIdx], command=self.update_color) # could also use super().__init__()
        self.config(height = 2, width = 5)
        self.grid(row = myRow, column = myCol)

    def update_color(self):
        counter = self.counter;
        counter += 1
        if counter > 3:
            counter = 0
        self.config(bg = self.colorList[counter])
        self.counter = counter

class PatternFrame(tk.Frame):
    def __init__(self, master, myRow, myCol):
        tk.Frame.__init__(self, master)
        self.grid(row = myRow, column = myCol)
        self.config(height = 400, width = 400)
        self.config(bd = 1, relief = "raised")
        self.addSquares()
        
    def addSquares(self):
        numSide = 5
        for r in range(numSide):
            for c in range(numSide):
                self.square = Square(self, r, c)
     
        

class PatternBuilderTool:
    def __init__(self, master):
        self.master = master
        master.title("Sidekicks: Pattern Builder")
        master.geometry('1000x500')

        self.label = tk.Label(master, text="Simple pattern")
        self.label.grid(row = 1, column = 1)
        
        self.frameSimple = PatternFrame(master, 2, 1)
        self.frameSpacer = tk.Frame(master, height = 400, width = 100)
        self.frameSpacer.grid(row = 2, column = 2)
        self.frameComplex = PatternFrame(master, 2, 3)
        
        sk = pandas.read_csv('sidekicksDeck.csv', index_col = 'ID')
        print(sk["Name"][1])
        
root = tk.Tk()
patternBuilder = PatternBuilderTool(root)
root.mainloop()