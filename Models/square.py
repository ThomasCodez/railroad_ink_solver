from Models.enums import SquareConnectorType
from Models.piece import Piece


class Square:
  """
  Represents a square on the board. 

  Attributes:
    x: x coordinate of the square. Increases from left to right. 0 < x < 7
    
    y: y coordinate of the square. Increases from right to left. 0 < y < 7
    
    north: indicates the type of connector the square has to the north
    
    east: indicates the type of connector the square has to the east
    
    south: indicates the type of connector the square has to the south
    
    west: indicates the type of connector the square has to the west
    
    is_central: indicates whether the square is one of nine central squares. 
               This is determined based on the passed x and y coordinates.
               
    piece: indicates the current piece placed on the square. Initially, this is None.
  """
  def __init__(
    self, 
    x: int, 
    y: int,
    north: SquareConnectorType,
    east: SquareConnectorType,
    south: SquareConnectorType,
    west: SquareConnectorType,
  ):
    if x > 6 or x < 0 or y < 0 or y > 6:
      raise AttributeError("Values not permitted")
      
    self._x = x
    self._y = y
    self._north = north
    self._east = east
    self._south = south
    self._west = west
    self._is_central = self._determine_if_central()
    self._piece = None

  @property
  def x(self) -> int:
    return self._x

  @property
  def y(self) -> int:
    return self._y

  @property
  def north(self) -> SquareConnectorType:
    return self._north

  @property
  def east(self) -> SquareConnectorType:
    return self._east

  @property
  def south(self) -> SquareConnectorType:
    return self._south

  @property
  def west(self) -> SquareConnectorType:
    return self._west
  
  @property
  def is_central(self) -> bool:
    return self._is_central
  
  @property
  def piece(self) -> Piece | None:
    return self._piece
  
  @piece.setter
  def piece(self, piece: Piece) -> None:
    self._piece = piece
    
  
  def _determine_if_central(self) -> bool:
    '''
    Determines whether a tile is a central, which results in 
    extra points if a piece is placed in it. 
    '''
    if 2 <= self._x <= 4 and 2 <= self._y <= 4:
      return True
    
    return False
  
  def __str__(self):
    return (
        f"Square({self.x}, {self.y}) | "
        f"N: {self.north}, E: {self.east}, S: {self.south}, W: {self.west} | "
        f"Central: {self.is_central} | Piece: {self.piece}"
    )
  