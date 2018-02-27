from tkinter import *
import random
from BinaryHeap import BinaryHeap
#from BinaryHeapTwo   import BinaryHeapTwo
import csv #For read/write maze to files



#GUI Cell class mixed with conceptual Cell class
class Cell():
    PATH = "green" #Filled in cell/Path
    EMPTY_CELL = "white" #Empty Cells Color
    PATH_BORDER = "black" #Border of filled in cells
    EMPTY_CELL_BORDER = "black" #Border of empty cells
    START_STATE = "orange" #Color of Agents start state
    GOAL_STATE = "red" #Color of goal cell
    OBSTACLES = "black" #Color of blocked cells
   
    def __init__(self, master, x, y, size, startCoords, goalCoords):
        #Gui attributes
        self.master = master
        self.x = x
        self.y = y
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
        self.heapvalue = -999
        self.gx_val = 1
        self.hx_val = 1
        self.fx_val = self.gx_val + self.hx_val
    
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
                
            if self.isBlocked and not (self.isGoal or self.isStart):
                fill = Cell.OBSTACLES
            
            xmin = self.x * self.size
            xmax = xmin + self.size
            ymin = self.y * self.size
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
        self.rowNumber = rowNumber
        self.columnNumber = columnNumber
        readWrite = "r"
        file = input("Enter a file name: ")
        
        #Create environment(array of cells)
        #Code was used for generating mazes
        self.grid = []
        if readWrite is "w":
            f = open(file, "w+") #Truncate/wipe file to overwrite for new maze
            f.close()
            for row in range(rowNumber):
            
                line = []
                with open(file, 'a') as csvfile: #Append lines
                    spamwriter = csv.writer(csvfile)
                    for column in range(columnNumber):
                        c = Cell(self, row, column, cellSize,start,goal)
                        #Mark cell to be blocked with 30% probability & unblocked with 70% 
                        if random.randint(0,100) <= 30:
                            if not c.isGoal and not c.isStart:
                                c.isBlocked = True
                                spamwriter.writerow('b')
                            else:
                                c.isBlocked = False
                                spamwriter.writerow('b')
                        else:
                            c.isBlocked = False
                            spamwriter.writerow('u')
                        line.append(c)
                    
                    self.grid.append(line)
        
            #After creating each Cell call helper method to draw the cells
            self.draw()
            
            
        #code for reading saved environments
        elif readWrite is "r":
            fileList = []
            index = 0
            with open(file, readWrite) as csvfile:
                spamreader = csv.reader(csvfile)
                for n in spamreader:
                    if ''.join(n).strip():
                        fileList.append(''.join(map(str,n)))
                        
            for row in range(rowNumber):
            
                line = []
                for column in range(columnNumber):
                    c = Cell(self, row, column, cellSize,start,goal)
                    #Mark cell to be blocked with 30% probability & unblocked with 70% 
                    if fileList[index] is 'b':
                        c.isBlocked = True
                    elif fileList[index] is 'u':
                        c.isBlocked = False
                    line.append(c)
                    index = index + 1
                    
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
        if path is None:
            print("No Path Found")
            return
        for p in path:
            cell = self.grid[p.x][p.y]
            cell._switch()
            cell.draw()
    
    #Helper method to get cell at a x,y coord
    def getCellAt(self, coord):
        if(coord.x < 0 or coord.
           x >= self.rowNumber or coord.y < 0 or coord.y >= self.columnNumber):
            return NONE        
        return self.grid[coord.x][coord.y]
            
class Algorithms:
    def __init__(self, agent, cellGrid):
        self.agent = agent
        self.cellGrid = cellGrid    
    
    def Adaptive_A_Star(self):
        pass
    
    def A_Star(self):
        temp2 = []
        came_from = {}
        came_from[self.agent.currentCell] = None
        openList = BinaryHeap(self.cellGrid.getCellAt(self.cellGrid.goal))
        openList.insert(self.agent.currentCell)
        closedList = []
        while not openList.empty():
            current = openList.delete()
            if(current == self.agent.goalCell):
                break
            closedList.append(current)
            self.agent.updateCurrentCell(current)
            children = self.agent.getUnblockedList()
            for x in children:
                if(closedList.__contains__(x)):
                    continue
                if(openList.contains(x)):
                    new_g = current.gx_val + 1
                    if(new_g < x.gx_val):
                        x.gx_val = new_g
                        came_from[x] = current
                else:
                    came_from[x] = current
                    openList.insert(x)
                    
        if(current != self.agent.goalCell):
            return None
        
        temp2 = []
        temp2.append(current)
        while came_from[current] != None:
            temp2.append(came_from[current])
            current = came_from[current]  
        return temp2
                            
class Agent:
    def __init__(self, startCell, goalCell, cellGrid):
        self.currentCell = startCell
        self.goalCell = goalCell
        self.cellGrid = cellGrid
        self.north = cellGrid.getCellAt(Coords(self.currentCell.x, self.currentCell.y - 1))
        self.east = cellGrid.getCellAt(Coords(self.currentCell.x + 1, self.currentCell.y))
        self.south = cellGrid.getCellAt(Coords(self.currentCell.x, self.currentCell.y + 1))
        self.west = cellGrid.getCellAt(Coords(self.currentCell.x - 1, self.currentCell.y))
        self.blockedList = []
        self.algorithm = Algorithms(self, cellGrid)
        self.numExpanded = 0 #For stats
    
    #Helper Method that updates N,E,S,W based on the agent's current cell's coordinates
    def updateCurrentCell(self, updatedCoords):
        self.currentCell = self.cellGrid.getCellAt(Coords(updatedCoords.x, updatedCoords.y))
        self.numExpanded = self.numExpanded + 1 #Update number of cells expanded
        
        if self.cellGrid.getCellAt(Coords(self.currentCell.x, self.currentCell.y - 1)) is NONE:
            self.north = NONE
        else:
            self.north = self.cellGrid.getCellAt(Coords(self.currentCell.x, self.currentCell.y - 1))
        if self.cellGrid.getCellAt(Coords(self.currentCell.x + 1, self.currentCell.y)) is NONE:
            self.east = NONE
        else:
            self.east = self.cellGrid.getCellAt(Coords(self.currentCell.x + 1, self.currentCell.y))
        if self.cellGrid.getCellAt(Coords(self.currentCell.x, self.currentCell.y  + 1)) is NONE:
            self.south = NONE
        else:
            self.south = self.south = self.cellGrid.getCellAt(Coords(self.currentCell.x, self.currentCell.y + 1))
        if self.cellGrid.getCellAt(Coords(self.currentCell.x - 1, self.currentCell.y)) is NONE:
            self.west = NONE
        else:
            self.west = self.cellGrid.getCellAt(Coords(self.currentCell.x - 1, self.currentCell.y))
    
    #Returns list of current cells neighbors that are blocked
    def getBlockedList(self):
        self.blockedList = []
        if(self.north != NONE):
            if self.north.isBlocked:
                self.blockedList.append(self.north)
        if(self.east != NONE):
            if self.east.isBlocked:
                self.blockedList.append(self.east)
        if self.south != NONE:
            if self.south.isBlocked:
                self.blockedList.append(self.south)
        if self.west != NONE:
            if self.west.isBlocked:
                self.blockedList.append(self.west)
        return self.blockedList
    
    #Returns list of current cells neighbors that are unblocked
    def getUnblockedList(self):
        self.unblockedList = []
        if self.north != NONE:
            if not self.north.isBlocked:
                self.unblockedList.append(self.north)
        if self.east != NONE:
            if not self.east.isBlocked:
                self.unblockedList.append(self.east)
        if self.south != NONE:
            if not self.south.isBlocked:
                self.unblockedList.append(self.south)
        if self.west != NONE:
            if not self.west.isBlocked:
                self.unblockedList.append(self.west)
        return self.unblockedList
    
    #Helper method for Backward A*
    def getHelper(self):
        return self.algorithm.A_Star()
        
    
    #Return path of user specified algorithm for printing to the GUI
    def getPath(self):
        
        x = input("Enter 1,2,3 for A*, Backwards A*, or adaptive A*, respectively")
        if x is "1":
            return self.algorithm.A_Star()
        
        elif x is "2":
            #Backwards A* (Swap start & goal, otherwise same as forward A*)
            temp = Agent(self.goalCell, self.currentCell, self.cellGrid)
            return temp.getHelper()
        
        elif x is "3":
            #Adaptive A*
            print("Line 312: Fill in this line with call to adaptive A* when implemented")
        
        
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
        
 
if __name__ == "__main__" :
    app = Tk()
    i =0 #Start x
    j = 1 #Start y
    a = 86 # Goal x
    b = 50 # Goal y
    start = Coords(i,j) #Make Start Coord
    goal = Coords(a,b) #Make Goal Coord
    size = 101 #Size of nxn grid
    cellSize = 10 #Size of individual cells
    c = CellGrid(app,size,size,cellSize,start,goal) # Create agents environment
    a = Agent(c.getCellAt(start),c.getCellAt(goal), c) #Create Agent
    
    #Display GUI
    Gui(app, c, a.getPath()) 