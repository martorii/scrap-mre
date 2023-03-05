from sklearn.base import TransformerMixin
import py3langid as langid
import pandas as pd


class Preprocessor(TransformerMixin):
    def __init__(self, nlp=None):
        self.nlp = nlp
    
    @staticmethod
    def lemmatize_and_remove_stopwords(x, nlp):
        """
        Use spacy to clean text
        """
        return ' '.join([w.lemma_ for w in nlp(x) if not w.is_stop])

    def transform(self, X, *_):        
        # Convert to lowercase
        X['cleaned_text'] = X['text'].str.lower()
        
        # Add language column
        X['lang'] = X['cleaned_text'].apply(lambda x: langid.classify(x)[0])

        # Remove symbols
        X['cleaned_text'] = X['cleaned_text'].str.replace(r'[^a-z0-9 ]', ' ', regex=True)

        # Remove multiple spaces
        X['cleaned_text'] = X['cleaned_text'].str.replace(r'[ ]+', ' ', regex=True)

        # Use model to lemmatize and remove stopwords
        if self.nlp:
            X['cleaned_text'] = X['cleaned_text'].apply(
                self.lemmatize_and_remove_stopwords, args=(self.nlp,)
            )

        # Clean multiple spaces
        X['cleaned_text'] = X['cleaned_text'].str.replace(r'[ ]+', ' ', regex=True)

        # Since there are some left chars, remove them.
        X['cleaned_text'] = X['cleaned_text'].apply(lambda x: ' '.join([z for z in x.split() if len(z)>1]))
        
        return X['cleaned_text'].tolist()

    def fit(self, *_):
        return self