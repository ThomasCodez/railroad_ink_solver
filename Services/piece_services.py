import json
from typing import List
from Models.enums import BasicDice, SpecialDice
from Models.piece import Piece

def get_all_basic_pieces() -> List[Piece]:
  '''
  Returns all attainable pieces from the basic dice.
  '''
  with open("Services/basic_pieces.json") as file:
    return [Piece(**piece) for piece in json.load(file)]
  
def get_basic_pieces_for_dice(diceResult: BasicDice) -> List[Piece]:
  '''
  Returns all placable pieces for a given dice result
  '''
  return [piece for piece in get_all_basic_pieces() if BasicDice[piece.name] == diceResult]

def get_all_special_pieces() -> List[Piece]:
  '''
  Returns all placable "special" pieces, i.e the ones attainable by the fourth, different dice.
  '''
  with open("Services/special_pieces.json") as file:
    return [Piece(**piece) for piece in json.load(file)]
  
def get_special_pieces_for_dice(diceResult: SpecialDice) -> List[Piece]:
  '''
  Returns all placable "special" pieces for a given dice result.
  '''
  return [piece for piece in get_all_special_pieces() if SpecialDice[piece.name] == diceResult]

def get_all_unique_pieces() -> List[Piece]:
  '''
  Returns all placable "unique" pieces, i.e the ones not requiring a dice and that may only get placed once.
  '''
  with open("Services/unique_pieces.json") as file:
    return [Piece(**piece) for piece in json.load(file)]
