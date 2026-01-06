from matplotlib.axes import Axes
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle
from Models.board import Board
from Models.square import Square
import textwrap

def visualize_board_matplotlib(board: Board, filename: str = "board.png") -> None:
  """Creates a matplotlib visualization of the board matching Railroad Ink's style."""
  fig, ax = plt.subplots(figsize=(12, 12))  # type: ignore
  
  cell_size = 1.0
  line_width = 0.08
  
  for row_idx, row in enumerate(board.grid):  # row_idx = y coordinate
      for col_idx, square in enumerate(row):  # col_idx = x coordinate
          x_pos = col_idx  # column -> horizontal position
          y_pos = 6 - row_idx  # row -> vertical position (inverted for matplotlib)
          
          # Draw cell background
          color = '#E8E8E8' if square.is_central else '#FFFFFF'
          rect = patches.Rectangle((x_pos, y_pos), cell_size, cell_size, 
                                    linewidth=2, edgecolor='#333333', facecolor=color)
          ax.add_patch(rect)
          
          # Draw piece on the square
          if square.piece:
              _draw_piece(ax, square, x_pos, y_pos, cell_size, line_width)
          
          # Add grid coordinates for debugging (showing square's x, y)
          ax.text(x_pos + 0.05, y_pos + 0.95, f"({square.x},{square.y})",  # type: ignore
                  fontsize=7, color='gray', alpha=0.5)
  
  ax.set_xlim(-0.2, 7.2)
  ax.set_ylim(-0.2, 7.2)
  ax.set_aspect('equal')
  ax.axis('off')
  
  plt.savefig(filename, dpi=150, bbox_inches='tight')  # type: ignore
  plt.close()


def _draw_piece(ax: Axes, square: Square, x_pos: float, y_pos: float, cell_size: float, line_width: float) -> None:
    """Draw the piece on the square with its connectors."""
    piece = square.piece
    center = cell_size / 2
    mid_x = x_pos + center
    mid_y = y_pos + center
    
    # Draw piece background
    piece_rect = FancyBboxPatch((x_pos + 0.1, y_pos + 0.1), cell_size - 0.2, cell_size - 0.2,
                                boxstyle="round,pad=0.02", linewidth=1.5,
                                edgecolor='#000000', facecolor='#F5F5F5', zorder=5)
    ax.add_patch(piece_rect)
    
    assert piece is not None
    
    # Draw train station indicator if present
    if piece.has_train_station:
        station_circle = Circle((mid_x, mid_y), 0.08, color='#FF6B6B', zorder=6)
        ax.add_patch(station_circle)
        ax.text(mid_x, mid_y, '⚡', fontsize=8, ha='center', va='center', zorder=7) # type: ignore
          
    # 2. Process the name: Clean it, then wrap it
    clean_name = piece.name.replace('_', ' ')
    
    # 'width' is the max number of characters per line. 
    # For fontsize=6 inside a standard square, 10-12 is usually a good starting point.
    wrapped_label = textwrap.fill(clean_name, width=12)

    # Add piece name label
    # Note: With va='bottom', multi-line text grows UPWARDS, which is perfect 
    # for a label positioned at the bottom of the square.
    ax.text(mid_x, y_pos + 0.08, wrapped_label,  # type: ignore
           fontsize=6, ha='center', va='bottom', style='italic', color='#333333', zorder=6)