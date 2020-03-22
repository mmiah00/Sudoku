#! /usr/bin/python
import time
import sys
import copy

class MyStack:
  def __init__(self,in_list = None):
    self.storage = []
    self.filled = 0    # will keep track of how many slots in self.storage are actually filled
    if in_list != None:   # there are more efficient ways to initialize than this, but...
        for val in in_list:
          self.push(val)

  def push(self,val):
    if self.filled == len(self.storage):
      self.storage.append(val)
    else:
      self.storage[self.filled] = val
    self.filled += 1

  def pop(self):
    if self.filled == 0:
      return None
    self.filled -= 1
    return self.storage[self.filled]

class box: #one square on a board
    def __init__ (self, data, id):
        self.data = data
        self.id = id #position in board
        self.status = ""

    def set_status (self):
        if self.data == '_':
            self.status = "open"
        else:
            self.status = "filled"

class board:
    cliques=[[0,1,2,3,4,5,6,7,8],
    [9,10,11,12,13,14,15,16,17],
    [18,19,20,21,22,23,24,25,26],
    [27,28,29,30,31,32,33,34,35],
    [36,37,38,39,40,41,42,43,44],
    [45,46,47,48,49,50,51,52,53],
    [54,55,56,57,58,59,60,61,62],
    [63,64,65,66,67,68,69,70,71],
    [72,73,74,75,76,77,78,79,80],
    [0,9,18,27,36,45,54,63,72],
    [1,10,19,28,37,46,55,64,73],
    [2,11,20,29,38,47,56,65,74],
    [3,12,21,30,39,48,57,66,75],
    [4,13,22,31,40,49,58,67,76],
    [5,14,23,32,41,50,59,68,77],
    [6,15,24,33,42,51,60,69,78],
    [7,16,25,34,43,52,61,70,79],
    [8,17,26,35,44,53,62,71,80],
    [0,1,2,9,10,11,18,19,20],
    [3,4,5,12,13,14,21,22,23],
    [6,7,8,15,16,17,24,25,26],
    [27,28,29,36,37,38,45,46,47],
    [30,31,32,39,40,41,48,49,50],
    [33,34,35,42,43,44,51,52,53],
    [54,55,56,63,64,65,72,73,74],
    [57,58,59,66,67,68,75,76,77],
    [60,61,62,69,70,71,78,79,80]]

    steps = 0

    def __init__ (self, parsed_file):
        self.data = dict ()
        self.dups = []
        self.all_boxes = self.setup (parsed_file)
        self.open_boxes = []
        for cell in self.all_boxes:
            cell.set_status ()
            if cell.status == "open":
                self.open_boxes.append (cell)
                self.find_possibles (cell)

    def printboard (self):
        ans = ""
        for key in self.data.keys ():
            ans += str (self.data[key]) + " "
            if (key + 1) % 9 == 0:
                ans += "\n"
        print (ans)

    def setup (self, bored): #takes parsed board and makes and array of boxes holding the id and the data
        id = 0
        ans = []
        for r in bored:
            new_box = box (r, id)
            ans.append (new_box)
            self.data[id] = r
            id += 1
        return ans

    def possibleshelper (self, id): #takes the id and finds each clique that has that id in it
        ans = []
        for list in self.cliques:
            if id in list:
                ans.append (list)
        return ans

    def find_possibles (self, cell): #takes the cell and finds all the numbers that it can be
        clicks = self.possibleshelper (cell.id)
        all_nums = ['1','2','3','4','5','6','7','8','9']
        for list in clicks:
            for id in list:
                num = self.data[id]
                if num != '_':
                    if num in all_nums:
                        all_nums.remove (num)
        cell.possibles = all_nums

    def check_clique(self, clique): #takes a row, column, or group and checks if there are doubles
        c = dict ()
        for position in clique: #creates a dictionary of only the positions in the given clique
            num = self.data[position]
            c[position] = num
        nums = set (c.values())
        if (len (nums) != 9): #there are duplicates
            duplicates = [] #stores the places where there is a duplicate
            vals = list (c.values ())
            for position in c.keys():
                n = c[position]
                if vals.count (n) > 1:
                    duplicates.append (position)
            self.dups.append (duplicates)
            return duplicates
        else:
            return -1

    def check_board (self):
        ans = True
        for i in range (len (self.cliques)):
            if self.check_clique (self.cliques[i]) != -1:
                ans = False
        return ans

    # def solve (self, bored):
    #     stack = MyStack ()
    #     backtracks, trials = 0, 0
    #     i = 0 #keeping track of each open cell
    #     while (not self.check_board()):
    #         trials += 1
    #         temp_board = copy.deepcopy (self)
    #         MyStack.push (temp_board)
    #         cell = temp_board.open_boxes[i]
    #         for num in cell.possibles: #trying each possiblity
    #             ide = cell.id
    #             temp_board.data[ide] = num #setting the value to that on the tempboard
    #             if self.solve(temp_board):
    #
    #     print ("Solved!")
    #     return True

    # def solve (self, bored, current_cell, next_cell, trials, backtracks):
    #     if bored.check_board ():
    #         self = bored #works?
    #         print ("Solved! with " + trials + "trials and " + backtracks + "backtracks")
    #         return True
    #     else:
    #         c = copy.deepcopy (bored)
    #         p = current_cell.possibles
    #         for num in p:

    def solverhelp(self, nodeindex):
        if (self.check_board()):
            return True
        else:
            nums = self.open_boxes[nodeindex].possibles
            for x in nums:
                if nodeindex < len(self.open_boxes):
                    self.open_boxes[nodeindex].data = x
                    self.steps = self.steps + 1
                    if (self.solverhelp(nodeindex + 1)):
                        return True
                    else:
                        self.open_boxes[nodeindex].data = '_'
                else:
                    return False

    def findSolutions(self, nodeindex):
        if (self.isSolved(self.all_boxes)):
            return True
        else:
            nums = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
            if nodeindex < len(self.open_boxes):
                relevantcliques = []
                for clique in self.cliques:
                    if self.open_boxes[nodeindex].id in clique:
                        relevantcliques.append(clique)

                for clique in relevantcliques:
                    for x in clique:
                        if self.all_boxes[x].data in nums:
                            nums.remove(self.all_boxes[x].data)

            for x in nums:
                if nodeindex < len(self.open_boxes):
                    self.open_boxes[nodeindex].data = x
                    self.steps = self.steps + 1
                    if (self.findSolutions(nodeindex + 1)):
                        return True
                    else:
                        self.open_boxes[nodeindex].data = '_'
                else:
                    return False


    def isSolved(self, in_nodes):
        for x in self.cliques:
            nums = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
            for y in x:
                if self.all_boxes[y].data in nums:
                    nums.remove(self.all_boxes[y].data)
            if (len(nums) > 0):
                return False
        return True

    def solve(self):
        self.findSolutions(0)

    def swap (self, id1, id2): #takes the id of the spots you want to swap and swaps the values
        one = self.data[id1]
        another = self.data[id2]
        self.data[id1] = another
        self.data[id2] = one
        if id1 < id2:
            return ("" + str (id1) + "," + str(id2) + "\n")
        else:
            return ("" + str(id2) + "," + str(id1) + "\n")

    def unswap (self, outfile):
        self.check_board () #sets up multiple to find the duplicates
        i = 0
        while (not self.check_board () and i < len (self.dups)):
            r = i + 1
            for r in range (len (self.dups) - 1):
                a = self.swap (self.dups[i][0], self.dups[r][0])
                if self.check_board ():
                    o = open (outfile, "a")
                    o.write (a)
                    o.close ()
                    break
                else:
                    self.swap (self.dups[i][0], self.dups[r][0])

                b = self.swap (self.dups[i][1], self.dups[r][0])
                if self.check_board ():
                    o = open (outfile, "a")
                    o.write (b)
                    o.close ()
                    break
                else:
                    self.swap (self.dups[i][1], self.dups[r][0])

                c = self.swap (self.dups[i][1], self.dups[r][1])
                if self.check_board ():
                    o = open (outfile, "a")
                    o.write (c)
                    o.close ()
                    break
                else:
                    self.swap (self.dups[i][1], self.dups[r][1])

                d = self.swap (self.dups[i][0], self.dups[r][1])
                if self.check_board ():
                    o = open (outfile, "a")
                    o.write (d)
                    o.close ()
                    break
                else:
                    self.swap (self.dups[i][0], self.dups[r][1])


def parser (file): #returns an array parsed with all the values in the board
    boards = []
    fi = open (file, "r").read ()
    f = fi.split ("\n\n")
    for i in range (len (f)):
        nums = []
        b = f[i].split("\n")[1:]
        for row in b:
            elements = row.split (",")
            if (elements != ['']):
                for n in elements:
                    nums.append (n)
        boards.append (board(nums))
    return boards

input = sys.argv [1]
output = sys.argv [2]

tests = parser (input)

for i in range (len (tests)):
    #tests[i].unswap (output)
    # for x in range (len (tests[i].open_boxes)):
    #     print (x, " : ", tests[i].open_boxes[x].id)
    tests[i].solve ()
    print (tests[i].steps)
    print ("\n\n")
    #tests[i].solver (0)
    # tests[i].printBoard ()
