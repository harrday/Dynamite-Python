from constants import *
from boterror import BotError

class Game:
  def __init__(self, bot1, bot2):
    self.__bots = [bot1, bot2]
    self.__score = [0, 0]
    self.__dynamite = [NUM_DYNAMITE, NUM_DYNAMITE]
    self.__nextRoundPoints = 1

    self.__gameState = {0: {'rounds': []}, 1: {'rounds': []}}

  def update_dynamite(self, moves):
    for i in range(2):
      if moves[i] == 'D':
        self.__dynamite[i] -= 1
      if self.__dynamite[i] < 0:
        raise BotError(i, 'dynamite')

  def update_gamestate(self, moves):
    self.__gameState[0]['rounds'].append({'p1': moves[0], 'p2': moves[1]})
    self.__gameState[1]['rounds'].append({'p1': moves[1], 'p2': moves[0]})

  def update_score(self, moves):
    for i in range(2):
      if VALID_MOVES.index(moves[i]) == -1:
        raise BotError(i, 'invalidMove', moves[i])

    if moves[0] == moves[1]:
      self.__nextRoundPoints += 1
      return

    if (
            moves[0] == 'D' and moves[1] != 'W' or
            moves[0] == 'W' and moves[1] == 'D' or
            moves[0] == 'R' and moves[1] == 'S' or
            moves[0] == 'S' and moves[1] == 'P' or
            moves[0] == 'P' and moves[1] == 'R' or
            moves[0] != 'D' and moves[1] == 'W'):
      self.__score[0] += self.__nextRoundPoints
    else:
      self.__score[1] += self.__nextRoundPoints
    self.__nextRoundPoints = 1

  def get_output(self, reason, err=None):
    output = {
      'score' : self.__score,
      'gamestate' : self.__gameState[1],
      'reason' : reason
    }
    if self.__score[0] > self.__score[1]:
      output['winner'] = 0
    else:
      output['winner'] = 1

    if err is not None and err.errorPlayer is not None:
      output['errorBot'] = err['errorPlayer']
      output['errorReason'] = err['errorReason']
      output['errorStack'] = err['stack']
      output['winner'] = 3 - err['errorPlayer']

    return output

  def play(self):
    while True:
      if SCORE_TO_WIN <= max(self.__score[0], self.__score[1]):
        return self.get_output('score')
      if len(self.__gameState[1]['rounds']) >= ROUND_LIMIT:
        return self.get_output('round limit')

      moves = [self.__bots[0].make_move(self.__gameState[0]), self.__bots[1].make_move(self.__gameState[1])]

      self.update_gamestate(moves)
      self.update_dynamite(moves)
      self.update_score(moves)

  def handle_bot_error(self, err, playerNum):
    raise BotError(playerNum, 'error', err)