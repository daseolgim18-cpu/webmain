import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("key.json")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)
db = firestore.client()

if "login" not in st.session_state:
    st.session_state["login"] = False

if st.session_state["login"]:
    with st.form("input_form"):
        title = st.title("다설의 일정목록")
        task1 = st.text_input("할 일을 적으세요1")
        task2 = st.text_input("할 일을 적으세요2")
        task3 = st.text_input("할 일을 적으세요3")
        sub = st.form_submit_button("추가")

    if sub and task1 and task2 and task3:
        db.collection("todos").add(
        {           
            "content1": task1,
            "content2": task2,
            "content3": task3,
            "at": firestore.SERVER_TIMESTAMP
        }
        )
        st.rerun()

    docs = db.collection("todos").stream()

    for doc in docs:
        todo = doc.to_dict()

        col1, col2, col3, col4, col5 = st.columns([2,2,2,2,2]) 
    
        with col1:
            st.info(todo["content1"])
        with col2:
            st.info(todo["content2"])
        with col3:
            st.info(todo["content3"])
    
        with col4:
            st.info(todo["at"])
    
        with col5:
            if st.button("삭제", key = doc.id):
               db.collection("todos").document(doc.id).delete()
               st.success("삭제되었습니다!")
               st.rerun()

    if st.button("로그아웃"):
       st.session_state["login"] = False
       st.rerun()
else:
    st.title("로그인 하세요")
    password = st.text_input("비밀번호를 입력하세요", type="password")
    if st.button("로그인"):
        if password == "0226": # 원하는 비밀번호 설정
            st.session_state["login"] = True
            st.rerun()
        else:
            st.error("비밀번호가 틀렸습니다.")


   