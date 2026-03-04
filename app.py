import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("key.json")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)
db = firestore.client()

with st.form("input_form"):
    title = st.title("다설의 일정목록")
    task = st.text_input("할 일을 적으세요")
    sub = st.form_submit_button("추가")
if sub:
    st.write(f"{task}추가됨")

if sub and task:
    db.collection("todos").add(
        {
            "content": task,
            "at": firestore.SERVER_TIMESTAMP
        }
    )
    st.rerun()



docs = db.collection("todos").stream()

for doc in docs:
    todo = doc.to_dict()

    col1, col2 = st.columns([8,2]) # col1과 col2를 각각 8:2 크기로 만듬
    
    with col1:
        st.info(todo["content"])
    
    with col2:
        if st.button("삭제", key = doc.id):
            db.collection("todos").document(doc.id).delete()
            st.success("삭제되었습니다!")
            st.rerun()



