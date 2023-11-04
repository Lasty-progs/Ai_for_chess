import chess
import numpy as np
from random import randint



class ModelData:
    def __init__(self, rows=0):
        self.x = []
        self.y = []
        self.__load(rows)


    def __load(self, rows):
        self.data = DataSet().for_model(rows)
       

    def create_inputs(self) -> (np.array, np.array):
        for win, history in zip(self.data["win"], self.data["history"]):
            board = chess.Board()
            
            for i, move in enumerate(history):
                if win:
                    bin_board = ModelData.convert_unicode(board.unicode())
                else:
                    bin_board = ModelData.convert_unicode(board.mirror().unicode())
                
                if i%2 != win:
                    legal = []
                    [legal.append(x) for x in board.legal_moves]
                    try:
                        board.push_san(move)
                    except:
                        break

                    if win:
                        self.x.append(np.array([*bin_board, *ModelData.convert_unicode(board.unicode())]))
                    else:
                        self.x.append(np.array([*bin_board, *ModelData.convert_unicode(board.mirror().unicode())]))
                    self.y.append(1)

                    lose = legal[randint(0, len(legal) - 1)]
                    if board.pop() != lose:
                        self.y.append(0)
                        board.push(lose)
                        if win:
                            self.x.append(np.array([*bin_board, *ModelData.convert_unicode(board.unicode())]))
                        else:
                            self.x.append(np.array([*bin_board, *ModelData.convert_unicode(board.mirror().unicode())]))
                        board.pop()

                    board.push_san(move)
                else:
                    board.push_san(move)

        return (np.array(self.x),np.array(self.y))

    @staticmethod
    def convert_unicode(unicode:str) -> list:
        unicode = unicode.split()
        unicode = list(map(ModelData.unicode_to_bytes, unicode))
        unicode = ModelData.flatten(unicode)
        return unicode
        
    @staticmethod
    def flatten(matrix):
        flat_list = []
        for row in matrix:
            flat_list.extend(row)
        return flat_list
    
    @staticmethod
    def unicode_to_bytes(x:str):
        UNICODE_TO_BYTES = {
            "♛":[0,1,1,0],
            "♚":[0,1,1,1],
            "♝":[0,1,0,0],
            "♞":[0,0,1,1],
            "♜":[0,0,1,0],
            "♟":[0,0,0,1],
            "⭘":[0,0,0,0],
            "♙":[1,0,0,1],
            "♖":[1,0,1,0],
            "♘":[1,0,1,1],
            "♗":[1,1,0,0],
            "♕":[1,1,1,0],
            "♔":[1,1,1,1],
        }
        return UNICODE_TO_BYTES[x]


if __name__ == '__main__':
    from Data import DataSet

    x, y = ModelData(200).create_inputs()
    print(np.shape(x))
else:
    from .Data import DataSet

                        # Old variant of create
                        # for avaliable in board.legal_moves:
                        #     board.push_san(move)
                        #     if avaliable == board.pop():
                        #         self.y.append(1)
                        #     else: self.y.append(0)
                        #     board.push(avaliable)
                        #     self.x.append(np.array([*bin_board, *ModelData.convert_unicode(board.unicode())]))
                        #     board.pop()