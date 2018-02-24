from tkinter import *
import random

#GUI Cell class mixed with conceptual Cell class
class Cell():
    PATH = "grey" #Filled in cell/Path
    EMPTY_CELL = "white" #Empty Cells Color
    PATH_BORDER = "black" #Border of filled in cells
    EMPTY_CELL_BORDER = "black" #Border of empty cells
    START_STATE = "orange" #Color of Agents start state
    GOAL_STATE = "red" #Color of goal cell
    OBSTACLES = "black" #Color of blocked cells
   
    def __init__(self, master, x, y, size, startCoords, goalCoords):
        #Gui attributes
        self.master = master
        self.abs = x
        self.ord = y
        self.size= size
        self.fill= False
        
        #Algorithmic Attributes
        if startCoords.x is x and startCoords.y is y:
            self.isStart = True
        else:
            self.isStart = False
        
        if goalCoords.x is x and goalCoords.y is y:
            self.isGoal = True
        else:
            self.isGoal = False
        
        self.isBlocked = False
        self.isVisited = False
        self.gx_Val = 1
        self.hx_Val = 1
        self.fx_Val = self.gx_Val + self.hx_Val
    
    #Gui method for filling in a cell    
    def _switch(self):
        self.fill= not self.fill
        
    #Gui method for drawing the cell
    def draw(self):
        if self.master != None :
            fill = Cell.PATH
            outline = Cell.PATH_BORDER

            if not self.fill:
                fill = Cell.EMPTY_CELL
                outline = Cell.EMPTY_CELL_BORDER
            
            if self.isStart:
                fill = Cell.START_STATE
                    
            if self.isGoal:
                fill = Cell.GOAL_STATE
                
            if self.isBlocked and not self.isGoal and not self.isStart:
                fill = Cell.OBSTACLES
            
            xmin = self.abs * self.size
            xmax = xmin + self.size
            ymin = self.ord * self.size
            ymax = ymin + self.size

            self.master.create_rectangle(xmin, ymin, xmax, ymax, fill = fill, outline = outline)

#GUI class that stores an array of Cells to represent the agents environment
class CellGrid(Canvas):
    def __init__(self,master, rowNumber, columnNumber, cellSize, start, goal, *args, **kwargs):
        #Call to super constructor
        Canvas.__init__(self, master, width = cellSize * columnNumber , height = cellSize * rowNumber, *args, **kwargs)

        self.cellSize = cellSize
        self.start = start
        self.goal = goal
        
        #Create environment(array of cells)
        self.grid = []
        for row in range(rowNumber):

            line = []
            for column in range(columnNumber):
                c = Cell(self, column, row, cellSize,start,goal)
                #***************TODO: ADD DEPTH FIRST SEARCH ALGORITHM TO DRAW THE MAZE PROPERLY & write to File****
                #Mark cell to be blocked with 30% probability & unblocked with 70% 
                if random.randint(0,100) < 30:
                    c.isBlocked = True
                else:
                    c.isBlocked = False
                line.append(c)
                    
            self.grid.append(line)
        
        #After creating each Cell call helper method to draw the cells
        self.draw()


    #Gui method for drawing the environment
    def draw(self):
        for row in self.grid:
            for cell in row:
                cell.draw()

    #algorithmic helper method that takes an array of x,y coordinates that represent 
    #The result of the A*(or other path finding algorithms) shortest path and fills in
    #Corresponding cells in the GUI
    def showPath(self, path):
        for p in path:
            cell = self.grid[p.x][p.y]
            cell._switch()
            cell.draw()
    
    #Helper method to get cell at a x,y coord
    def getCellAt(self, coord):
        return self.grid[coord.x][coord.y]
            
class Algorithms:
    def __init__(self, agent, cellGrid):
        self.agent = agent
        self.cellGrid = cellGrid
        
    def A_Star(self):
        pass
    
    def repeated_A_Star(self):
        pass
    
    def DFS(self):
        pass
                    
class Agent:
    def __init__(self, startCell, goalCell, listOfBlockedCells, cellGrid):
        self.currentCell = startCell
        self.goalCell = goalCell
        self.cellGrid = cellGrid
        self.north = cellGrid.getCellAt(Coords(self.currentCell.x, self.currentCell.y + 1))
        self.east = cellGrid.getCellAt(Coords(self.currentCell.x + 1, self.currentCell.y))
        self.south = cellGrid.getCellAt(Coords(self.currentCell.x, self.currentCell.y - 1))
        self.west = cellGrid.getCellAt(Coords(self.currentCell.x - 1, self.currentCell.y))
        self.blockedList = listOfBlockedCells
        self.algorithm = Algorithms(self, cellGrid)
    
    #Helper Method that updates N,E,S,W based on the agent's current cell's coordinates
    def updateCurrentCell(self, updatedCoords):
        self.currentCell = self.cellGrid.getCellAt(Coords(updatedCoords.x, updatedCoords.y))
        self.north = self.cellGrid.getCellAt(Coords(self.currentCell.x, self.currentCell.y + 1))
        self.east = self.cellGrid.getCellAt(Coords(self.currentCell.x + 1, self.currentCell.y))
        self.south = self.cellGrid.getCellAt(Coords(self.currentCell.x, self.currentCell.y - 1))
        self.west = self.cellGrid.getCellAt(Coords(self.currentCell.x - 1, self.currentCell.y))
    
    def getBlockedList(self):
        if self.north.isBlocked:
            self.blockedList.append(self.north)
        elif self.east.isBlocked:
            self.blockedList.append(self.east)
        elif self.south.isBlocked:
            self.blockedList.append(self.south)
        elif self.west.isBlocked:
            self.blockedList.append(self.west)
        return self.blockedList
                
    def getPath(self):
        #Return algorithm.A_Star() -> Returns list of x,y coords of A*path
        pass
        
    def addBlockedCell(self, cell): 
        self.blockedList.append(cell)
        
        
#Class for easier storage/manipulation of (x,y) points in a list
class Coords:
    def __init__(self, x, y):
        self.x = x 
        self.y = y

#Class instantiation will show finalized shortest path on creation
#So in main-> GUI(params) -> Done
class Gui: #Instantiation(app = Tk(), grid = CellGrid(params), list of x,y coords on path)
    def __init__(self, app, grid, path):
        grid.showPath(path) 
        grid.pack()
        app.mainloop()
        
#For testing methods DELETE LATER ON WHEN DONE!!!     
if __name__ == "__main__" :
    app = Tk()
    
    
    coordinates = []
    x = int(input("Enter x value of shortest path(-999 when done)"))
    while x != -999:
        y = int(input("Enter y value of shortest path"))
        coordinates.append(Coords(x,y))
        x = int(input("Enter x value of shortest path(-999 when done)"))
    i = 0
    j = 0
    a = 40
    b = 40
    start = Coords(i,j)
    goal = Coords(a,b)
    size = 101
    cellSize = 10
    #All that's Needed to be in main
    Gui(app, CellGrid(app,size,size,cellSize,start,goal),coordinates)

