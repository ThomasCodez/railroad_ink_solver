from typing import List, Set, Tuple
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
      if node in visited_exit_nodes:
          continue
      if not __piece_fits_exit_node(node):
          continue

      # We need to determine the "virtual" incoming direction for the start node
      # so the neighbor logic works correctly.
      start_direction = ""
      if node.y == 0: start_direction = "north"     # Came from top edge
      elif node.y == 6: start_direction = "south"   # Came from bottom edge
      elif node.x == 0: start_direction = "west"    # Came from left edge
      elif node.x == 6: start_direction = "east"    # Came from right edge

      visited: Set[tuple[Square, str]] = set()

      __traverse_network(node, start_direction, exit_nodes, visited, visited_exit_nodes, board)

      unique_exits_reached = {item[0] for item in visited if item[0] in exit_nodes and __piece_fits_exit_node(item[0])}
      
      count = len(unique_exits_reached)
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
      total_points += scores.get(count, 0)

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
  occupied_squares: Set[Square] = board.get_squares_with_pieces()
  exit_nodes = board.get_exit_nodes()
  
  deductions: int = 0
  # First, handle exit nodes
  occupied_exit_nodes = occupied_squares.intersection(exit_nodes)
  for node in occupied_exit_nodes:
    assert node.piece is not None
    
    # If the piece fits the exit node, no deduction
    if __piece_fits_exit_node(node):
      continue
    deductions += 1
  
  # Handle all other squares
  occupied_non_exit_squares = occupied_squares.difference(exit_nodes)
  for square in occupied_non_exit_squares:
    assert square.piece is not None
    
    # North
    if square.piece.north != SquareConnectorType.none:
      if square.y == 0:
        deductions += 1
      else:
        adjacent = board.grid[square.x][square.y - 1]
        if adjacent.piece is None or adjacent.piece.south != square.piece.north:
          deductions += 1
    
    # East
    if square.piece.east != SquareConnectorType.none:
      if square.x == 6:
        deductions += 1
      else:
        adjacent = board.grid[square.x + 1][square.y]
        if adjacent.piece is None or adjacent.piece.west != square.piece.east:
          deductions += 1
    
    # South
    if square.piece.south != SquareConnectorType.none:
      if square.y == 6:
        deductions += 1
      else:
        adjacent = board.grid[square.x][square.y + 1]
        if adjacent.piece is None or adjacent.piece.north != square.piece.south:
          deductions += 1
    
    # West
    if square.piece.west != SquareConnectorType.none:
      if square.x == 0:
        deductions += 1
      else:
        adjacent = board.grid[square.x - 1][square.y]
        if adjacent.piece is None or adjacent.piece.east != square.piece.west:
          deductions += 1
      
  return deductions

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

def __traverse_network(node: Square, incoming_from: str, exit_nodes: Set[Square], 
                       visited: Set[tuple[Square, str]], visited_exit_nodes: Set[Square], board: Board) -> None:
    
  # Check if we have visited this specific port on this square
  if (node, incoming_from) in visited:
      return

  visited.add((node, incoming_from))

  # Mark global visited set (for the outer loop optimization)
  if node in exit_nodes and __piece_fits_exit_node(node):
      visited_exit_nodes.add(node)

  # Pass the incoming direction to get strict valid neighbors
  neighbors_with_entry = __get_neighbors(node, incoming_from, board)

  for neighbor, approach_direction in neighbors_with_entry:
      __traverse_network(neighbor, approach_direction, exit_nodes, visited, visited_exit_nodes, board)
  
def __get_neighbors(node: Square, incoming_from: str, board: Board) -> Set[Tuple[Square, str]]:
  '''
  Returns a set of tuples: (NeighborSquare, The_Side_We_Enter_Neighbor_From).
  '''
  if node.piece is None:
      return set()

  allowed_outputs: list[str] = []
  
  is_underground = (node.piece.dice == SpecialDice.underground)
  
  # --- LOGIC FOR UNDERGROUNDS vs NORMAL ---
  if is_underground:
      # Undergrounds act as straight lines that do not turn or mix types
      if incoming_from == "north": allowed_outputs = ["south"]
      elif incoming_from == "south": allowed_outputs = ["north"]
      elif incoming_from == "east": allowed_outputs = ["west"]
      elif incoming_from == "west": allowed_outputs = ["east"]
  else:
      # Normal pieces (and Stations): If we entered correctly, we can exit 
      # via ANY connector the piece has, essentially broadcasting to all connections.
      # (Stations mix networks, so Road in -> Rail out is allowed).
      
      # Add all directions that have a connector (except the one we came from)
      if node.piece.north != SquareConnectorType.none and incoming_from != "north": 
          allowed_outputs.append("north")
      if node.piece.south != SquareConnectorType.none and incoming_from != "south": 
          allowed_outputs.append("south")
      if node.piece.east != SquareConnectorType.none and incoming_from != "east": 
          allowed_outputs.append("east")
      if node.piece.west != SquareConnectorType.none and incoming_from != "west": 
          allowed_outputs.append("west")

  neighbors: Set[tuple[Square, str]] = set()
  
  if "north" in allowed_outputs and node.y > 0:
      adjacent = board.grid[node.x][node.y - 1]
      if adjacent.piece and adjacent.piece.south == node.piece.north:
          neighbors.add((adjacent, "south"))
          
  if "south" in allowed_outputs and node.y < 6:
      adjacent = board.grid[node.x][node.y + 1]
      if adjacent.piece and adjacent.piece.north == node.piece.south:
          neighbors.add((adjacent, "north"))

  if "east" in allowed_outputs and node.x < 6:
      adjacent = board.grid[node.x + 1][node.y]
      if adjacent.piece and adjacent.piece.west == node.piece.east:
          neighbors.add((adjacent, "west"))

  if "west" in allowed_outputs and node.x > 0:
      adjacent = board.grid[node.x - 1][node.y]
      if adjacent.piece and adjacent.piece.east == node.piece.west:
          neighbors.add((adjacent, "east"))
          
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