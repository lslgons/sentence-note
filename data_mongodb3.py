from pymongo import MongoClient
from datetime import datetime
import pandas as pd
import csv

MONGO_URI="mongodb+srv://superiorgon:Im0FatwK52VzLW8q@cluster0.m81lk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
CLIENT_CHILDREN="english_learning_for_children"

# MongoDB Atlas 연결
client = MongoClient(MONGO_URI)
db = client[CLIENT_CHILDREN]

db_type="mongodb"
# DB 초기화 함수
def init_db():
    global sentences_col, words_col

    if "sentences" not in db.list_collection_names():
        db.create_collection("sentences")
    sentences_col = db["sentences"]

    if "words" not in db.list_collection_names():
        db.create_collection("words")
    words_col = db["words"]
    print("Database initialized.")


# 문장 및 단어 컬렉션
init_db()


# 문장 등록 함수
def add_sentence(korean, english):
    print("add sentence:", english)
    if get_sentence(korean):
        print("already exists:", korean)
        return
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
    _sentences=list(sentences_col.find({}))
    return [(s["_id"], s["korean"], s["english"], s["created_at"]) for s in _sentences]

def get_sentence(korean):
    s=sentences_col.find_one({"korean": korean})
    if s:
        return (s["_id"], s["korean"], s["english"], s["created_at"])
    else:
        return None

# 단어 등록 함수
def add_word(word, meaning):
    print("add word:", word)
    if get_word(word):
        print("already exists:", word)
        return
    try:
        words_col.insert_one({
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
    _words=list(words_col.find({}))
    return [(w["_id"], w["word"], w["meaning"], w["created_at"]) for w in _words]


# 특정 단어 조회 함수
def get_word(word):
    w=words_col.find_one({"word": word})
    if w:
        return (w["_id"], w["word"], w["meaning"], w["created_at"])
    else:
        return None

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
    df = pd.read_csv(file,)
    for _, row in df.iterrows():
        if "korean" in row and "english" in row:
            add_sentence(row["korean"], row["english"])


# CSV에서 단어 가져오기
def import_words_from_csv(file):
    df = pd.read_csv(file)
    for _, row in df.iterrows():
        if "word" in row and "meaning" in row:
            add_word(row["word"], row["meaning"])
