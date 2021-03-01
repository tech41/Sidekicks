# pattern_builder: Tool for creating spell patterns and reading/writing to the Sidekicks CSV
import tkinter as tk
import pandas         # read/write CSV
import re             # regular expressions

class Square(tk.Button):
    def __init__(self, master, myRow, myCol):
        self.counter = 0
        self.colorList = master.colorList
        initColorIdx = 0
        tk.Button.__init__(self, master, bg=self.colorList[initColorIdx], command=self.click_change_color) # could also use super().__init__()
        self.config(height = 2, width = 5)
        self.grid(row = myRow, column = myCol)

    def update_color(self, color):
        self.color = color
        self.config(bg = color)

    def click_change_color(self):
        counter = self.counter
        counter += 1
        if counter > 3:
            counter = 0
        thisColor = self.colorList[counter]
        self.update_color(thisColor)
        self.counter = counter

class PatternFrame(tk.Frame):
    def __init__(self, master, myRow, myCol):
        tk.Frame.__init__(self, master)
        self.numSide = 5
        self.grid(row = myRow, column = myCol)
        self.config(height = 400, width = 400)
        self.config(bd = 1, relief = "raised")
        self.colorList = master.colorList
        self.squareMat = self.add_squares(self.numSide)
        
    def add_squares(self, numSide):
        squareMat = []
        for r in range(numSide):
            row = []
            for c in range(numSide):
                row.append(Square(self, r, c))
            squareMat.append(row)
        return squareMat
                
    def blank_out_squares(self):
        squareMat = self.squareMat
        numSide = self.numSide
        for r in range(numSide):
            for c in range(numSide):
                s = squareMat[r][c]        
                s.update_color("white")

class Spacer(tk.Frame):
    def __init__(self, master, myRow, myCol):
        tk.Frame.__init__(self, master)
        self.grid(row = myRow, column = myCol)
        self.config(height = 400, width = 50)
     
class PatternBuilderTool:
    def __init__(self, master):
        self.master = master
        master.title("Sidekicks: Pattern Builder")
        master.geometry('1000x500+-1050+10')
        master.colorList = ["white", "green", "blue", "yellow"] # first color = blank/none
        
        cardData = pandas.read_csv('sidekicksDeck.csv', index_col = 'ID')

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
        self.patternLvl1 = PatternFrame(master, 2, 3)
        self.spacer2 = Spacer(master, 2, 4)
        self.patternLvl2 = PatternFrame(master, 2, 5)
    
    def parse_pattern_col(self, patternStr):

        dots = [m.start() for m in re.finditer('\.', patternStr)]
        if len(dots) > 0:
            rIdx = [dot - 1 for dot in dots]
            cIdx = [dot + 1 for dot in dots]
            
            rows = [int(patternStr[r])-1 for r in rIdx]
            cols = [int(patternStr[c])-1 for c in cIdx]
        else:
            rows = []
            cols = []

        return [rows, cols]
    
    def select_card(self, event):
        # get index of current selection
        cardIdx = self.cardList.curselection()
        csvIdx = cardIdx[0]
        print(cardIdx)
        print(csvIdx)
        cardData = self.cardData
        
        patternLvlList = [1, 2]
        colorList = ["green", "blue", "yellow"] # need to use list from root

        for lvl in patternLvlList:
            
            thisPattern = getattr(self, 'patternLvl%s' % (lvl))
            thisPattern.blank_out_squares()

            thisSquareMat = thisPattern.squareMat
           
            for color in colorList:
                colName = "Pattern_%s_%s" % (lvl, color)
                thisPattern =  cardData[colName][csvIdx+1]
                rowsCols = self.parse_pattern_col(thisPattern)
                rows = rowsCols[0]
                cols = rowsCols[1]
                for r, c in zip(rows, cols):
                    s = thisSquareMat[r][c]
                    s.update_color(color)
        
root = tk.Tk()
patternBuilder = PatternBuilderTool(root)
root.mainloop()