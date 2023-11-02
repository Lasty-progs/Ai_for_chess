import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from app.Data import DataSet

df = DataSet(debug=1)
df = df.get_data()

elo = pd.concat([df['WhiteElo'], df['BlackElo']])

sns_plot = sns.kdeplot(elo, fill=True)
fig = sns_plot.get_figure()
fig.show()


plt.show()