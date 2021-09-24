from abc import ABC, abstractmethod
from constants import *
import random
from bot import Bot


class HarryBot(ABC):

    def __init__(self):
        self.dynamiteused = 0
        self.options = VALID_MOVES
        self.opponentsmoves = []
        self.counter = [0] * len(self.options)
        self.wonrounds = [0,0]

    def make_move(self, gamestate):

        roundnum = len(gamestate["rounds"])
        prevrn = roundnum - 1

        if roundnum > 0:
            self.updateCounter(gamestate, roundnum)

        omoves = self.opponentsmoves

        if roundnum > 3:
            if omoves[prevrn] == omoves[prevrn] == omoves[prevrn]:
                output = BEATERS[omoves[prevrn]]
            else:
                output = self.leastSelected()

        else:
            output = self.leastSelected()

        return output


    def randomSelect(self):
        randnum = random.randint(0, len(self.options) - 1)
        choice = self.options[randnum]
        self.checkDynamite(choice)
        return choice

    def leastSelected(self):  # Defends against the opponents least selected attack
        leastindex = self.counter.index(min(self.counter))
        choice = self.options[int(leastindex)]
        self.checkDynamite(choice)
        return choice

    def checkDynamite(self, choice):
        if choice == 'D':
            self.dynamiteused += 1
            if self.dynamiteused == NUM_DYNAMITE:
                self.options.pop()
                self.counter.pop()

    def updateCounter(self, gamestate, roundnum):
        prevrn = roundnum - 1
        oppsprevmove = gamestate['rounds'][prevrn]['p2']
        self.opponentsmoves.append(oppsprevmove)
        count = self.options.index(oppsprevmove)
        self.counter[count] += 1

    def addWinner(self, gamestate, roundnum):
        prevrn = roundnum - 1
        prevround = gamestate['rounds'][prevrn]
        p1choice, p2choice = prevround['p1'], prevround['p2']
        row, col = self.options.index(p1choice), self.options.index(p2choice)
        colkey = WIN_CONDITIONS[row].keys()[col]
        win = WIN_CONDITIONS[row][colkey]
        if win == 'p1win':
            self.wonrounds[0] += 1
        elif win == 'p2win':
            self.wonrounds[1] += 1
