from typing import List, Set
from Models.board import Board
from Models.enums import SpecialDice, SquareConnectorType
from Models.square import Square


def evaluate_board_position(board: Board) -> int:
  grid = board.grid
  
  total_points: int = 0
  total_points += determine_points_from_central_squares(grid)
  total_points += determine_points_from_networks(board)
  total_points += determine_points_from_longest_road(board)
  total_points += determine_points_from_longest_railway(board)
  total_points -= determine_deductions_for_unconnected_pieces(board)
  
  return total_points
  
def determine_points_from_central_squares(grid: List[List[Square]]) -> int:
  occupied_central_squares: List[Square] = [square for row in grid for square in row if square.is_central and square.piece is not None]
  
  return len(occupied_central_squares)

def determine_points_from_networks(board: Board) -> int:
  exit_nodes: Set[Square] = board.get_exit_nodes()
  visited_exit_nodes: Set[Square] = set()
  
  total_points: int = 0
  
  for node in exit_nodes:
    # Check if node is in network or doesn't have a piece
    if node in visited_exit_nodes:
      continue
    
    if __piece_fits_exit_node(node) is False:
      continue
    
    visited: Set[Square] = set()
      
    total_points += __traverse_network(node, exit_nodes, visited, visited_exit_nodes, board)
    
  return total_points

def determine_points_from_longest_road(board: Board) -> int:
  occupied_squares: Set[Square] = board.get_squares_with_pieces()
  
  longest_road = 0
  for square in occupied_squares:
    assert square.piece is not None
    
    if square.piece.east != SquareConnectorType.road and square.piece.west != SquareConnectorType.road and square.piece.north != SquareConnectorType.road and square.piece.south != SquareConnectorType.road:
      continue
    
    longest_road_from_node = __find_longest_path_from_node(square, "", set(), board, is_railway=False)
    
    if longest_road_from_node > longest_road:
      longest_road = longest_road_from_node
    
  return longest_road

def determine_points_from_longest_railway(board: Board) -> int:
  occupied_squares: Set[Square] = board.get_squares_with_pieces()
  
  longest_rail = 0
  for square in occupied_squares:
    assert square.piece is not None
    
    if square.piece.east != SquareConnectorType.railway and square.piece.west != SquareConnectorType.railway and square.piece.north != SquareConnectorType.railway and square.piece.south != SquareConnectorType.railway:
      continue
    
    longest_rail_from_node = __find_longest_path_from_node(square, "", set(), board, is_railway=True)
    
    if longest_rail_from_node > longest_rail:
      longest_rail = longest_rail_from_node
    
  return longest_rail

def determine_deductions_for_unconnected_pieces(board: Board) -> int:
  return 0

def __piece_fits_exit_node(node: Square) -> bool:
    '''
    Checks whether a piece fits to the exit node. To do so, the square's connector must equal the piece's connector. I.E, square.north is rail, the piece's north connector sholuld also be rail.
    '''
    if node.piece is None:
      return False
    
    if node.north != SquareConnectorType.none:
      if node.north == node.piece.north:
        return True
    
    if node.east != SquareConnectorType.none:
      if node.east == node.piece.east:
        return True
    
    if node.west != SquareConnectorType.none:
      if node.west == node.piece.west:
        return True
    
    if node.south != SquareConnectorType.none:
      if node.south == node.piece.south:
        return True
      
    return False

def __traverse_network(node: Square, exit_nodes: Set[Square], visited: Set[Square], visited_exit_nodes: Set[Square], board: Board) -> int:
  '''
  Traverses the network recursively from an initial start node. Returns the amount of points this network is worth. 
  Updates the visisted exit nodes 
  '''
  if node in visited:
    return 0
  
  visited.add(node)

  if node in exit_nodes:
    # Only add to network if the piece fits the exit node
    if __piece_fits_exit_node(node):
      visited_exit_nodes.add(node)
    
  # Add all neighbors where the piece connects to, don't add neighbors whose connectors don't fit -> Not the same network!
  neighbors: Set[Square] = __get_neighbors(node, board)
    
  for neighbor in neighbors:
    __traverse_network(neighbor, exit_nodes, visited, visited_exit_nodes, board)
  
  scores: dict[int, int] = {
    2: 4,
    3: 8,
    4: 12,
    5: 16,
    6: 20,
    7: 24,
    8: 28,
    9: 32,
    10: 36,
    11: 40,
    12: 45,
  }
  
  return scores[len(visited.intersection(exit_nodes))]
  
def __get_neighbors(node: Square, board: Board) -> Set[Square]:
    '''
    Returns all neighbors of a square that have a piece and the piece fits the connector. Undergrounds are treated specially.
    '''
    if node.piece is None:
      return set()
    
    # Special case: Undergrounds. 
    if node.piece.dice == SpecialDice.underground:
      pass # We have to fucking do something about this, but I don't know what yet.
      
    neighbors: Set[Square] = set()
    
    if node.piece.north != SquareConnectorType.none and node.y > 0:
      adjacent = board.grid[node.x][node.y - 1]
    
      if adjacent.piece and adjacent.piece.south == node.piece.north:
        neighbors.add(adjacent)
    
    if node.piece.east != SquareConnectorType.none and node.x < 6:
      adjacent = board.grid[node.x + 1][node.y]
    
      if adjacent.piece and adjacent.piece.west == node.piece.east:
        neighbors.add(adjacent)
  
    if node.piece.south != SquareConnectorType.none and node.y < 6:
      adjacent = board.grid[node.x][node.y + 1]
    
      if adjacent.piece and adjacent.piece.north == node.piece.south:
        neighbors.add(adjacent)
  
    if node.piece.west != SquareConnectorType.none and node.x > 0:
      adjacent = board.grid[node.x - 1][node.y]
    
      if adjacent.piece and adjacent.piece.east == node.piece.west:
        neighbors.add(adjacent)
        
    return neighbors

def __find_longest_path_from_node(node: Square, incoming_orientation: str, visited: set[tuple[Square, str]], board: Board, is_railway: bool) -> int:
  if (node, incoming_orientation) in visited:
    return 0
  
  visited = visited.copy()
  visited.add((node, incoming_orientation))
  
  neighbors = __get_rail_or_road_neighbors(node, board, incoming_orientation, is_railway)
  
  best = 1
  for neighbor, orientation in neighbors:
    length = 1 + __find_longest_path_from_node(neighbor, orientation, visited, board, is_railway)
    if length > best:
      best = length
  
  return best

def __get_rail_or_road_neighbors(node: Square, board: Board, incoming_orientation: str, is_railway: bool) -> Set[tuple[Square, str]]:
  if node.piece is None:
    return set()
  
  neighbors: Set[tuple[Square, str]] = set()
  
  connector_type = SquareConnectorType.railway if is_railway else SquareConnectorType.road
  
  # Special case: Undergrounds. 
  if node.piece.dice == SpecialDice.underground:
      pass # We have to fucking do something about this, but I don't know what yet.

  if node.piece.north == connector_type and node.y > 0 and incoming_orientation != "south":
    adjacent = board.grid[node.x][node.y - 1]
  
    if adjacent.piece and adjacent.piece.south == connector_type:
      neighbors.add((adjacent, "north"))
  
  if node.piece.east == connector_type and node.x < 6 and incoming_orientation != "west":
    adjacent = board.grid[node.x + 1][node.y]
  
    if adjacent.piece and adjacent.piece.west == connector_type:
      neighbors.add((adjacent, "east"))

  if node.piece.south == connector_type and node.y < 6 and incoming_orientation != "north":
    adjacent = board.grid[node.x][node.y + 1]
  
    if adjacent.piece and adjacent.piece.north == connector_type:
      neighbors.add((adjacent, "south"))

  if node.piece.west == connector_type and node.x > 0 and incoming_orientation != "east":
    adjacent = board.grid[node.x - 1][node.y]
  
    if adjacent.piece and adjacent.piece.east == connector_type:
      neighbors.add((adjacent, "west"))
  
  return neighbors 
    

    
    
    
  
      
    
    
      
    
      
        
    
      
    

        
  
  