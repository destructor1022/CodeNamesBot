import random
from math import sqrt


class table:
    def __init__(self, names, bold, ulin, evil, board_size):
        self.binary = []
        self.group = []
        self.names = names
        self.bold = bold
        self.ulin = ulin
        self.evil = evil
        self.board_size = board_size
        self.count = 1
        self.reveal = []

    def generate(self):
        bold_size = self.bold
        ulin_size = self.ulin
        evil_size = self.evil

        for i in range(int(sqrt(self.board_size))):
            row = []
            for j in range(int(sqrt(self.board_size))):
                row.append(0)
            self.reveal.append(row)

        for i in range(int(sqrt(self.board_size))):
            row = []
            for j in range(int(sqrt(self.board_size))):
                row.append('norm')
            self.binary.append(row)

        my_dict = set()
        while len(my_dict) < bold_size:
            curr1 = random.randint(0, int(sqrt(self.board_size)) - 1)
            curr2 = random.randint(0, int(sqrt(self.board_size)) - 1)
            if curr1 * self.board_size + curr2 not in my_dict:
                my_dict.add(curr1 * self.board_size + curr2)
                self.binary[curr1][curr2] = 'bold'

        while len(my_dict) < bold_size + ulin_size:
            curr1 = random.randint(0, int(sqrt(self.board_size)) - 1)
            curr2 = random.randint(0, int(sqrt(self.board_size)) - 1)
            if curr1 * self.board_size + curr2 not in my_dict:
                my_dict.add(curr1 * self.board_size + curr2)
                self.binary[curr1][curr2] = 'ulin'

        while len(my_dict) < bold_size + ulin_size + evil_size:
            curr1 = random.randint(0, int(sqrt(self.board_size)) - 1)
            curr2 = random.randint(0, int(sqrt(self.board_size)) - 1)
            if curr1 * self.board_size + curr2 not in my_dict:
                my_dict.add(curr1 * self.board_size + curr2)
                self.binary[curr1][curr2] = 'evil'

        my_dict = set()
        while len(my_dict) < self.board_size:
            row = []
            while len(row) < sqrt(self.board_size):
                curr = random.choice(self.names)
                if curr not in my_dict:
                    my_dict.add(curr)
                    row.append(curr)
                if len(row) == sqrt(self.board_size):
                    self.group.append(row)

    def print(self):
        for i in range(len(self.group)):
            for j in range(len(self.group[i])):
                print(self.group[i][j], end=' ')
            print()

    def revealing(self, word):
        for i in range(int(sqrt(self.board_size))):
            for j in range(int(sqrt(self.board_size))):
                if self.group[i][j] == word:
                    self.reveal[i][j] = self.count
                    self.count = self.count + 1

    def find_recent(self):
        u = 0
        word = self.group[0][0]
        for i in range(int(sqrt(self.board_size))):
            for j in range(int(sqrt(self.board_size))):
                if self.reveal[i][j] > u:
                    u = self.reveal[i][j]
                    word = self.group[i][j]
        return word

    def find_recent_x(self):
        x = 0
        u = 0
        for i in range(int(sqrt(self.board_size))):
            for j in range(int(sqrt(self.board_size))):
                if self.reveal[i][j] > u:
                    u = self.reveal[i][j]
                    x = i
        return x

    def find_recent_y(self):
        y = 0
        u = 0
        for i in range(int(sqrt(self.board_size))):
            for j in range(int(sqrt(self.board_size))):
                if self.reveal[i][j] > u:
                    u = self.reveal[i][j]
                    y = j
        return y

    def bold_left(self):
        counted = 0
        for i in range(int(sqrt(self.board_size))):
            for j in range(int(sqrt(self.board_size))):
                if self.reveal[i][j] > 0 and self.binary[i][j] == 'bold':
                    counted = counted + 1
        return self.bold - counted

    def ulin_left(self):
        counted = 0
        for i in range(int(sqrt(self.board_size))):
            for j in range(int(sqrt(self.board_size))):
                if self.reveal[i][j] > 0 and self.binary[i][j] == 'ulin':
                    counted = counted + 1
        return self.ulin - counted
