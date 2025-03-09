from enum import Enum

class SquareConnectorType(Enum):
  none = 0
  road = 1
  railway = 2
  
class BasicDice(Enum):
  straight_rail = 0
  curved_rail = 1
  rail_t_junction = 2
  straight_road = 3
  curved_road = 4
  road_t_junction = 5
  
class SpecialDice(Enum):
  underground = 0
  straight_train_station = 1
  curved_train_station = 2

class UniqueTiles(Enum):
  four_rail = 0
  three_rail_one_road = 1
  two_rail_two_road_straight = 2
  two_rail_two_road_curved = 3
  one_rail_three_road = 4
  four_road = 5
  