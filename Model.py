import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import chess, re
import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import Dense

from Data.Data import DataSet

data = DataSet().for_model(30)
print(data)
# Carefully there are many draws(-1) in data
