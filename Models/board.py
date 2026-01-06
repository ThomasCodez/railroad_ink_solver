from __future__ import annotations #
from Models.enums import SquareConnectorType
from Models.square import Square
from typing import List, Set
import json

from Services.Pieces.piece_service import get_piece_by_name


class Board:
  '''
  Represents the game board for Railroad Ink. The board is a 7x7 grid of Squares.
  
  COORDINATE SYSTEM:
  - Uses (column, row) indexing where (0,0) is TOP-LEFT corner
  - column (x): 0 = left edge, 6 = right edge
  - row (y): 0 = top edge, 6 = bottom edge
  - Access via: grid[row][column] or grid[y][x]
  '''
  squares: Set[Square] | None = None
  
  def __init__(self):
    self._grid = self._create_grid()
    
  @property
  def grid(self) -> List[List[Square]]:
    return self._grid 
 
  def _create_grid(self) -> List[List[Square]]:
    '''
    Creates the grid of Squares, which make up the game board.
    '''
    rows: List[List[Square]] = []
    for x in range(7):
      row: List[Square] = []
      
      for y in range(7):
        row.append(Square(
          x = x,
          y = y,
          north = self.__determine_north_connector(x, y),
          east = self.__determine_east_connector(x, y),
          south = self.__determine_south_connector(x, y),
          west = self.__determine_west_connector(x, y)
        ))
      
      rows.append(row)
    
    return rows
      
  def __determine_north_connector(self, x: int, y: int) -> SquareConnectorType:
    '''
    Determines the connector type for the north side of a Square.
    '''
    
    if (x == 1 or x == 5) and y == 0:
      return SquareConnectorType.road
      
    if x == 3 and y == 0:
      return SquareConnectorType.railway
    
    return SquareConnectorType.none 
  
  def __determine_east_connector(self, x: int, y: int) -> SquareConnectorType:
    '''
    Determines the connector type for the east side of a Square.
    '''
    
    if x == 6 and (y == 1 or y == 5):
      return SquareConnectorType.railway
      
    if x == 6 and y == 3:
      return SquareConnectorType.road
    
    return SquareConnectorType.none
  
  def __determine_south_connector(self, x: int, y: int) -> SquareConnectorType:
    '''
    Determines the connector type for the south side of a Square.
    '''
    
    if (x == 1 or x == 5) and y == 6:
      return SquareConnectorType.road
      
    if x == 3 and y == 6:
      return SquareConnectorType.railway
    
    return SquareConnectorType.none
  
  def __determine_west_connector(self, x: int, y:int) -> SquareConnectorType:
    '''
    Determines the connector type for the west side of a Square.
    '''
    
    if x == 0 and (y == 1 or y == 5):
      return SquareConnectorType.railway
      
    if x == 0 and y == 3:
      return SquareConnectorType.road
    
    return SquareConnectorType.none
  
  def get_exit_nodes(self) -> Set[Square]:
    '''
    Returns the exit nodes of the board.
    '''
    return {self.grid[0][1], 
            self.grid[0][3], 
            self.grid[0][5], 
            self.grid[1][0],
            self.grid[1][6],
            self.grid[3][0],
            self.grid[3][6],
            self.grid[5][0],
            self.grid[5][6],
            self.grid[6][1],
            self.grid[6][3],
            self.grid[6][5]
          }
    
  def get_all_squares(self) -> Set[Square]:
    '''
    Returns all squares of the board as a set.
    '''
    if self.squares is not None:
      return self.squares

    self.squares = set()
    
    for row in self._grid:
      for square in row:
        self.squares.add(square)
        
    return self.squares
  
  def get_squares_with_pieces(self) -> Set[Square]:
    '''
    Returns all squares of the board that have pieces placed on them.
    '''
    all_squares: Set[Square] = self.get_all_squares()
    occupied_squares = {square for square in all_squares if square.piece is not None}
    
    return occupied_squares
    
  def to_json(self) -> None:
    '''
    Exports the board grid to a JSON string.
    '''
    grid_data = []
    
    for row in self._grid:
      row_data = []
      
      for square in row:
        row_data.append({ # type: ignore
          'x': square.x,
          'y': square.y,
          'north': square.north.name,
          'east': square.east.name,
          'south': square.south.name,
          'west': square.west.name,
          'is_central': square.is_central,
          'piece': square.piece.name if square.piece else None
        })
      grid_data.append(row_data) # type: ignore
    
    data = json.dumps(grid_data, indent=2)
    
    with open("board.json", 'w') as file:
      file.write(data)
      
  @classmethod
  def from_json(cls, json_data: str) -> Board:
    '''
    Creates a board based on the passed json data. Specifically, the grid is determined as usual, however pieces are placed 
    on the board based on the passed json data. 
    
    Parameters
    ----------
    json_data : str
        The json should be an array of objects, where each object has the fields 'x', 'y' and 'piece'. 0 <= 'x' <= 6, 0 <= 'y' <= 6 and 'piece' should be the name matching to one of the pieces. 
    '''
    data = json.loads(json_data)
    
    board = Board()
    grid = board.grid
    
    for row in data:
      for col in row:
        square: Square = grid[col['x']][col['y']] # type: ignore
        if col['piece'] is not None:
          square.piece = get_piece_by_name(col['piece'])
    
    return board
    