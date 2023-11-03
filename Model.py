import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from keras.models import Sequential
from keras.layers import Dense


# 512 ins 1 out
# activation out simoid
# activation hide tanh
# hide 1024
class Model:
    pass


if __name__ == '__main__':
    from Data.ModelData import ModelData
else:
    from .Data.ModelData import ModelData


x, y = ModelData(20).create_inputs()
print(x.shape)