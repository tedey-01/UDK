# UDK  
## Микросервис
Сервис предназначен для решения задачи STS - Semantic Textual Similarity. 

## Модель 
В качестве модели используется [universal-sentence-encoder-multilingual-large](https://tfhub.dev/google/universal-sentence-encoder-multilingual-large/3)


## Развёртывание
Структура проекта:  
- `data_parser.py` - Модуль парсинга данных из электронной библиотеки 
- `data_convertor.py` - Модуль реструктуризации распаршенных данных 
- `cloud_loader.py` - Модуль загрузки/выгрузки данных/эмбеддингов в облачное хранилище
- `use_model.py` - Модуль взаимодействия с моделью 
- `sts_webserver.py` - Бэк на Flask

Пример развёртывания 
```bacs
$ cd src 
$ python sts_webserver.py
```

Скрипт эмуляции клиента 
```python
import json
import requests

text = <YOUR TEXT>

url = 'http://0.0.0.0:5050/find_similar'
response = requests.post(url=url, json={'text': text, 'top_n': 2})
print(response.text)
```