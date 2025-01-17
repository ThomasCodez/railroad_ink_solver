from Models.enums import SquareConnectorType


class Square:
  """
  Represents a square on the board. Importantly, this only describes the grid square
  without any game information contained.

  Attributes:
    x: x coordinate of the square. Increases from left to right
    y: y coordinate of the square. Increases from right to left
    north: indicates the type of onramp the square has to the north
    east: indicates the type of onramp the square has to the east
    south: indicates the type of onramp the square has to the south
    west: indicates the type of onramp the square has to the west
  """
  def __init__(
    self, 
    x: int, 
    y: int,
    north: SquareConnectorType,
    east: SquareConnectorType,
    south: SquareConnectorType,
    west: SquareConnectorType
  ):
    self._x = x
    self._y = y
    self._north = north
    self._east = east
    self._south = south
    self._west = west
    

  @property
  def x(self):
    return self._x

  @property
  def y(self):
    return self._y

  @property
  def north(self):
    return self._north

  @property
  def east(self):
    return self._east

  @property
  def south(self):
    return self._south

  @property
  def west(self):
    return self._west
