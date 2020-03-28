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

    trials = 0
    backtracks = 0

    def __init__ (self, parsed_file, name = ""):
        self.name = name
        self.data = dict ()
        self.dups = []
        self.all_boxes = self.setup (parsed_file)
        self.open_boxes = []
        for cell in self.all_boxes:
            cell.set_status ()
            if cell.status == "open":
                self.find_possibles (cell)
                if len (cell.possibles) == 1:
                    cell.data = cell.possibles[0]
                    self.data[cell.id] = cell.possibles[0]
                    cell.status = "filled"
                else:
                    self.open_boxes.append (cell)


    def board_string (self):
        ans = ""
        for key in self.data.keys ():
            ans += str (self.data[key])
            if (key + 1) % 9 == 0:
                ans += "\n"
            else:
                ans += ","
        return ans + "\n"

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
                if num in all_nums:
                    all_nums.remove (num)
        cell.possibles = all_nums
        return all_nums

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

    def setup_openboxes (self): #makes a dictionary whose keys are lengths and the vals are each box w the possibilities that are that len, returns then in order of smallest to largest
        d = dict ()
        for box in self.open_boxes:
            a = box.possibles
            if len(a) in d.keys ():
                d[len(a)].append (box)
            else:
                d[len (a)] = [box]
        lens = sorted (d.keys ())
        ans = dict ()
        for length in lens:
            ans[length] = d[length]
        return ans

    def solverhelp (self, nodeindex):
        if (self.done()):
            return True
        else:
            if nodeindex < len(self.open_boxes):
                current_cell = self.open_boxes[nodeindex]
                possibles = self.find_possibles (current_cell)
                cliques = self.possibleshelper (current_cell.id) #find all the cliques that is related to the index
                for clique in cliques:
                    for id in clique:
                        if self.all_boxes[id].data in possibles: #goes through each clique to see what numbers are/aren't possible
                            possibles.remove(self.all_boxes[id].data) #removes what's already theres
            #print ("Nums: ", nums, "Possibles List: ", self.find_possibles (self.open_boxes[nodeindex]))

            for guess in possibles:
                if nodeindex < len(self.open_boxes):
                    current_cell.data = guess #a guess
                    self.trials += 1
                    if (self.solverhelp(nodeindex + 1)): #worked, so try the next one
                        self.data[current_cell.id] = guess
                        return True
                    else: #if it doesn't work backtrack
                        self.backtracks += 1
                        current_cell.data = '_'
                else:
                    return False


    def done(self):
        for clique in self.cliques:
            nums = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
            for pos in clique:
                if self.all_boxes[pos].data in nums:
                    nums.remove (self.all_boxes[pos].data)
            if (len (nums) > 0):
                return False
        return True

    def solve(self, outfile):
        o = open (outfile, "w")
        self.solverhelp(0)
        o.write (self.board_string ())
        o.close ()

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

names = []
def parser (file): #returns an array parsed with all the values in the board
    boards = []
    fi = open (file, "r").read ()
    f = fi.split ("\n\n")
    for i in range (len (f)):
        nums = []
        s = f[i].split ("\n")
        name = s[0]
        b = s[1:]
        for row in b:
            elements = row.split (",")
            if (elements != ['']):
                for n in elements:
                    nums.append (n)
        boards.append (board(nums, name))
    return boards

input = sys.argv [1]
output = sys.argv [2]
board_name = sys.argv[3]

tests = parser (input)
# mytest = tests[2]
# opens = mytest.setup_openboxes ()
# for key in opens.keys ():
#     print ("LENGTH: ", key, "\n\t")
#     for box in opens[key]:
#         print (box.id, " : ", box.possibles)

for i in range (len (tests)):
    title = tests[i].name.split (",")[0]
    if title == board_name:
        o = open (output, "w")
        o.write (tests[i].name + "\n") #he didn't want this but i just kept it in there
        tests[i].solve (output)
        print ("Trials: ", tests[i].trials, " Backtracks: ", tests[i].backtracks)

    print ("\n\n")
