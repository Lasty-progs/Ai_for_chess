import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from keras.losses import binary_crossentropy
import matplotlib.pyplot as plt

# 512 ins 1 out
# activation out simoid
# activation hide tanh
# hide 1024
class Model:

    def main(self, x_train, y_train):

        self.model = Sequential([
            Dense(1024, activation='tanh', input_shape=(512,)),
            Dense(1, activation='sigmoid')
        ])

        myAdam = Adam(learning_rate=0.001)
        self.model.compile(optimizer=myAdam,
                    loss=binary_crossentropy,
                    metrics=['accuracy'])

        Epochs = 100
        history = self.model.fit(x_train, y_train, batch_size=32, epochs=Epochs, validation_split=0.4)
        plt.plot(history.history['loss'])
        plt.plot(history.history['val_loss'])
        plt.title("model loss")
        plt.ylabel("loss")
        plt.xlabel("epoch")
        plt.legend(["train", 'test'], loc="upper left")
        plt.savefig("loss.png")

if __name__ == '__main__':
    from Data.ModelData import ModelData

    x, y = ModelData(200).create_inputs()
    model = Model()
    model.main(x, y)
else:
    from .Data.ModelData import ModelData

