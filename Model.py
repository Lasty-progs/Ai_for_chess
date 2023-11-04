import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from keras.losses import binary_crossentropy
from keras.saving import load_model
import matplotlib.pyplot as plt

import chess
# import numpy as np

class Model:

    def create_model(self) -> None:
        self.model = Sequential([
            Dense(1024, activation='tanh', input_shape=(512,)),
            Dense(1, activation='sigmoid')
        ])

        myAdam = Adam(learning_rate=0.001)
        self.model.compile(optimizer=myAdam,
                    loss=binary_crossentropy,
                    metrics=['accuracy'])
        
    
    def save_model(self) -> None:
        self.model.save("saved_model/")

    def load_model(self) -> None:
        self.model = load_model("saved_model/")

    def fit(self, x, y, batch_size=128, epochs=100, validation_split=0.2):
        self.history = self.model.fit(x=x,y=y, batch_size=batch_size,
                                    epochs=epochs, verbose=1,
                                    validation_split=validation_split).history
    def predict(self, board, colour):
        """board:chess.Board, colour:Bool (1-white, 0, black)"""
        moves, x = prepare_predict(board, colour)
        predict = self.model.predict(x, verbose=0)
        return moves[predict.argmax()]
        

        

    def create_plot(self, metrics:str) -> None:
        plt.plot(self.history[metrics])
        print(type(self.history))
        plt.plot(self.history['val_' + metrics])
        plt.title("model " + metrics)
        plt.ylabel(metrics)
        plt.xlabel("epoch")
        plt.legend(["train", 'test'], loc="upper left")
        plt.savefig("analitics/" + metrics + ".png")
        plt.clf()

if __name__ == '__main__':
    from Data.ModelData import ModelData
    from Data.PredictData import prepare_predict

    # x, y = ModelData(200).create_inputs()
    model = Model()

    model.load_model()
    # model.create_model()
    board = chess.Board()
    board.push_san("e2e4")
    print(model.predict(board, 0))

    # model.fit(x, y, batch_size=128, epochs=10, validation_split=0.2)
    # model.create_plot("loss")
    # model.create_plot("accuracy")


else:
    from .Data.ModelData import ModelData
    from .Data.PredictData import prepare_predict

