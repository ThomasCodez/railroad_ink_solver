from Models.enums import BasicDice, SpecialDice, SquareConnectorType, UniqueTiles


class Piece:
  '''
  Represents a playable piece in the game, which may get placed onto a Square.
  
  Attributes:
    north: Which connector the piece has to the north
    
    east: Which connector the piece has to the east
    
    west: Which connector the piece has to the west
    
    south: Which connector the piece has to the west
    
    has_train_station: Indicates, whether the piece has a train station, where transfer from rail to road is possible.
  '''
  def __init__(
    self,
    name: str,
    dice: BasicDice | SpecialDice | UniqueTiles,
    has_rail_station: bool,
    north: SquareConnectorType,
    east: SquareConnectorType,
    south: SquareConnectorType,
    west: SquareConnectorType,
  ):
    self._name = name
    self._dice = dice
    self._north = north
    self._east = east
    self._south = south
    self._west = west
    self._has_train_station = has_rail_station
  
  @property
  def name(self) -> str:
    return self._name

  @property
  def dice(self) -> BasicDice | SpecialDice | UniqueTiles:
    return self._dice
  
  @property
  def has_train_station(self) -> bool:
    return self._has_train_station

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

  def __str__(self) -> str:
    return (
      f"Name: {self.name}"
      f"Dice: {self.dice}"
      f"Has Train Station?: {self.has_train_station}"
      f"N: {self.north}, E: {self.east}, S: {self.south}, W: {self.west}"
    )
