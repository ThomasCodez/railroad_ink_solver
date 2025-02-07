import json
from Models.enums import BasicDice
from Models.piece import Piece

def get_all_basic_pieces():
  '''
  Returns all attainable pieces from the basic dice.
  '''
  with open("Services/basic_pieces.json") as file:
    return [Piece(**piece) for piece in json.load(file)]
  
def get_basic_pieces_for_dice(diceResult: BasicDice):
  #all_dice: List[Piece] = get_all_basic_pieces()
  return [piece for piece in get_all_basic_pieces() if BasicDice[piece.name] == diceResult]
