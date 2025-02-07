from enum import Enum

class SquareConnectorType(Enum):
  none = 0
  road = 1
  railway = 2
  
class BasicDice(Enum):
  straight_rail = 0
  curved_rail = 1
  rail_t_junction = 2
  straigh_road = 3
  curved_road = 4
  road_t_junction = 5
  