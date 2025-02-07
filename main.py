from Models.board import Board
from Models.enums import BasicDice
from Services.piece_services import get_all_basic_pieces, get_basic_pieces_for_dice

board = Board()
pieces = get_all_basic_pieces()
pieces = get_basic_pieces_for_dice(BasicDice.straight_rail)
for piece in pieces:
  print(piece)