import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from keras.models import Sequential
from keras.layers import Dense

from Data.ModelData import ModelData

# 512 ins 1 out
# activation out simoid
# activation hide tanh
# hide 1024

x, y = ModelData(200).create_inputs()
print(x.shape())