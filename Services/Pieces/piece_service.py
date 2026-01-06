import json
from typing import Any, List
from Models.enums import BasicDice, SpecialDice, SquareConnectorType, UniqueTiles
from Models.piece import Piece

def __get_piece(json: dict[str, Any]) -> Piece:
  '''
  Returns a piece for the passed JSON representation. Ensures that Enums are properly parsed.
  
  :return: The created piece
  :rtype: Piece
  '''
  json = json.copy()
  
  for direction in ["north", "east", "south", "west"]:
    json[direction] = SquareConnectorType[json[direction]]
  
  dice = json["dice"]
  if dice in BasicDice.__members__:
    json["dice"] = BasicDice[dice]
  elif dice in SpecialDice.__members__:
    json["dice"] = SpecialDice[dice]
  elif dice in UniqueTiles.__members__:
    json["dice"] = UniqueTiles[dice]
   
  return Piece(**json)

def get_all_basic_pieces() -> List[Piece]:
  '''
  Returns all attainable pieces from the basic dice.
  '''
  with open("Services/Pieces/basic_pieces.json") as file:
    return [__get_piece(piece) for piece in json.load(file)]
  
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
    return [__get_piece(piece) for piece in json.load(file)]
  
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
    return [__get_piece(piece) for piece in json.load(file)]
  
def get_piece_by_name(name: str) -> Piece:
  '''
  Returns a piece by its name.
  '''
  for piece in get_all_basic_pieces() + get_all_special_pieces() + get_all_unique_pieces():
    if piece.name == name:
      return piece
    
  raise ValueError(f"Piece with name {name} not found")
