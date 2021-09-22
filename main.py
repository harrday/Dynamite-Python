from pprint import pprint

from game import Game
from paperbot import PaperBot
from rockbot import RockBot

def main():
  bot1 = PaperBot()
  bot2 = RockBot()
  game = Game(bot1, bot2)
  result = game.play()
  pprint(result)

if __name__ == '__main__':
  main()