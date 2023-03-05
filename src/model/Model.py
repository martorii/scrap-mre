from sklearn.base import BaseEstimator
import py3langid as langid
import pandas as pd


class Model(BaseEstimator):
    def __init__(self, pipeline, lang=None):
        self.lang = lang
        self.pipeline = pipeline

    def fit(self, X, y=None):
        return self

    def predict(self, X):
        # So that it also works with lists, we need this step.
        if isinstance(X, list):
            X = pd.DataFrame(X, columns=['text'])
        # Get language
        lang_col = X['text'].apply(lambda x: langid.classify(x)[0]).tolist()
        
        # Transform
        X = self.pipeline.transform(X)
        
        # Overwrite
        results = pd.DataFrame(
            list(zip(lang_col, X)), columns=['lang', 'prediction']
        )
        results['prediction'] = results.apply(
            lambda x: x['prediction'] if x['lang']==self.lang else -1, axis=1
        )
        return results['prediction']