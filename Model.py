import chess #, keras
import pandas as pd
import numpy as np
import matplotlib as plt
# from keras.models import Sequential
# from keras.layers import Dense, Flatten


# load dataset
DEBUG = 1

if DEBUG:
    name = 'short_games.csv'
else:
    name = 'chess_games.csv'


coloumns = ['Event','White','Black','Result','UTCDate','UTCTime','WhiteElo','BlackElo','WhiteRatingDiff','BlackRatingDiff','ECO','Opening','TimeControl','Termination','AN']

df = pd.read_csv(name, names= coloumns)[0:10]

print(df)
# prepare massives
print("Started...")

combination_code = ''

histories = []
status = []
x = []
y = []
fen_massive = []
fen_and_code_combination = []

PIECE_SYMBOLS_NEW = ['.','P','R','N','B','Q','K','p','n','b','r','q','k']

def piece(board, cell):
    if str(board.piece_at(cell)) != 'None':
        return str(board.piece_at(cell))
    else:
        return '.'
    
histories = [key for key in df.AN]

status = [1 if key == '1-0' else 0 for key in df.Result]

print('Started..')

for histories_index, this_history in enumerate(histories):
    if histories_index % 1000 == 0: print(histories_index)

    board=chess.Board()
    fen = board.fen()
    combination_code = [PIECE_SYMBOLS_NEW.index(piece(board, cell)) for cell in range(64)] 

    for index, key in enumerate(histories[histories_index].split()[:10]): #create re for true split !fix
        print(key)
        board.push_san(key)

        if index % 2 == 0: 
            fen = board.fen()
            combination_code = [PIECE_SYMBOLS_NEW.index(piece(cell)) for cell in range(64)]


            x.append(combination_code)
            y.append(status[histories_index])
            fen_massive.append(fen) 
            fen_and_code_combination.append([fen, combination_code])

print(fen_massive[0])
print('Finished')