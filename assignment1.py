from tkinter import *
import random
from BinaryHeap import BinaryHeap
from BinaryHeapTwo import BinaryHeapTwo


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
                
            if self.isBlocked and not self.isGoal and not self.isStart:
                fill = Cell.OBSTACLES
            
            xmin = self.x * self.size
            xmax = xmin + self.size
            ymin = self.y * self.size
            ymax = ymin + self.size

            self.master.create_rectangle(xmin, ymin, xmax, ymax, fill = fill, outline = outline)
    
    #def isBlockedCell(self):
        #if self.fill is Cell.OBSTACLES:
            #self.isBlocked = True
            #return True
        #else:
            #self.isBlocked = False
            #return False
            

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
        #Create environment(array of cells)
        self.grid = []
        for row in range(rowNumber):

            line = []
            for column in range(columnNumber):
                c = Cell(self, row, column, cellSize,start,goal)
                #***************TODO: ADD DEPTH FIRST SEARCH ALGORITHM TO DRAW THE MAZE PROPERLY & write to File****
                #Mark cell to be blocked with 30% probability & unblocked with 70% 
                if random.randint(0,100) <= 30:
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
        if(path != NONE):
            for p in path:
                cell = self.grid[p.x][p.y]
                cell._switch()
                cell.draw()
    
    #Helper method to get cell at a x,y coord
    def getCellAt(self, coord):
        if(coord.x < 0 or coord.x >= self.rowNumber or coord.y < 0 or coord.y >= self.columnNumber):
            return NONE        
        return self.grid[coord.x][coord.y]
            
class Algorithms:
    def __init__(self, agent, cellGrid):
        self.agent = agent
        self.cellGrid = cellGrid
    
    def BackwardsA_Star(self):
        temp2 = []
        temp = self.agent.currentCell
        openList = BinaryHeap(temp)
        openList.insert(self.agent.goalCell)
        came_from = {}
        cost_so_far = {}
        visited = []
        came_from[self.agent.goalCell] = NONE
        cost_so_far[self.agent.goalCell] = 0
        while not openList.empty():
            current = openList.delete()
            current.isVisited = True
            if(not visited.__contains__(current)):
                if(current == temp):
                    break
                self.agent.updateCurrentCell(current)
                neighbors = self.agent.getUnblockedList()
                for next in neighbors:
                    new_cost = cost_so_far[current] + current.gx_val
                    if next not in cost_so_far or new_cost < cost_so_far[next]:
                        cost_so_far[next] = new_cost
                        openList.insert(next)
                        came_from[next] = current
            visited.append(current)
            current.isVisited = True
            
        if(current != temp):
            return NONE
        temp = current
        temp2.append(current)
        while came_from[temp] != NONE:
            temp2.append(came_from[temp])
            temp = came_from[temp]

        return temp2
        
    def A_Star(self):
        temp2 = []
        openList = BinaryHeap(self.agent.goalCell)
        openList.insert(self.agent.currentCell)
        came_from = {}
        cost_so_far = {}
        visited = []
        came_from[self.agent.currentCell] = NONE
        cost_so_far[self.agent.currentCell] = 0
        while not openList.empty():
            current = openList.delete()
            current.isVisited = True
            if(not visited.__contains__(current)):
                if(current == self.agent.goalCell):
                    break
                self.agent.updateCurrentCell(current)
                neighbors = self.agent.getUnblockedList()
                for next in neighbors:
                    new_cost = cost_so_far[current] + current.gx_val
                    if next not in cost_so_far or new_cost < cost_so_far[next]:
                        cost_so_far[next] = new_cost
                        openList.insert(next)
                        came_from[next] = current
            visited.append(current)
            current.isVisited = True
            
        if(current != self.agent.goalCell):
            return NONE
        temp = current
        temp2.append(current)
        while came_from[temp] != NONE:
            temp2.append(came_from[temp])
            temp = came_from[temp]

        return temp2
    
    def adapativeAStar(self):
        temp = self.agent.currentCell
        openList = BinaryHeap(self.agent.goalCell)
        openList.insert(self.agent.currentCell)
        came_from = {}
        cost_so_far = {}
        visited = []
        came_from[self.agent.currentCell] = NONE
        cost_so_far[self.agent.currentCell] = 0
        while not openList.empty():
            current = openList.delete()
            current.isVisited = True
            if(not visited.__contains__(current)):
                if(current == self.agent.goalCell):
                    break
                self.agent.updateCurrentCell(current)
                neighbors = self.agent.getUnblockedList()
                for next in neighbors:
                    new_cost = cost_so_far[current] + current.gx_val
                    if next not in cost_so_far or new_cost < cost_so_far[next]:
                        cost_so_far[next] = new_cost
                        openList.insert(next)
                        came_from[next] = current
            visited.append(current)
            current.isVisited = True
            
        self.agent.updateCurrentCell(current)
        openList = BinaryHeapTwo(self.agent.goalCell)
        temp2 = []
        openList.insert(self.agent.currentCell)
        came_from = {}
        cost_so_far = {}
        visited = []
        came_from[self.agent.currentCell] = NONE
        cost_so_far[self.agent.currentCell] = 0
        while not openList.empty():
            current = openList.delete()
            current.isVisited = True
            if(not visited.__contains__(current)):
                if(current == self.agent.goalCell):
                    break
                self.agent.updateCurrentCell(current)
                neighbors = self.agent.getUnblockedList()
                for next in neighbors:
                    new_cost = cost_so_far[current] + current.gx_val
                    if next not in cost_so_far or new_cost < cost_so_far[next]:
                        cost_so_far[next] = new_cost
                        openList.insert(next)
                        came_from[next] = current
            visited.append(current)
            current.isVisited = True
            
        if(current != self.agent.goalCell):
            return NONE
        temp = current
        temp2.append(current)
        while came_from[temp] != NONE:
            temp2.append(came_from[temp])
            temp = came_from[temp]

        return temp2
            
    def heuristic(self):
        pass
    
    def repeated_A_Star(self):
        pass
    
    def DFS(self):
        pass
                    
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
    
    #Helper Method that updates N,E,S,W based on the agent's current cell's coordinates
    def updateCurrentCell(self, updatedCoords):
        self.currentCell = self.cellGrid.getCellAt(Coords(updatedCoords.x, updatedCoords.y))
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
                
    def getPath(self):
        #Return algorithm.A_Star() -> Returns list of x,y coords of A*path
        return self.algorithm.A_Star()
        pass
        
    def addBlockedCell(self, cell): 
        self.blockedList.append(cell)
        
        
#Class for easier storage/manipulation of (x,y) points in a list
class Coords:
    def __init__(self, x, y):
        self.x = x 
        self.y = y
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    
#Class instantiation will show finalized shortest path on creation
#So in main-> GUI(params) -> Done
class Gui: #Instantiation(app = Tk(), grid = CellGrid(params), list of x,y coords on path)
    def __init__(self, app, grid, path):
        grid.showPath(path) 
        grid.pack()
        app.mainloop()
        
 
if __name__ == "__main__" :
    app = Tk()
    i = 0 #Start x
    j = 1 #Start y
    a = 86 # Goal x
    b = 50 # Goal y
    start = Coords(i,j) #Make Start Coord
    goal = Coords(a,b) #Make Goal Coord
    size = 101 #Size of nxn grid
    cellSize = 10 #Size of individual cells
    c = CellGrid(app,size,size,cellSize,start,goal) # Create agents environment
    a = Agent(c.getCellAt(start),c.getCellAt(goal), c) #Create Agent
    #All that's Needed to be in main
    Gui(app, c, a.getPath()) #Display GUI