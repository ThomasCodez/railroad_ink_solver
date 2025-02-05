from Models.board import Board
from Models.enums import SquareConnectorType
from Models.square import Square


def test_board_setup():
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
          assert square.west is SquareConnectorType.highway
      
      if col in (1, 5):
        if row == 0:
          assert square.north is SquareConnectorType.highway

        if row == 6:
          assert square.south is SquareConnectorType.highway
        
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
          assert square.east is SquareConnectorType.highway
          
          
      
        
          
      
  
  