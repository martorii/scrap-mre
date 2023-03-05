from sklearn.base import TransformerMixin
import pandas as pd


class Predictor(TransformerMixin):
    def __init__(self, vocabulary, threshold):
        self.vocabulary = vocabulary
        self.threshold = threshold

    def transform(self, X, *_):
        X = pd.DataFrame(X.todense(), columns=self.vocabulary)

        # Create a column that sums up occurrencies
        X['total'] = X[self.vocabulary].sum(axis=1)

        # Set up a threshold and run prediction
        X['prediction'] = X['total'].apply(lambda x: 1 if x>self.threshold else 0)
        
        return X['prediction'].tolist()

    def fit(self, *_):
        return self