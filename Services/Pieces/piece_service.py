import json
from typing import List
from Models.enums import BasicDice, SpecialDice
from Models.piece import Piece

def get_all_basic_pieces() -> List[Piece]:
  '''
  Returns all attainable pieces from the basic dice.
  '''
  with open("Services/Pieces/basic_pieces.json") as file:
    return [Piece(**piece) for piece in json.load(file)]
  
def get_basic_pieces_for_dice(diceResult: BasicDice) -> List[Piece]:
  '''
  Returns all placable pieces for a given dice result
  '''
  return [piece for piece in get_all_basic_pieces() if piece.dice == diceResult]

def get_all_special_pieces() -> List[Piece]:
  '''
  Returns all placable "special" pieces, i.e the ones attainable by the fourth, different dice.
  '''
  with open("Services/Pieces/special_pieces.json") as file:
    return [Piece(**piece) for piece in json.load(file)]
  
def get_special_pieces_for_dice(diceResult: SpecialDice) -> List[Piece]:
  '''
  Returns all placable "special" pieces for a given dice result.
  '''
  return [piece for piece in get_all_special_pieces() if piece.dice == diceResult]

def get_all_unique_pieces() -> List[Piece]:
  '''
  Returns all placable "unique" pieces, i.e the ones not requiring a dice and that may only get placed once.
  '''
  with open("Services/Pieces/unique_pieces.json") as file:
    return [Piece(**piece) for piece in json.load(file)]
  
def get_piece_by_name(name: str) -> Piece:
  '''
  Returns a piece by its name.
  '''
  for piece in get_all_basic_pieces() + get_all_special_pieces() + get_all_unique_pieces():
    if piece.name == name:
      return piece
    
  raise ValueError(f"Piece with name {name} not found")
