import chess
import numpy as np

from Data import DataSet


class ModelData:
    def __init__(self, rows=0):
        self.x = []
        self.y = []
        self.__load(rows)


    def __load(self, rows): #Create validation of histories
        self.data = DataSet().for_model(rows)
        board = chess.Board()
       

    def create_inputs(self) -> (np.array, np.array): # create operations if black wins
        for win, history in zip(self.data["win"], self.data["history"]):
            board = chess.Board()
            bin_board = self.convert_unicode(board.unicode())
            if win:
                for i, move in enumerate(history):
                    if i%2:
                        for avaliable in board.legal_moves:
                            board.push_san(move)
                            self.x.append(np.array([*bin_board, *ModelData.convert_unicode(board.unicode())]))
                            if avaliable == board.pop():
                                self.y.append(1)
                            else: self.y.append(0)
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


# x, y = ModelData(200).create_inputs()
# print(np.shape(x))
