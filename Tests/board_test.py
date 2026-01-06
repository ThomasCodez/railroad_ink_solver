import os
from Models.board import Board
from Models.enums import SquareConnectorType
from Models.square import Square
from Services.Board.Evaluation.board_evaluation_service import determine_deductions_for_unconnected_pieces, determine_points_from_longest_railway, determine_points_from_longest_road, evaluate_board_position # type: ignore
from Services.Board.Evaluation.board_evaluation_service import determine_points_from_networks # type: ignore
from Services.Board.Evaluation.board_evaluation_service import determine_points_from_central_squares # type: ignore
import pytest

current_dir = os.path.dirname(os.path.abspath(__file__))

def test_board_setup():
  '''
  Tests, whether the board is setup correctly with correct connectors at the edges and double point squares in the middle.
  '''
  board = Board()
  grid = board.grid
  board.to_json()
  
  for col in range(7):
    for row in range(7):
      square: Square = grid[col][row]
      
      if col == 0:
        if row == 1 or row == 5:
          assert square.west is SquareConnectorType.railway
          
        if row == 3:
          assert square.west is SquareConnectorType.road
      
      if col in (1, 5):
        if row == 0:
          assert square.north is SquareConnectorType.road

        if row == 6:
          assert square.south is SquareConnectorType.road
        
      if col in (2,4):
        if row in (2,3,4):
          assert square.is_central is True
          
      if col == 3:
        if row == 0:
          assert square.north is SquareConnectorType.railway
          
        if row in (2,3,4):
          assert square.is_central is True

        if row == 6:
          assert square.south is SquareConnectorType.railway
          
      if col == 6:
        if row == 1 or row == 5:
          assert square.east is SquareConnectorType.railway
          
        if row == 3:
          assert square.east is SquareConnectorType.road
          
def test_board_evaluation_with_empty_board():
  '''
  Tests, whether the board evaluation returns the correct amount of points for an empty board.
  '''
  with open(os.path.join(current_dir, "Boards/empty_board.json")) as f:
    board = Board.from_json(f.read())
    points = evaluate_board_position(board)
    assert points == 0
          
@pytest.mark.parametrize("filename, expected_points", [
    ("Boards/one_network_board.json", 4),
    ("Boards/two_networks_board.json", 12),
], ids=["one_network", "two_networks"])
def test_board_evaluation_networks(filename: str, expected_points: int):
    """
    Tests whether the board evaluation returns the correct amount of points 
    from networks for different board configurations.
    """
    file_path = os.path.join(current_dir, filename)
    
    with open(file_path) as f:
        board = Board.from_json(f.read())
        
    points = determine_points_from_networks(board)
    assert points == expected_points

def test_board_evaluation_with_central_squares():
  '''
  Tests, whether the board evaluation returns the correct amount of points for a board with all central squares occupied.
  '''
  with open(os.path.join(current_dir, "Boards/central_squares_board.json")) as f:
    board = Board.from_json(f.read())
    points = determine_points_from_central_squares(board.grid)
    assert points == 9
        
def test_board_evaluation_longest_railway():
  '''
  Tests, whether the board evaluation correctly identifies the longest railway.
  '''
  with open(os.path.join(current_dir, "Boards/one_network_board.json")) as f:
    board = Board.from_json(f.read())
    points = determine_points_from_longest_railway(board)
    assert points == 3

@pytest.mark.parametrize("filename, expected_points", [
    ("Boards/two_networks_board.json", 5),
    ("Boards/complex_road_network_board.json", 15),
], ids=["naive_two_networks", "complex_looping"]) 
def test_board_evaluation_longest_road(filename: str, expected_points: int):
    """
    Tests whether the board evaluation correctly identifies the longest road 
    for various board configurations.
    """
    file_path = os.path.join(current_dir, filename)
    
    with open(file_path) as f:
        board = Board.from_json(f.read())
        
    points = determine_points_from_longest_road(board)
    assert points == expected_points

@pytest.mark.parametrize("board_name, expected_deductions", [
    ("penalties_board_middle_piece_non_fitting.json", 2),
    ("penalties_board_edge_piece_non_fitting.json", 2),
    ("penalties_board_multiple_non_fitting.json", 4),
])
def test_board_evaluation_penalties_edge_piece_non_fitting(board_name: str, expected_deductions: int):
  '''
  Tests, whether the board evaluation correctly applies penalties for unconnected pieces.
  '''
  with open(os.path.join(current_dir, "Boards/" + board_name)) as f:
    board = Board.from_json(f.read())
    deductions = determine_deductions_for_unconnected_pieces(board)
    assert deductions == expected_deductions