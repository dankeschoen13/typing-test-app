import pandas as pd


class Offline:

    def __init__(self):
        self.data = pd.read_csv("paragraphs/v1.csv")

    def difficulty(self, selection):
        paragraph = self.data.loc[self.data.difficulty == selection, 'text'].iloc[0]
        return paragraph