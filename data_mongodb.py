from pymongo import MongoClient
from datetime import datetime
from pymongo.server_api import ServerApi
import os
MONGO_URI="mongodb+srv://superiorgon:Im0FatwK52VzLW8q@cluster0.m81lk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# DB 연결 및 컬렉션 생성
def init_db():
    MONGO_DB_URI=os.environ.get("MONGO_DB_URI")
    # Create a new client and connect to the server
    client = MongoClient(MONGO_URI, server_api=ServerApi('1'))

    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
    # client = MongoClient('localhost', 27017)
    db = client['english_learning']
    sentences = db['sentences']
    words = db['words']
    sentences.create_index('english', unique=True)
    words.create_index('word', unique=True)

# 문장 등록 함수
def add_sentence(korean, english):
    print("add sentence: ", english)
    client = MongoClient(MONGO_URI, 27017)
    db = client['english_learning']
    sentences = db['sentences']
    try:
        sentences.insert_one({
            'korean': korean,
            'english': english,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    except Exception as e:
        print(e)
    finally:
        client.close()

# 문장 수정 함수
def update_sentence(sentence_id, korean, english):
    client = MongoClient(MONGO_URI, 27017)
    db = client['english_learning']
    sentences = db['sentences']
    sentences.update_one(
        {'_id': sentence_id},
        {'$set': {
            'korean': korean,
            'english': english
        }}
    )
    client.close()

# 문장 삭제 함수
def delete_sentence(sentence_id):
    client = MongoClient(MONGO_URI, 27017)
    db = client['english_learning']
    sentences = db['sentences']
    sentences.delete_one({'_id': sentence_id})
    client.close()

# 문장 조회 함수
def get_sentences():
    client = MongoClient(MONGO_URI, 27017)
    db = client['english_learning']
    sentences = db['sentences']
    result = list(sentences.find())
    client.close()
    return result

# 단어 등록 함수
def add_word(word, meaning):
    print("add word : ", word)
    word_check = get_word(word)
    if word_check:
        print("already exists: ", word_check)
        return
    client = MongoClient(MONGO_URI, 27017)
    db = client['english_learning']
    words = db['words']
    try:
        words.insert_one({
            'word': word,
            'meaning': meaning,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    except Exception as e:
        print(e)
    finally:
        client.close()

# 단어 수정 함수
def update_word(word_id, word, meaning):
    client = MongoClient(MONGO_URI, 27017)
    db = client['english_learning']
    words = db['words']
    words.update_one(
        {'_id': word_id},
        {'$set': {
            'word': word,
            'meaning': meaning
        }}
    )
    client.close()

# 단어 삭제 함수
def delete_word(word_id):
    client = MongoClient(MONGO_URI, 27017)
    db = client['english_learning']
    words = db['words']
    words.delete_one({'_id': word_id})
    client.close()

# 단어 조회 함수
def get_words():
    client = MongoClient(MONGO_URI, 27017)
    db = client['english_learning']
    words = db['words']
    result = list(words.find())
    client.close()
    return result

def get_word(word: str):
    client = MongoClient(MONGO_URI, 27017)
    db = client['english_learning']
    words = db['words']
    result = words.find_one({'word': word})
    print("get_word: ", result)
    client.close()
    return result
