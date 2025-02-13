from typing import List
from Models.board import Board
from Models.square import Square


def evaluate_board_position(board: Board) -> int:
  grid = board.grid
  
  total_points: int = 0
  total_points += _determine_points_from_central_squares(grid)
  total_points += _determine_points_from_networks(grid)
  
  return total_points
  
def _determine_points_from_central_squares(grid: List[List[Square]]) -> int:
  central_squares: List[Square] = [square for row in grid for square in row if square.is_central]
  
  return len(central_squares)

def _determine_points_from_networks(grid: List[List[Square]]) -> int:
  return 0
        
  
  