import chess
import numpy as np


# colour for bot 1-white, 0-black
def prepare_predict(board:chess.Board, colour) -> np.array: #shape (legal_moves, 512)
    pass

if __name__ == '__main__':
    from ModelData import ModelData
else:
    from .ModelData import ModelData