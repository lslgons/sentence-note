from pymongo import MongoClient
from datetime import datetime
import pandas as pd
import csv
MONGO_URI="mongodb+srv://superiorgon:Im0FatwK52VzLW8q@cluster0.m81lk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# MongoDB Atlas 연결
client = MongoClient(MONGO_URI)
db = client["english_learning"]
type="mongodb"
sentences_col = None
words_col = None

# DB 초기화 함수
def init_db():
    if "sentences" not in db.list_collection_names():
        db.create_collection("sentences")
    if "words" not in db.list_collection_names():
        db.create_collection("words")
    global sentences_col, words_col
    sentences_col = db["sentences"]
    words_col = db["words"]

# 문장 등록 함수
def add_sentence(korean, english):
    print("add sentence:", english)
    try:
        sentences_col.insert_one({
            "korean": korean,
            "english": english,
            "created_at": datetime.now()
        })
    except Exception as e:
        print("Error:", e)

# 문장 수정 함수
def update_sentence(sentence_id, korean, english):
    sentences_col.update_one(
        {"_id": sentence_id},
        {"$set": {"korean": korean, "english": english}}
    )

# 문장 삭제 함수
def delete_sentence(sentence_id):
    sentences_col.delete_one({"_id": sentence_id})

# 문장 조회 함수
def get_sentences():
    return list(sentences_col.find({}, {"_id": 0}))

# 단어 등록 함수
def add_word(word, meaning):
    print("add word:", word)
    if get_word(word):
        print("already exists:", word)
        return
    try:
        now=datetime.now()
        seq_id=now.strftime("%Y%m%d%H%M%S")
        words_col.insert_one({
            "id": "w"+seq_id,
            "word": word,
            "meaning": meaning,
            "created_at": datetime.now()
        })
    except Exception as e:
        print("Error:", e)

# 단어 수정 함수
def update_word(word_id, word, meaning):
    words_col.update_one(
        {"_id": word_id},
        {"$set": {"word": word, "meaning": meaning}}
    )

# 단어 삭제 함수
def delete_word(word_id):
    words_col.delete_one({"_id": word_id})

# 단어 조회 함수
def get_words():
    #words=list(words_col.find({}, {"_id": 0}))
    words = list(words_col.find({}))
    return words

# 특정 단어 조회 함수
def get_word(word):
    return words_col.find_one({"word": word}, {"_id": 0})

# 문장을 CSV로 내보내기
def export_sentences():
    sentences = get_sentences()
    df = pd.DataFrame(sentences)
    return df.to_csv(index=False)

# 단어를 CSV로 내보내기
def export_words():
    words = get_words()
    df = pd.DataFrame(words)
    return df.to_csv(index=False)

# CSV에서 문장 가져오기
def import_sentences_from_csv(file):
    df = pd.read_csv(file)
    for _, row in df.iterrows():
        add_sentence(row["korean"], row["english"])

# CSV에서 단어 가져오기
def import_words_from_csv(file):
    df = pd.read_csv(file)
    for _, row in df.iterrows():
        add_word(row["word"], row["meaning"])
