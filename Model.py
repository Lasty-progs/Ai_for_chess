import chess, keras
import pandas as pd
import numpy as np
import matplotlib as plt
from keras.models import Sequential
from keras.layers import Dense, Flatten


# load dataset
DEBUG = 1

if DEBUG:
    name = 'short_games.csv'
else:
    name = 'chess_games.csv'


coloumns = ['Event','White','Black','Result','UTCDate','UTCTime','WhiteElo','BlackElo','WhiteRatingDiff','BlackRatingDiff','ECO','Opening','TimeControl','Termination','AN']

df = pd.read_csv(name, names= coloumns)

# print(df)
# # prepare massives
# print("Started...")

# combination_code = ''

# histories = []
# status = []
# x = []
# y = []
# fen_massive = []
# fen_and_code_combination = []

# PIECE_SYMBOLS_NEW = ['.','P','R', 'N','B','Q','K','p','n','b', 'r','q','k']

# def piece(board, cell):
#     if str(board.piece_at(cell)) != 'None':
#         return str(board.piece_at(cell))
#     else:
#         return '.'
    
