from abc import ABC, abstractmethod

class Bot(ABC):
  @abstractmethod
  def make_move(self, gamestate):
    raise NotImplementedError('Cannot call base class')