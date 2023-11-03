import chess
import numpy as np

# import for statics
from ModelData import ModelData

# colour for bot 1-white, 0-black
def prepare_predict(board:chess.Board, colour) -> np.array: #shape (legal_moves, 512)
    pass