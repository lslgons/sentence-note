import streamlit as st
import random
import pandas as pd
# from data import *
from data_mongodb3 import *



# 문장 랜덤 퀴즈 함수
def random_sentence_quiz():
    sentences = get_sentences()
    if not sentences:
        st.warning("등록된 문장이 없습니다. 문장을 먼저 등록해주세요.")
        return

    if 'sentence_quiz' not in st.session_state:
        st.session_state.sentence_quiz = random.choice(sentences)
    if 'sentence_input' not in st.session_state:
        st.session_state.sentence_input = ''



    quiz = st.session_state.sentence_quiz
    korean_sentence = quiz[1]
    correct_english = quiz[2]

    st.subheader(f"한국어 문장: {korean_sentence}")
    st.text_input("영문장을 입력하세요:", key='sentence_input')
    def random_sentence_quiz_reset():
        del st.session_state.sentence_quiz
        st.session_state['sentence_input'] = ''

    st.button("다시하기", key='sentence_retry', on_click=random_sentence_quiz_reset)
    if st.button("정답 확인", key='sentence_check'):
        st.subheader(f"""\n
            😊 정답=> {correct_english} \n
            🤔 입력=> {st.session_state.sentence_input}
        """)





# 단어 랜덤 퀴즈 함수
#  애들용은 한글 -> 영어 반대로...
def random_word_quiz():
    words = get_words()
    if not words:
        st.warning("등록된 단어가 없습니다. 단어를 먼저 등록해주세요.")
        return

    print(words)
    if 'word_quiz' not in st.session_state:
        st.session_state.word_quiz = random.choice(words)
    if 'word_input' not in st.session_state:
        st.session_state.word_input = ''
    quiz = st.session_state.word_quiz
    word = quiz[1]
    correct_meaning = quiz[2]
    st.subheader(f"단어: {correct_meaning}")
    st.text_input("영단어을 입력하세요:", key="word_input")

    def random_word_quiz_reset():
        del st.session_state.word_quiz
        st.session_state['word_input'] = ''
    st.button("다시하기", key='word_retry', on_click=random_word_quiz_reset)
    if st.button("정답 확인", key='word_check'):
        st.subheader(f"""\n
            😊 정답=> {word} \n
            🤔 입력=> {st.session_state.word_input}
        """)



st.set_page_config(page_title="🗒️영어노트", layout="wide")

init_db()
st.title("🗒️김우현/김수현 영어노트")
# 탭형 메뉴
menu_tabs = st.tabs(["문장노트", "단어노트", "패턴퀴즈", "단어퀴즈", "⚙️관리"])

with menu_tabs[0]:
    st.subheader("패턴문장")
    sentences = get_sentences()
    if st.button("패턴 새로고침"):
        sentences = get_sentences()
    if sentences:
        df_sentences = pd.DataFrame(sentences, columns=['ID', '한국어 문장', '영문장', '등록일'])
        st.table(df_sentences[['한국어 문장', '영문장', '등록일']])
    else:
        st.write("등록된 문장이 없습니다.")
with menu_tabs[1]:
    st.subheader("주요단어")
    words = get_words()
    if st.button("단어 새로고침"):
        words = get_words()
    if words:
        df_words = pd.DataFrame(words, columns=['ID', '영단어', '뜻', '등록일'])
        st.table(df_words[['영단어', '뜻', '등록일']])
    else:
        st.write("등록된 단어가 없습니다.")

with menu_tabs[2]:
    st.subheader("랜덤 퀴즈 (패턴문장)")
    random_sentence_quiz()


with menu_tabs[3]:
    st.subheader("랜덤 퀴즈 (단어)")
    random_word_quiz()


if 'add_sentence_korean_input' not in st.session_state:
    st.session_state.add_sentence_korean_input=''
if 'add_sentence_english_input' not in st.session_state:
    st.session_state.add_sentence_english_input=''
if 'add_word_korean_input' not in st.session_state:
    st.session_state.add_word_korean_input=''
if 'add_word_english_input' not in st.session_state:
    st.session_state.add_word_english_input=''


def add_word_action():
    print("add_word_action")
    if st.session_state.add_word_korean_input and st.session_state.add_word_english_input:
        add_word(st.session_state.add_word_english_input, st.session_state.add_word_korean_input)
        # st.success("문장이 등록되었습니다!")
        st.session_state.after_add_word_status = "단어가 등록되었습니다."
        st.session_state.add_word_korean_input = ''
        st.session_state.add_word_english_input = ''
    else:
        st.session_state.after_add_word_status = "모든 필드를 입력해주세요."

def add_sentence_action():
    if st.session_state.add_sentence_korean_input and st.session_state.add_sentence_english_input:
        add_sentence(st.session_state.add_sentence_korean_input, st.session_state.add_sentence_english_input)
        # st.success("문장이 등록되었습니다!")
        st.session_state.after_add_status = "문장이 등록되었습니다."
        st.session_state.add_sentence_korean_input = ''
        st.session_state.add_sentence_english_input = ''
    else:
        st.session_state.after_add_status = "모든 필드를 입력해주세요."


with menu_tabs[4]:
    st.header("⚙️ 문장/단어 관리")
    mgmt_tabs=st.tabs(["문장 관리", "단어 관리", "Export/Import"])

    with mgmt_tabs[0]:
        st.subheader("패턴 관리")
        if 'after_add_status' in st.session_state:
            st.success(st.session_state.after_add_status)
        st.text_input("한국어 문장 입력", key='add_sentence_korean_input')
        st.text_input("영문장 입력", key='add_sentence_english_input')

        st.button("문장 등록", on_click=add_sentence_action)

        sentences = get_sentences()
        if sentences:
            df_sentences = pd.DataFrame(sentences, columns=['ID', '한국어 문장', '영문장', '등록일'])

            selected_sentence = st.selectbox("수정하거나 삭제할 문장을 선택하세요", df_sentences['한국어 문장'])
            selected_data = df_sentences[df_sentences['한국어 문장'] == selected_sentence].iloc[0]
            print("====== selected ======")
            print(selected_data)
            print("======================")
            new_korean = st.text_input("수정할 한국어 문장", selected_data['한국어 문장'])
            new_english = st.text_input("수정할 영문장", selected_data['영문장'])
            selected_id = selected_data["ID"]
            if st.button("문장 수정"):
                if new_korean and new_english:
                    update_sentence(selected_id, new_korean, new_english)
                    st.success("문장이 수정되었습니다!")
                else:
                    st.warning("모든 필드를 입력해주세요.")

            if st.button("문장 삭제"):
                delete_sentence(selected_id)
                st.success("문장이 삭제되었습니다!")
                st.rerun()


        else:
            st.write("등록된 문장이 없습니다.")

    with mgmt_tabs[1]:
        st.header("단어 관리")
        if 'after_add_word_status' in st.session_state:
            st.success(st.session_state.after_add_word_status)
        st.text_input("영단어 입력", key="add_word_english_input")
        st.text_input("뜻 입력", key="add_word_korean_input")

        st.button("단어 등록", on_click=add_word_action)

        st.subheader("등록된 단어 목록")
        words = get_words()
        if words:
            df_words = pd.DataFrame(words, columns=['ID', '영단어', '뜻', '등록일'])
            selected_word = st.selectbox("수정하거나 삭제할 단어를 선택하세요", df_words['영단어'])
            selected_data = df_words[df_words['영단어'] == selected_word].iloc[0]
            print("====== selected ======")
            print(selected_data)
            print("======================")
            new_word = st.text_input("수정할 영단어", selected_data['영단어'])
            new_meaning = st.text_input("수정할 뜻", selected_data['뜻'])
            selected_id=selected_data["ID"]
            print(selected_id)
            if st.button("단어 수정"):
                if new_word and new_meaning:
                    update_word(selected_id, new_word, new_meaning)
                    st.success("단어가 수정되었습니다!")
                else:
                    st.warning("모든 필드를 입력해주세요.")

            if st.button("단어 삭제"):
                delete_word(selected_id)
                st.success("단어가 삭제되었습니다!")
                st.rerun()
        else:
            st.write("등록된 단어가 없습니다.")
    with mgmt_tabs[2]:
        # 다운로드 버튼 생성
        st.download_button(
            label="패턴문장 CSV로 다운로드",
            data=export_sentences(),
            file_name=f'sentences_{datetime.today().strftime("%Y%m%d")}.csv',
            mime='text/csv'
        )

        st.download_button(
            label="단어 CSV로 다운로드",
            data=export_words(),
            file_name=f'words_{datetime.today().strftime("%Y%m%d")}.csv',
            mime='text/csv'
        )

        uploaded_sentence_file = st.file_uploader("패턴문장 CSV 업로드", type=["csv"])
        if uploaded_sentence_file is not None:
            import_sentences_from_csv(uploaded_sentence_file)
            st.success("문장이 업로드되었습니다!")

        uploaded_word_file = st.file_uploader("단어 CSV 업로드", type=["csv"])
        if uploaded_word_file is not None:
            import_words_from_csv(uploaded_word_file)
            st.success("단어가 업로드되었습니다!")