#! /usr/bin/python
import sys

class box: #one square on a board
    def __init__ (self, data, id):
        self.data = data
        self.id = id #position in board
        self.possibles = []

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

    def __init__ (self, parsed_file):
        self.data = dict ()
        self.dups = []
        self.boxes = self.setup (parsed_file)

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

    def possibleshelper (self, id): #takes the id and finds each clique that has that id
        ans = []
        for list in self.cliques:
            if id in list:
                ans.append (list)
        return ans

    def find_possibles (self, cell): #takes the cell and finds all the numbers that it can be
        clicks = self.possibleshelper (cell.id)
        all_nums = [1,2,3,4,5,6,7,8,9]
        for list in clicks:
            for id in list:
                num = self.data[id]
                if num != '_':
                    if num in all_nums:
                        all_nums.remove (num)
        # if cell.data == '_':
        #     for list in clicks:
        #         for id in list:
        #             num = self.data[id]
        #             if num != '_':
        #                 if num in all_nums:
        #                     all_nums.remove (num)
        cell.possibles = all_nums
        print (cell.possibles)


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
        # for clique in b:
        #     n = clique.split (",")
        #     try:
        #         for num in n:
        #             nums.append(int (num))
        #     except: #doesnt add the extra ['']
        #         for num in n:
        #             nums.append(num)
        boards.append (board(nums))
    return boards

input = sys.argv [1]
output = sys.argv [2]

tests = parser (input)

for i in range (len (tests)):
    #tests[i].unswap (output)
    bored = tests[i]
    bored.printboard ()
    print ("\n")
    #bored.find_possibles (bored.boxes[0])
    #print (bored.boxes)


# input = sys.argv[1]
# output = sys.argv[2]
#
# boards = parser (input)
#
# board1 = board (boards[0])
# board2 = board (boards[1])
#
# a = board1.unswap (output)
# b = board2.unswap (output)
