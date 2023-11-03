import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from keras.losses import binary_crossentropy


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
        self.model.fit(x_train, y_train, batch_size=32, epochs=Epochs, validation_split=0.4)

if __name__ == '__main__':
    from Data.ModelData import ModelData

    x, y = ModelData(20).create_inputs()
    model = Model()
    model.main(x, y)
else:
    from .Data.ModelData import ModelData

