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

class Spacer(tk.Frame):
    def __init__(self, master, myRow, myCol):
        tk.Frame.__init__(self, master)
        self.grid(row = myRow, column = myCol)
        self.config(height = 400, width = 50)
     
class PatternBuilderTool:
    def __init__(self, master):
        self.master = master
        master.title("Sidekicks: Pattern Builder")
        master.geometry('1000x500')
        
        cardData = pandas.read_csv('sidekicksDeck.csv', index_col = 'ID')
        #print(cardData["Name"])        

        self.label = tk.Label(master, text="Simple pattern")
        self.label.grid(row = 1, column = 1)
        
        # Listbox containing card names
        self.cardList = tk.Listbox(master)
        self.cardList.grid(row = 2, column = 1)
        for card in cardData["Name"]:
            self.cardList.insert(tk.END, card)
        self.cardList.bind('<<ListboxSelect>>', self.select_card)
        self.cardData = cardData

        self.spacer1 = Spacer(master, 2, 2)
        self.frameSimple = PatternFrame(master, 2, 3)
        self.spacer2 = Spacer(master, 2, 4)
        self.frameComplex = PatternFrame(master, 2, 5)
        
    def select_card(self):
        print("Calling method from top")
        cardIdx = self.cardList.curselection()
        print(cardIdx)
        
        # get index of current selection
        
        # read CSV pattern columns for index
        
        # convert nanDeck format to python
        
        # update strength text according to CSV (counting how many grids of that type)
        
        # update grid colors according to CSV
        
        
        
root = tk.Tk()
patternBuilder = PatternBuilderTool(root)
root.mainloop()