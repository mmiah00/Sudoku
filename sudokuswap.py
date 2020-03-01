import sys

class box: #one square on a board
    def __init__ (self, data, id):
        self.data = data
        self.id = id #position in board

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

    def __init__ (self, file):
        bored = parser (file)
        setup (bored)
        self.boxes = bored
        # b = file.split ("\n")
        # bored = []
        # for i in range (len (b)):
        #     bored.append (b[i].split (","))

    def setup (board): #takes parsed board and makes and array of boxes holding the id and the data
        id = 0
        ans = []
        for r in board:
            for c in r:
                num = int (c)
                new_box = box (num, id)
                ans.append (new_box)
                id += 1
        return ans

    def initialize (self):
        id = 0
        for i in range (9):
            for j in range (9):
                bored[i][j] = box(0, id)
                id += 1

    def make_rows(self):
        row = []
        for i in range (len (self.b)):
            row.append (clique (self.b[i]))

    def parser (file): #returns an array parsed with all the values in the board
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

a = parser ("tester.txt")
print (a)
