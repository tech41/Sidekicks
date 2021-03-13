# pattern_builder: Tool for creating spell patterns and reading/writing to the Sidekicks CSV
import tkinter as tk
import pandas         # read/write CSV
import re             # regular expressions

class PatternBuilderTool:
    def __init__(self, master):
        self.master = master
        master.title("Sidekicks: Pattern Builder")
        master.geometry('1000x500+-1050+10')
        master.colorList = ["white", "green", "blue", "yellow"] # first color = blank/none
        self.colorList = master.colorList
        # future - make # pattern levels dynamic, or read this list from existing pattern objects
        self.patternLvlList = [1, 2] 
        self.csvIdx = 1 # default initial value
        
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

        self.exportButton = tk.Button(master, text="Export to CSV", command=self.export_to_csv)

        self.spacer1 = Spacer(master, 2, 2)
        self.patternLvl1 = PatternFrame(master, 2, 3)
        self.spacer2 = Spacer(master, 2, 4)
        self.patternLvl2 = PatternFrame(master, 2, 5)
        self.spacer3 = Spacer(master, 2, 6)
        self.exportButton.grid(row=2, column=7)
        
        self.update_current_card() # use initial value
    
    def export_to_csv(self):
        self.update_current_cardData()
        cardData = self.cardData
        cardData.to_csv('sidekicksDeck.csv')
    
    def parse_pattern_col(self, patternStr):

        dots = [m.start() for m in re.finditer('\.', patternStr)]
        if len(dots) > 0:
            rIdx = [dot + 1 for dot in dots]
            cIdx = [dot - 1 for dot in dots]
            
            rows = [int(patternStr[r])-1 for r in rIdx]
            cols = [int(patternStr[c])-1 for c in cIdx]
        else:
            rows = []
            cols = []

        return [rows, cols]
    
    def update_current_cardData(self):
        # write the current GUI pattern back to cardData
        cardData = self.cardData
        oldIdx = self.csvIdx
        patternLvlList = self.patternLvlList
        colorList = self.colorList
        
        for lvl in patternLvlList:
            
            thisPattern = getattr(self, 'patternLvl%s' % (lvl))

            thisSquareMat = thisPattern.squareMat
            
            for color in self.colorList[1:]:
                colName = "Pattern_%s_%s" % (lvl, color)
                hasThisColor = 0
                rowColStr = ""
                for r in range(len(thisSquareMat)):
                    for c in range(len(thisSquareMat[r])):
                        s = thisSquareMat[c][r]
                        oldColor = s.color
                        if color == oldColor:
                            hasThisColor = 1
                            rCard = r+1
                            cCard = c+1
                            newStr = "{}.{}_".format(rCard, cCard)
                            rowColStr += newStr

                if hasThisColor:
                    cardData.at[oldIdx, colName] = rowColStr
                else:
                    cardData.at[oldIdx, colName] = "0"           
                        
    def update_current_card(self):
        cardData = self.cardData
        csvIdx = self.csvIdx
        patternLvlList = self.patternLvlList

        for lvl in patternLvlList:
            
            thisPattern = getattr(self, 'patternLvl%s' % (lvl))
            thisPattern.blank_out_squares()

            thisSquareMat = thisPattern.squareMat
           
            for color in self.colorList[1:]:
                colName = "Pattern_%s_%s" % (lvl, color)
                thisPattern = cardData[colName][csvIdx]
                rowsCols = self.parse_pattern_col(thisPattern)
                rows = rowsCols[1]
                cols = rowsCols[0]
                for r, c in zip(rows, cols):
                    s = thisSquareMat[c][r]
                    s.update_color(color)
                    
    def select_card(self, event):
        # update cardData with current pattern before moving to the next card
        self.update_current_cardData()
        
        # get index of current selection
        cardIdx = self.cardList.curselection()
        csvIdx = cardIdx[0]+1
        self.csvIdx = csvIdx;
        self.update_current_card()

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
        self.config(height = 400, width = 30)


root = tk.Tk()
patternBuilder = PatternBuilderTool(root)
root.mainloop()