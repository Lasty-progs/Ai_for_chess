import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


import chess, re, keras
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from keras.models import Sequential
from keras.layers import Dense


def read_data(DEBUG=1):

    if DEBUG:
        name = 'short_games.csv'
    else:
        name = 'chess_games.csv'

    coloumns = ['Event','White','Black','Result','UTCDate','UTCTime','WhiteElo','BlackElo','WhiteRatingDiff','BlackRatingDiff','ECO','Opening','TimeControl','Termination','AN']

    df = pd.read_csv(name, names=coloumns)

    histories = [key[:-4] for key in df.AN]
    filter_history = r'[0-9]*[.]+'
    # delete computer evals from histories
    filter_eval_history = r'\{.*\}|\?+|\!+'

    histories = [re.sub(filter_history, r'', history)[1:] for history in histories]
    histories = [re.sub(filter_eval_history, r'', history) for history in histories]


    status = [1 if key == '1-0' else 0 for key in df.Result]
    return histories, status


def piece(board, cell) -> str:
    if str(board.piece_at(cell)) != 'None':
        return str(board.piece_at(cell))
    else:
        return '.'


def create_fen_operations(histories):
    combination_code = ''

    x = []
    y = []
    fen_massive = []
    fen_and_code_combination = []

    PIECE_SYMBOLS_NEW = ['.','P','R','N','B','Q','K','p','n','b','r','q','k']

    incorr_data = 0

    for histories_index, this_history in enumerate(histories):
        if histories_index % 1000 == 0: print(histories_index)

        board=chess.Board()
        fen = board.fen()
        combination_code = [PIECE_SYMBOLS_NEW.index(piece(board, cell)) for cell in range(64)] 

        for index, key in enumerate(histories[histories_index].split()): #[:10]
            try:
                board.push_san(key)
            except:
                incorr_data += 1
                break
            if index % 2 == 0: 
                fen = board.fen()
                combination_code = [PIECE_SYMBOLS_NEW.index(piece(board, cell)) for cell in range(64)]


                x.append(combination_code)
                y.append(status[histories_index])
                fen_massive.append(fen) 
                fen_and_code_combination.append([fen, combination_code])
    return fen_massive, incorr_data, fen_and_code_combination, y


histories, status = read_data()
fen_massive, incorr_data, fen_and_code_combination, y = create_fen_operations(histories)

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
print('unreaded data: ', int(incorr_data/len(histories)*100), '%')


# specs for 2nd move
def train_layer(fen_massive_unicum_counter):
    fen_massive_unicum_counter_2 = []
    for key in fen_massive_unicum_counter:
        if key[0][-1] == '2' and key[0][-2] == ' ':
            fen_massive_unicum_counter_2.append(key)

    fen_massive_unicum_2 = []
    for key in fen_massive_unicum_counter_2: 
        fen_massive_unicum_2.append(key[0])

    fen_and_combination_code_unicum_2 = []
    for key in fen_massive_unicum_2:
        for key2 in fen_and_code_combination:
            if key == key2[0]:
                fen_and_combination_code_unicum_2.append([key, key2[1]])
                break 

    # create inputs for 2nd move
    x_train_2 = [ key[1] for key in fen_and_combination_code_unicum_2 ]

    y_train_2 = [ ( 1 if key[4] > 0.5 else 0 )for key in fen_massive_unicum_counter_2 ]

    x_train = np.array([ [ int(key2) for key2 in key ] for key in x_train_2  ])

    y_train = np.array([int(key) for key in y_train_2])

    # model for 2nd move
    model_1 = Sequential([
        Dense(128, activation='relu', input_shape=(64,)),
        Dense(1, activation='sigmoid')
    ])

    myAdam = keras.optimizers.Adam(learning_rate=0.0001)
    model_1.compile(optimizer=myAdam,
                loss='binary_crossentropy',
                metrics=['accuracy'])

    Epochs = 1000
    history_1 = model_1.fit(x_train, y_train, batch_size=32, epochs=Epochs, validation_split=0.2)

    plt.plot(history_1.history['accuracy'])
    plt.plot(history_1.history['val_accuracy'])
    plt.title("model accuracy")
    plt.ylabel("accuracy")
    plt.xlabel("epoch")
    plt.legend(["train", 'test'], loc="upper left")
    plt.savefig("layer.png")

train_layer(fen_massive_unicum_counter)