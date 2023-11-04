import chess
import numpy as np


# colour for bot 1-white, 0-black
def prepare_predict(board:chess.Board, colour:bool): #add support for black
    """colour for model - 1 if white else 0"""
    moves = []
    ins = []
    if colour:
        bin_board = ModelData.convert_unicode(board.unicode())
        for move in board.legal_moves:
            moves.append(move.uci())
            board.push(move)
            ins.append(np.array([*bin_board, *ModelData.convert_unicode(board.unicode())]))
            board.pop()
    else:
        bin_board = ModelData.convert_unicode(board.mirror().unicode())
        for move in board.legal_moves:
            moves.append(move.uci())
            board.push(move)
            ins.append(np.array([*bin_board, *ModelData.convert_unicode(board.mirror().unicode())]))
            board.pop()


    return (np.array(moves), np.array(ins))

            

if __name__ == '__main__':
    from ModelData import ModelData

else:
    from .ModelData import ModelData