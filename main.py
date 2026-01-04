from Models.board import Board
from Models.enums import BasicDice
from Services.Board.Evaluation.board_evaluation_service import evaluate_board_position
from Services.Pieces.piece_service import get_all_basic_pieces, get_basic_pieces_for_dice

board = Board()
pieces = get_all_basic_pieces()
pieces = get_basic_pieces_for_dice(BasicDice.straight_rail)

with open('Tests/Boards/complex_road_network_board.json') as f:
    board = board.from_json(f.read())
    points = evaluate_board_position(board)