import pandas as pd 
import numpy as np
import os 
import re 
# pip install PyMuPDF for fitz (PDF parser)
import fitz

DATA_PATH = os.path.join('..', 'data_1')


def extract_udk(filename: str):
    target = re.findall(r'УДК-.*_https', filename)
    if target:
        target = target[0].lstrip('УДК-').rstrip('_https')
    return target


def fill_dataset(data_path: str):
    docs_names = [file for file in os.listdir(data_path) if file[-3:] == 'pdf']
    texts, udks = [], []
    for doc_name in docs_names:
        doc_path = os.path.join(data_path, doc_name)
        udks.append(extract_udk(doc_name))
        
        full_text = ''
        f = fitz.open(doc_path)
        for page in f:
            text = re.sub(r"[-\n\t]*", "", page.get_text())
            full_text += text
        texts.append(full_text)

    return pd.DataFrame(np.array([texts, udks]).transpose(), columns=['text', 'udk'])


if __name__ == '__main__':
    dataset_path =  os.path.join(DATA_PATH, 'dataset.csv')
    df = fill_dataset(DATA_PATH)
    df.to_csv(dataset_path, index=False)


# def drop_trash_from_udk(udk:str) ->str:
#     udk = re.sub(r'\+.*', '', udk)
#     return udk


# print("LEN: ", len(docs_names))
# for doc in docs_names:
#     target = re.findall(r'УДК-.*_https', doc)
#     if target:
#         target = target[0].lstrip('УДК-').rstrip('_https')
#         first_target = drop_trash_from_udk(target)
#     print(f"\ntarget: {target}\nfirst_target: {first_target}")