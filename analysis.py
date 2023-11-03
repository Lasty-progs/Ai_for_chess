import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from Data.Data import DataSet

df = DataSet().for_analysis(30)

print(df["Winner"])

# elo = pd.concat([df['WhiteElo'], df['BlackElo']])

# sns_plot = sns.kdeplot(elo, fill=True)
# fig = sns_plot.get_figure()
# fig.show()


# plt.show()