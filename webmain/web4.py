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
    st.title("다설의 다이어리📝")

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
                user_doc = db.collection("users").document(new_id).get()

            if user_doc.exists:
                st.error("이미 존재하는 아이디입니다.")
            else:
                user_doc = db.collection("users").document(new_id).get()

                if user_doc.exists:
                    st.error("이미 존재하는 아이디입니다.")
                else:
                    db.collection("users").document(new_id).set({
                        "password": new_pw
                    })
                    st.success("회원가입 완료! 로그인 탭에서 접속하세요.")  


if st.session_state["login"]:
    with st.form("todo_form"):
        st.title("할 일 일정")
        category = st.selectbox("카테고리 선택", ["공부", "운동", "요리", "휴식"])

        task1 = st.text_input("할 일을 입력하세요 1")
        task2 = st.text_input("할 일을 입력하세요 2")
        task3 = st.text_input("할 일을 입력하세요 3")
        sub = st.form_submit_button("추가")

    if sub and task1 and task2 and task3:
        db.collection("todos").add(
            {
                "category": category,
                "content1": task1,
                "content2": task2,
                "content3": task3,
                "at": firestore.SERVER_TIMESTAMP 
            }
            )
        st.success(f"{category} 항목이 저장되었습니다!")
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

            st.write("카테고리:", todo.get("category", "미정"))    
            
            if st.button("삭제", key=doc.id):
                db.collection("todos").document(doc.id).delete()
                st.success("삭제되었습니다!")
                st.rerun()

    st.title("🧮 간단한 계산기")

    # 숫자 입력
    num1 = st.number_input("첫 번째 숫자", value=0)
    num2 = st.number_input("두 번째 숫자", value=0)

    # 연산 선택
    operation = st.selectbox("연산 선택", ["더하기", "빼기", "곱하기", "나누기"])

    # 계산 버튼
    if st.button("계산"):
        if operation == "더하기":
            result = num1 + num2
        elif operation == "빼기":
            result = num1 - num2
        elif operation == "곱하기":
            result = num1 * num2
        elif operation == "나누기":
            if num2 != 0:
                result = num1 / num2
            else:
                st.error("0으로 나눌 수 없습니다.")
                result = None

        if result is not None:
            st.success(f"결과: {result}")

with st.sidebar:
    st.header("오늘 정보") 

    if "show_balloon" not in st.session_state:
        st.session_state.show_balloon = False

    if st.button("응원받기"):
        st.toast("잘 먹고 잘 살자 🎉")
        st.session_state.show_balloon = True

    if st.session_state.show_balloon:
        st.balloons()
        st.session_state.show_balloon = False





