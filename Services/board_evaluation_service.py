from typing import List, Set
from Models.board import Board
from Models.enums import SquareConnectorType
from Models.square import Square


def evaluate_board_position(board: Board) -> int:
  grid = board.grid
  
  total_points: int = 0
  total_points += _determine_points_from_central_squares(grid)
  total_points += _determine_points_from_networks(board)
  
  return total_points
  
def _determine_points_from_central_squares(grid: List[List[Square]]) -> int:
  central_squares: List[Square] = [square for row in grid for square in row if square.is_central and square.piece is not None]
  
  return len(central_squares)

def _determine_points_from_networks(board: Board) -> int:
  exit_nodes: Set[Square] = board.getExitNodes()
  visited_exit_nodes: Set[Square] = set()
  
  total_points: int = 0
  
  for node in exit_nodes:
    # Check if node is in network or doesn't have a piece
    if node in visited_exit_nodes or node.piece is None:
      continue
    
    # Check if piece on node matches connector of square
    if node.north != SquareConnectorType.none:
      if node.north != node.piece.north:
        continue
    
    if node.east != SquareConnectorType.none:
      if node.east != node.piece.east:
        continue
    
    if node.west != SquareConnectorType.none:
      if node.west != node.piece.west:
        continue
    
    if node.south != SquareConnectorType.none:
      if node.south != node.piece.south:
        continue
    
    visited: Set[Square] = set()
      
    total_points += _traverse_network(node, exit_nodes, visited, visited_exit_nodes, board)
    
  return total_points

def _traverse_network(node: Square, exit_nodes: Set[Square], visited: Set[Square], visited_exit_nodes: Set[Square], board: Board) -> int:
  '''
  Traverses the network recursively from an initial start node. Returns the amount of points this network is worth. 
  Updates the visisted exit nodes 
  '''
  if node in visited:
    return 0
  
  visited.add(node)
  
  if(node in exit_nodes):
    visited_exit_nodes.add(node)
    
  # Add all neighbors where the piece connects to, don't add neighbors whose connectors don't fit -> Not the same network!
  neighbors: Set[Square] = _get_neighbors(node, board)
    
  for neighbor in neighbors:
    _traverse_network(neighbor, exit_nodes, visited, visited_exit_nodes, board)
  
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
  

def _get_neighbors(node: Square, board: Board) -> Set[Square]:
    if node.piece is None:
      return set()
      
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
        
    
    
  
      
    
    
      
    
      
        
    
      
    

        
  
  