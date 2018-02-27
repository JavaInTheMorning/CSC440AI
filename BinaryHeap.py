import math
import random
import sys

class BinaryHeap:

    def __init__ (self,goalCell,size = 100,tie_val = 0):
        self.heap = [0]
        self.tie_break = tie_val # 0 = break in favor of larger g, 1 = break in favor of smaller g
        self.c = (size**2) * 10
        self.goalCell = goalCell

    def insert(self,cell):
        cell.heap_val =  self.heuristic(cell, self.goalCell)+  cell.gx_val
        self.heap.append(cell)
        self.bubble_up()

    def heuristic(self, start, goal):
        return abs(start.x - goal.x) + abs(start.y - goal.y)
    
    def bubble_up(self):
        start = len(self.heap)-1
        for i in range(start,1,-1):
            parent_index = int(math.floor(i/2))
            parent_heap_val = self.heap[parent_index].heap_val
            child_heap_val = self.heap[i].heap_val
            
            if child_heap_val == parent_heap_val:
                if self.heap[parent_index].gx_val <= self.heap[i].gx_val:
                    temp = self.heap[parent_index]
                    self.heap[parent_index] = self.heap[i]
                    self.heap[i] = temp
            elif child_heap_val < parent_heap_val:
                temp = self.heap[parent_index]
                self.heap[parent_index] = self.heap[i]
                self.heap[i] = temp

    def bubble_down(self):
        size = len(self.heap)
        end = int(math.floor(size/2))

        for i in range(1,end):
            parent = self.heap[i].heap_val
            left = self.heap[2*i].heap_val
            right = self.heap[2*i+1].heap_val

            if parent > left and parent > right:
                if left <= right:
                    temp = self.heap[i]
                    self.heap[i] = self.heap[2*i]
                    self.heap[2*i] = temp
                else:
                    temp = self.heap[i]
                    self.heap[i] = self.heap[2*i+1]
                    self.heap[2*i+1] = temp
            elif parent <= left and parent > right:
                temp = self.heap[i]
                self.heap[i] = self.heap[2*i+1]
                self.heap[2*i+1] = temp
            elif parent > left:
                temp = self.heap[i]
                self.heap[i] = self.heap[2*i]
                self.heap[2*i] = temp
            
    def delete(self):
        min_val = self.heap[1] 
        self.heap[1] = self.heap[len(self.heap)-1]
        self.heap.pop()
        self.bubble_down()
        return min_val
    
    def contains(self, cell):
        truth = False
        for x in self.heap:
            if x == cell:
                truth = True
                
        return truth

    def size(self):
        return len(self.heap)-1

    def empty(self):
        if len(self.heap) > 1:
            return False
        else:
            return True

    def check_min(self):
        return self.heap[1].f_val