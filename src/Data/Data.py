import pandas as pd
import re

class DataSet:
    '''Class for operating data for model fiting or analysis \n
    -use for_model() for get wins, history dataframe'''
    # -use for_analysis() for get all meta information about games without history

    def for_model(self, rows=0, start=1) -> pd.DataFrame:
        self.__read_files(rows, start)
        self.data = pd.concat([self.__set_winner(self.__game_data["Winner"]),
                                self.__split_fen(self.__game_fen["FEN"])], axis=1)

        self.data = self.data[self.data["Winner"] >= 0]
        self.data = self.data.rename(columns={"Winner":"win", "FEN":"history"})
        self.data.reset_index(drop=True, inplace=True)
        return self.data
    
    # def for_analysis(self, rows=0) -> pd.DataFrame:
    #     self.__read_game_data(rows)
    #     return self.__game_data

    def __read_files(self, rows=0, start=1) -> None:
        self.__read_game_data(rows, start)
        self.__read_game_fen(rows, start)

    def __read_game_data(self, rows=0, start=1) -> None:
        if rows:
            self.__game_data = pd.read_csv("dataset/Lichess_2013_2014_Complete.csv", nrows=1)
            cols = self.__game_data.columns.to_list()
            self.__game_data = pd.read_csv(
                "dataset/Lichess_2013_2014_Complete.csv", nrows=rows, skiprows=start, names=cols)
        else:
            self.__game_data = pd.read_csv("dataset/Lichess_2013_2014_Complete.csv")

    def __read_game_fen(self, rows=0, start=1) -> None:
        if rows:
            self.__game_fen = pd.read_csv("dataset/Lichess_2013_2014_FEN.csv", nrows=1)
            cols = self.__game_fen.columns.to_list()
            self.__game_fen = pd.read_csv(
                "dataset/Lichess_2013_2014_FEN.csv", nrows=rows, skiprows=start, names=cols)
        else:
            self.__game_fen = pd.read_csv("dataset/Lichess_2013_2014_FEN.csv")

    def __split_fen(self, histories:pd.Series) -> pd.Series:
        # return histories
        filter_history = r'[0-9]*[.]+'
        # delete computer evals from histories
        # filter_eval_history = r'\{.*\}|\?+|\!+'

        histories = histories.map(lambda x:re.sub(filter_history, r'', x)[:-5])
        # histories.map(lambda x:re.sub(filter_eval_history, r'', x))
        histories = histories.map(lambda x:x.split())

        return histories

    def __set_winner(self, winner:pd.Series) -> pd.Series:
        winner = winner.map(lambda x:1 if x == "White" else 0 if x == "Black" else -1)
        return winner