import pandas as pd
import chess, re

class DataSet:


    def read_files(self, rows=0) -> None:
        self.read_game_data(rows)
        self.read_game_fen(rows)

    def read_game_data(self, rows=0) -> None:
        if rows:
            self.game_data = pd.read_csv("dataset/Lichess_2013_2014_Complete.csv", nrows=rows)
        else:
            self.game_data = pd.read_csv("dataset/Lichess_2013_2014_Complete.csv")

    def read_game_fen(self, rows=0) -> None:
        if rows:
            self.game_fen = pd.read_csv("dataset/Lichess_2013_2014_FEN.csv", nrows=rows)
        else:
            self.game_fen = pd.read_csv("dataset/Lichess_2013_2014_FEN.csv")

# 1st table
# WhiteElo,BlackElo,WhiteName,BlackName,Winner,Termination,Site,Day,Month,Year,InitialTime,Increment,TimeControl,Opening,ECO,Number_of_Moves
# 2nd table
# FEN,Site
a = DataSet()
a.read_files(300)
a = a.game_data
print(a)