import numpy as np
import matplotlib.pyplot as plt
import random


class tissue:
    
    def __init__(self,nu = 1.,delta = 0.05, eps = 0.05):
        """Fraction of vertical connections given: \'nu\'.
            Vertical connections are randomly filled. 
            Fraction of dystfunctional cells: \'delta\'. 
            Probability of failed firing: \'eps\'."""
        
        self.__n = nu    #Private vertical fractions variable
        self.__d = delta #Private cell dysfunction variable
        self.__e = eps   #Private cell depolarisation failure variable
        
        self.cell_grid = np.zeros((200,200), dtype = 'int8') #Grid on which signal will propagate. Defines whether cell is at rest, excited or refractory.
        self.cell_types = np.zeros((200,200), dtype = 'int8') #Defines cell type i.e. vertical connections and dysfunctional (or not)
        
        for i in self.cell_types:
            for j in range(len(i)):
                
                rand_nu = random.random()
                rand_delta = random.random()
                
                if rand_nu < self.__n: #If rand_nu < self.__n, cell (x,y) has connection to (x,y+1)
                    if rand_delta < self.__d: #If rand_delta < self.__d, cell (x,y) is dyfunctional. Failes to fire with P = self.__e.
                        i[j] = 2 #Both vertically connected and dysfunctional.
                    else:
                        i[j] = 1 #Vertically connected but not dysfunctional.
                else:
                    if rand_delta < self.__d:
                        i[j] = 3 #Dysfunctional but not vertically connected.
                        
    def destroy_cells(self,vectors):
        """Input vector of cells to be permanently blocked. Format as list of two lists:
        with x coordinates in list 1 and y coordinates in list 2. x = column, y = row.
        
        i.e. vectors = [[x1,x2,x3...],[y1,y2,y3...]]
        
        This will permanently block cells (x1,y1),(x2,y2),(x3,y3)..."""
        
        if len(vectors) == 2 and len(vectors[0]) == len(vectors[1]):
            for i in range(len(vectors[0])):
                self.cell_types[vectors[1][i]][vectors[0][i]] = 4 #Permanently blocked cell      
        else: 
            if len(vectors) != 2:
                print 'vectors must be list containing exactly two lists of equal length'                
            if len(vectors[0]) != len(vectors[1]):
                print 'list of x and y coordinates are not the same length'
                
    def starting_excited(self, vectors = None):
        """If cells = None, column x = 0 will be by defaults excited.
            To set custom cells to excite inputs cells as list of two lists
            with first list as x coordinates and second list as y coordinates.
            
            i.e. vectors = [[x1,x2,x3...],[y1,y2,y3...]]
        
            This will excite cells (x1,y1),(x2,y2),(x3,y3)..."""
        
        if vectors == None:
            self.cell_grid[:,0] = 50
        else:
            if len(vectors) != 2:
                print 'vectors must be list containing exactly two lists of equal length'                
            elif len(vectors[0]) != len(vectors[1]):
                print 'list of x and y coordinates are not the same length'
            else:
                for i in range(len(vectors[0])):
                    self.cell_grid[vectors[1][i]][vectors[0][i]] = 50 #Permanently blocked cell
                    
            
                
        
        
                