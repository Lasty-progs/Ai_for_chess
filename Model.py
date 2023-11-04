import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from keras.losses import binary_crossentropy
from keras.saving import load_model
import matplotlib.pyplot as plt


class Model:

    def create_model(self) -> Sequential:
        model = Sequential([
            Dense(1024, activation='tanh', input_shape=(512,)),
            Dense(1, activation='sigmoid')
        ])

        myAdam = Adam(learning_rate=0.001)
        model.compile(optimizer=myAdam,
                    loss=binary_crossentropy,
                    metrics=['accuracy'])
        return model
    
    def save_model(self, model) -> None:
        model.save("saved_model/")

    def load_model(self):
        model = load_model("saved_model/")
        return model

    def main(self, x_train, y_train):

        # model = self.load_model()
        model = self.create_model()

        history = model.fit(x_train, y_train, batch_size=128, epochs=100, validation_split=0.2)

        self.save_model(model)

        self.create_plot(history, "loss")
        self.create_plot(history, "accuracy")
    
    def create_plot(self, history, metrics:str) -> None:
        plt.plot(history.history[metrics])
        plt.plot(history.history['val_' + metrics])
        plt.title("model " + metrics)
        plt.ylabel(metrics)
        plt.xlabel("epoch")
        plt.legend(["train", 'test'], loc="upper left")
        plt.savefig("analitics/" + metrics + ".png")
        plt.clf()

if __name__ == '__main__':
    from Data.ModelData import ModelData

    x, y = ModelData(200).create_inputs()
    model = Model()
    model.main(x, y)
else:
    from .Data.ModelData import ModelData

