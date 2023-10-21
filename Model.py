import chess, re #, keras
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

df = pd.read_csv(name, names= coloumns)[:10]
# prepare massives

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



histories = [key[:-4] for key in df.AN]

histories = [re.sub(r'[0-9]*[.]', r'', history)[1:] for history in histories]
histories = [re.sub(r'  ', r' ', history) for history in histories]



status = [1 if key == '1-0' else 0 for key in df.Result]

print('Started..') # flag for new block

for histories_index, this_history in enumerate(histories):
    if histories_index % 1000 == 0: print(histories_index)

    board=chess.Board()
    fen = board.fen()
    combination_code = [PIECE_SYMBOLS_NEW.index(piece(board, cell)) for cell in range(64)] 

    for index, key in enumerate(histories[histories_index].split()[:10]):
        board.push_san(key)

        if index % 2 == 0: 
            fen = board.fen()
            combination_code = [PIECE_SYMBOLS_NEW.index(piece(board, cell)) for cell in range(64)]


            x.append(combination_code)
            y.append(status[histories_index])
            fen_massive.append(fen) 
            fen_and_code_combination.append([fen, combination_code])

print(fen_massive[0])
print('Finished')

fen_massive_unicum = list(set(fen_massive))

print('Started..')

fen_massive_unicum_counter = []

for key in fen_massive_unicum:
    fen_massive_unicum_counter.append([key,0,0,0,0])

for index, key in enumerate(fen_massive_unicum_counter):
    if index % 1000 == 0: print(index)
    for index2, key2 in enumerate(fen_massive):
        if key[0] == key2:
            key[1] += 1
            if y[index2] == 1: key[2] += 1 
            else: key[3] += 1
            key[4] = key[2]/key[1]

print()
print('Finished')

# first moves specs

board = chess.Board()
fen = board.fen()

win_persent = []
legals = []


for key in board.legal_moves:
    legals.append(str(key))

for index, legal_move in enumerate(legals):
    board.push_san(legal_move)
    fen = board.fen()

# find combinations
    for key in fen_massive_unicum_counter:
        if fen == key[0]:
            print(index, 'move:', legal_move, 'total:', key[1], 'wins:', key[2], 'percent:', key[4])
            win_persent.append([legal_move, key[1], key[4]])

            break
    board.pop()

print()
print('len(win_percent):', len(win_persent))
