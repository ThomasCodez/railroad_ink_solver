from Services.piece_service import get_all_basic_pieces, get_all_special_pieces, get_all_unique_pieces

def test_basic_piece_service():
  pieces = get_all_basic_pieces()
  assert len(pieces) == 20
  
def test_special_piece_service():
  pieces = get_all_special_pieces()
  assert len(pieces) == 10
  
def test_unique_piece_service():
  pieces = get_all_unique_pieces()
  assert len(pieces) == 16