import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from keras.models import Sequential
from keras.layers import Dense, Convolution1D
from keras.optimizers import Adam
from keras.losses import binary_crossentropy
from keras.saving import load_model
import matplotlib.pyplot as plt


class Model:
    # fix model architecture
    def create_model(self) -> None:
        self.model = Sequential([
            Dense(512, activation='tanh', input_shape=(512,)),
            Dense(1024, activation='tanh', input_shape=(512,)),
            Dense(128, activation='tanh', input_shape=(1024,)),
            Dense(16, activation='tanh', input_shape=(128,)),
            Dense(1, activation='sigmoid')
        ])

        myAdam = Adam(learning_rate=0.00001)
        self.model.compile(optimizer=myAdam,
                    loss=binary_crossentropy,
                    metrics=['accuracy'])
        
    
    def save_model(self) -> None:
        self.model.save("saved_model/")

    def load_model(self) -> None:
        self.model = load_model("saved_model/")

    def fit(self, x, y, batch_size=128, epochs=100, validation_split=0.2):
        self.history = self.model.fit(x=x,y=y, batch_size=batch_size,
                                    epochs=epochs, verbose="auto",
                                    validation_split=validation_split).history
        
    def fit_all(self, pack_size=200, batch_size=128, epochs=100, validation_split=0.2, len_file=14918230):
        for pack in range(len_file // pack_size):
            x, y = ModelData(pack_size, pack*pack_size).create_inputs()
            print(str((pack+1)*pack_size) + " Lines loaded")
            model.fit(x, y, batch_size=batch_size, epochs=epochs, validation_split=validation_split)
            model.save_model()
            print("saved")

    def predict(self, board, colour):
        """board:chess.Board, colour:Bool (1-white, 0, black)"""
        moves, x = prepare_predict(board, colour)
        predict = self.model.predict(x, verbose=0)
        return moves[predict.argmax()]
        

        

    def create_plot(self, metrics:str) -> None:
        plt.plot(self.history[metrics])
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

    model = Model()

    # model.load_model()
    model.create_model()
    # board = chess.Board()
    # board.push_san("e2e4")

    # x, y = ModelData(200, 1).create_inputs()
    # print("Pack loaded")
    # model.fit(x, y, batch_size=128, epochs=100, validation_split=0.2)
    
    # print(model.predict(board, 1))

    model.save_model()

    model.fit_all(pack_size=1000, batch_size=400, epochs=20, validation_split=0.2)
    # model.create_plot("loss")
    # model.create_plot("accuracy")
    # model.save_model()


else:
    from Data.ModelData import ModelData
    from Data.PredictData import prepare_predict
