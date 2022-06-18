import os
import joblib
import numpy as np
import pandas as pd
import tensorflow_text
import tensorflow_hub as hub

from tqdm import tqdm


class STS_USE:
    def __init__(self, raw_data_path: str, embeddings_path: str):
        self.embeddings_path = embeddings_path
        self.df = pd.read_csv(raw_data_path)
        self.use_model = hub.load("https://tfhub.dev/google/universal-sentence-encoder-multilingual-large/3")
        self.compute_embeddings()


    def compute_embeddings(self, refresh: bool = True) -> dict:
        embeddings_dict = {}
        if os.path.exists(self.embeddings_path):
            embeddings_dict = joblib.load(self.embeddings_path)

        if refresh:
            for index, row in tqdm(self.df.iterrows(), total=self.df.shape[0]):
                if index not in embeddings_dict:
                    embeddings_dict[index] = self.use_model(row['text'][:30_000])

        joblib.dump(embeddings_dict, self.embeddings_path)
        return embeddings_dict


    def predict(self, text: str, top_n: int = 2) -> list:
        text_embedding = self.use_model(text)
        embeddings_dict = self.compute_embeddings(refresh=False)
        embed_indexes = list(embeddings_dict.keys())
        embeddings = list(embeddings_dict.values())

        similarity = np.inner(embeddings, text_embedding)
        likelyhood = similarity.flatten()
        arglikelyhood = likelyhood.argsort()[::-1]

        top_similar_texts = []
        for al in arglikelyhood[:top_n]:
            candidate = {
                    'id': embed_indexes[al],
                    'text': self.df.loc[embed_indexes[al], 'text'],
                    'score': float(likelyhood[al])
            }
            top_similar_texts.append(candidate)
        return top_similar_texts


if __name__ == '__main__':
    pass
    # english_sentences = ["dog", "Puppies are nice.", "I enjoy taking long walks along the beach with my dog."]
    # df = pd.DataFrame(english_sentences, columns=["text"])
    # df.to_csv("test_data.csv", index=False, encoding='utf-8')
    
    # pd.read_csv("test_data.csv")
    # sts_use = STS_USE("test_data.csv", "embeddings.joblib")
    # print(sts_use.predict("i am the man"))
