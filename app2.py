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
    st.title("다설의 다이어리")

    if st.button("로그아웃"):
        st.session_state["login"] = False
        st.rerun()
else:
    tab1, tab2 = st.tabs(["로그인", "회원가입"])

    with tab1:
        st.header("로그인")
        login_id = st.text_input("아이디", key = "login_id")
        login_pw = st.text_input("비밀번호", type = "password", key = "login_pw")

        if st.button("로그인"):
            if not login_id or not login_pw:
                st.warning("아이디와 비밀번호를 모두 입력해주세요.")
        else:
            user_doc = db.collection("users").document(login_id).get()
            if user_doc.exists and user_doc.to_dict()["password"] == login_pw:
                st.session_state["login"] = True
                st.session_state["user_id"] = login_id
                st.rerun()
            else:
                st.error("아이디 또는 비밀번호가 틀렸습니다.")
    
    with tab2:
        st.header("회원가입")
        new_id = st.text_input("사용할 아이디", key = "new_id")
        new_pw = st.text_input("사용할 비밀번호", type = "password", key = "new_pw")
        confirm_pw = st.text_input("사용할 비밀번호", type = "password", key = "confirm_pw")

        if st.button("가입하기"):
            if new_pw != confirm_pw:
                st.error("비밀번호가 일치하지 않습니다.")
            elif not new_id or not new_pw:
                st.error("아이디와 비밀번호를 모두 입력해주세요.")
            else:
                db.collection("users").document(new_id).set({"password": new_pw})
                st.success("회원가입 완료! 로그인 탭에서 접속하세요.")  


if st.session_state["login"]:
    with st.form("todo_form"):
        st.title("다설의 다이어리")
        task1 = st.text_input("할 일을 입력하세요")
        task2 = st.text_input("할 일을 입력하세요")
        task3 = st.text_input("할 일을 입력하세요")
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
            col1, col2, col3, col4 = st.columns([2.5, 2.5, 2.5, 2.5])
            with col1:
                st.info(todo["content1"])
            with col2:
                st.info(todo["content2"])
            with col3:
                st.info(todo["content3"])
            with col4:
                timestamp = todo.get("at")
                st.info(str(timestamp))
            if st.button("삭제", key=doc.id):
                db.collection("todos").document(doc.id).delete()
                st.success("삭제되었습니다!")
                st.rerun()