import sys

class box: #one square on a board
    def __init__ (self, data, id):
        self.data = data
        self.id = id #position in board

class board:
    data = dict ()
    multiple = [] #stores all the positions that have duplicates
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

    def __init__ (self, file):
        bored = self.parser (file)
        self.boxes = self.setup (bored)

    def parser (self,file): #returns an array parsed with all the values in the board
        fi = open (file, "r")
        ans = []
        for line in fi:
            f = line.split ("\n")
            for clique in f:
                a = clique.split (",")
                ans.append (a)
        while [''] in ans:
            ans.remove ([''])
        return ans

    def setup (self,bored): #takes parsed board and makes and array of boxes holding the id and the data
        id = 0
        ans = []
        for r in bored:
            for c in r:
                num = int (c)
                new_box = box (num, id)
                ans.append (new_box)
                self.data[id] = num
                id += 1
        return ans

    def check_clique(self, clique): #takes a row, column, or group and checks if there are doubles
        c = dict ()
        for position in clique: #creates a dictionary of only the positions in the given clique
            c[position] = self.data[position]
        nums = set (c.values())
        if (len (nums) != 9): #there are duplicates
            duplicates = [] #stores the places where there is a duplicate
            vals = list (c.values ())
            for position in c.keys():
                n = c[position]
                if vals.count (n) > 1:
                    duplicates.append (position)
            self.multiple.append (duplicates)
            return duplicates
        else:
            return -1

    def check_board (self):
        ans = True
        for i in range (len (self.cliques)):
            if self.check_clique (self.cliques[i]) != -1:
                ans = False
        return ans
        # for clique in self.cliques:
        #     if self.check_clique (clique) != -1:
        #         return False
        # return True

    def swap (self, id1, id2): #takes the id of the spots you want to swap and swaps the values
        one = self.data[id1]
        another = self.data[id2]
        self.data[id1] = another
        self.data[id2] = one
        if one < another:
            return ("" + str (one) + "," + str(another) + "\n")
        else:
            return ("" + str(another) + "," + str(one) + "\n")

    def unswap (self, outfile):
        self.check_board ()
        i = 0
        while (not self.check_board () and i < len (self.multiple)):
            r = i + 1
            for r in range (len (self.multiple) - 1):
                a = self.swap (self.multiple[i][0], self.multiple[r][0])
                if self.check_board ():
                    o = open (outfile, "w")
                    o.write (a)
                    break
                else:
                    self.swap (self.multiple[i][0], self.multiple[r][0])

                b = self.swap (self.multiple[i][1], self.multiple[r][0])
                if self.check_board ():
                    o = open (outfile, "w")
                    o.write (b)
                    break
                else:
                    self.swap (self.multiple[i][1], self.multiple[r][0])

                c = self.swap (self.multiple[i][1], self.multiple[r][1])
                if self.check_board ():
                    o = open (outfile, "w")
                    o.write (c)
                    break
                else:
                    self.swap (self.multiple[i][1], self.multiple[r][1])

                d = self.swap (self.multiple[i][0], self.multiple[r][1])
                if self.check_board ():
                    o = open (outfile, "w")
                    o.write (d)
                    break
                else:
                    self.swap (self.multiple[i][0], self.multiple[r][1])


        # if not self.check_board ():
        #     s = self.swap (p1, p2)
        #     if self.check_board ():
        #         o = open (outfile, "w")
        #         o.write (s)
        #     else:
        #         unswap ()


        # if i + 1 > len (self.multiple):
        #     self.check_board ()
        #     self.unswap (outfile, i)
        # else:
        #     p1 = self.multiple [i][0]
        #     p2 = self.multiple [i][1]
        #     s = self.swap (p1, p2)
        #     if not self.check_board():
        #         #self.swap (p1, p2)
        #         self.unswap (outfile, i + 1)
        #     else:
        #         o = open (outfile, "w")
        #         outfile.write (s)


a = board ("tester2.txt")
a.unswap ("out.txt")
