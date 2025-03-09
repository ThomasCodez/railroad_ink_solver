from Models.board import Board
from Models.enums import BasicDice
from Services.Pieces.piece_service import get_all_basic_pieces, get_basic_pieces_for_dice

board = Board()
pieces = get_all_basic_pieces()
pieces = get_basic_pieces_for_dice(BasicDice.straight_rail)

with open('board.json') as f:
    board.from_json(f.read())