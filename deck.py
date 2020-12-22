import random


class Card:
    def __init__(self, name, flipped=False, team="normal"):
        self.name = name
        self.flipped = flipped
        self.team = team


class Deck:
    def __init__(self, names, height=5, width=5, bold=9, uline=8, bad=1):
        self.unique_words = set(names)
        self.height = height
        self.width = width
        self.size = self.height * self.width
        self.bold = bold
        self.uline = uline
        self.bad = bad
        self.deck_dict = {}
        self.most_recent = None
        self.deck_list = []

    def generate(self):
        # create and shuffle the list of words to work with
        list_of_names = list(self.unique_words)
        random.shuffle(list_of_names)
        # quick check to see if we have enough cards
        if len(list_of_names) < self.size:
            return "Not enough words in the list; make the list larger"
        # add the first n cards to the deck
        for i in range(self.size):
            temp = Card(list_of_names[i])
            self.deck_dict[list_of_names[i]] = temp
        # hold the cards in a temporary removed dictionary - so we cant adjust it twice
        temp_removed = {}
        # make some of the cards bolded
        for i in range(self.bold):
            temp = random.choice(tuple(self.deck_dict))
            temp_removed[temp] = self.deck_dict.pop(temp)
            temp_removed[temp].team = "bold"
        # make some of the cards underlined
        for i in range(self.uline):
            temp = random.choice(tuple(self.deck_dict))
            temp_removed[temp] = self.deck_dict.pop(temp)
            temp_removed[temp].team = "uline"
        # make some of the cards bad
        for i in range(self.bad):
            temp = random.choice(tuple(self.deck_dict))
            temp_removed[temp] = self.deck_dict.pop(temp)
            temp_removed[temp].team = "bad"
        # put all of the temporarily removed cards back into the deck_dict
        for i in temp_removed.keys():
            self.deck_dict[i] = temp_removed[i]
        for i in self.deck_dict.values():
            self.deck_list.append(i)
        random.shuffle(self.deck_list)
        return "The deck was successfully made & the game has started"

    def count(self, team):
        counter = 0
        for i in self.deck_dict.values():
            if i.team == team:
                counter += 1
        return counter

    def count_left(self, team):
        counter = 0
        for i in self.deck_dict.values():
            if i.team == team and i.flipped is False:
                counter += 1
        return counter

    def is_in_deck(self, string):
        if string not in self.deck_dict:
            return False
        elif self.deck_dict[string].flipped:
            return False
        else:
            return True

    def flip(self, string):
        self.deck_dict[string].flipped = True
        self.most_recent = self.deck_dict[string]
        return " just flipped " + string

    def deck_print(self, full=False):
        # cycle through the values in the deck and print them
        i = 0
        to_print = ""
        for t in self.deck_list:
            this_word = ""
            # add new line if we reached a new line
            if i % self.width == 0 and i != 0:
                this_word += "\n"
            # print the revealed version
            if t.flipped is True or full is True:
                if t.team == "normal":
                    this_word += str(t.name)
                elif t.team == "bold":
                    this_word += ("**" + str(t.name) + "**")
                elif t.team == "uline":
                    this_word += ("__" + str(t.name) + "__")
                elif t.team == "bad":
                    this_word += ("||" + str(t.name) + "||")
            # print the hidden version
            else:
                this_word += str(t.name)
            # add the flipped strikethrough
            if t.flipped is True:
                this_word = "~~" + this_word + "~~"
            # spacers between words
            this_word = "\t\t" + this_word
            # append to the final to_print variable
            to_print += this_word
            i += 1
        # return the final to_print statement
        return to_print
