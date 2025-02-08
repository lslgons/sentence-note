import sqlite3
from datetime import datetime
import pandas as pd
# DB 연결 및 테이블 생성
def init_db():
    conn = sqlite3.connect('english_learning.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS sentences (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    korean TEXT NOT NULL,
                    english TEXT NOT NULL UNIQUE,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP)''')
    c.execute('''CREATE TABLE IF NOT EXISTS words (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    word TEXT NOT NULL UNIQUE,
                    meaning TEXT NOT NULL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

# 문장 등록 함수
def add_sentence(korean, english):
    print("add sentence: ", english)
    conn = sqlite3.connect('english_learning.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO sentences (korean, english, created_at) VALUES (?, ?, ?)", (korean, english, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        conn.commit()
    except Exception as e:
        pass
    finally:
        conn.close()

# 문장 수정 함수
def update_sentence(sentence_id, korean, english):
    conn = sqlite3.connect('english_learning.db')
    c = conn.cursor()
    c.execute("UPDATE sentences SET korean = ?, english = ? WHERE id = ?", (korean, english, sentence_id))
    conn.commit()
    conn.close()

# 문장 삭제 함수
def delete_sentence(sentence_id):
    conn = sqlite3.connect('english_learning.db')
    c = conn.cursor()
    c.execute("DELETE FROM sentences WHERE id = ?", (sentence_id,))
    conn.commit()
    conn.close()

# 문장 조회 함수
def get_sentences():
    conn = sqlite3.connect('english_learning.db')
    c = conn.cursor()
    c.execute("SELECT * FROM sentences")
    sentences = c.fetchall()
    conn.close()
    return sentences

# 단어 등록 함수
def add_word(word, meaning):
    print("add word : ", word)
    word_check=get_word(word)
    if word_check:
        print("already exists: ", word_check)
        return
    conn = sqlite3.connect('english_learning.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO words (word, meaning, created_at) VALUES (?, ?, ?)", (word, meaning, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        conn.commit()
    except Exception as e:
        pass
    finally:
        conn.close()

# 단어 수정 함수
def update_word(word_id, word, meaning):
    conn = sqlite3.connect('english_learning.db')
    c = conn.cursor()
    c.execute("UPDATE words SET word = ?, meaning = ? WHERE id = ?", (word, meaning, word_id))
    conn.commit()
    conn.close()

# 단어 삭제 함수
def delete_word(word_id):
    conn = sqlite3.connect('english_learning.db')
    c = conn.cursor()
    c.execute("DELETE FROM words WHERE id = ?", (word_id,))
    conn.commit()
    conn.close()

# 단어 조회 함수
def get_words():
    conn = sqlite3.connect('english_learning.db')
    c = conn.cursor()
    c.execute("SELECT * FROM words")
    words = c.fetchall()
    conn.close()
    return words

def get_word(word: str):
    conn = sqlite3.connect('english_learning.db')
    c = conn.cursor()
    c.execute(f"SELECT * FROM words where word='{word}'")
    word = c.fetchone()
    print("get_word: ", word)
    conn.close()
    return word

def export_sentences_from_sqlite():
    conn = sqlite3.connect('english_learning.db')
    query = "SELECT * FROM sentences"  # 원하는 테이블을 선택
    df = pd.read_sql(query, conn)
    conn.close()
    return df.to_csv(index=False)

def export_words_from_sqlite():
    conn = sqlite3.connect('english_learning.db')
    query = "SELECT * FROM words"  # 원하는 테이블을 선택
    df = pd.read_sql(query, conn)
    conn.close()
    return df.to_csv(index=False)