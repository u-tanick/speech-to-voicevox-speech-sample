import streamlit as st

# ページの設定
st.set_page_config(
    page_title="Awesome Question",
    layout="wide"
)

# カスタムCSSを定義
custom_css = """
<style>
    .st-emotion-cache-h4xjwg {
        display: none;
    }
    .st-emotion-cache-1jicfl2 {
        width: 100%;
        padding: 1rem 2rem 1rem;
    }
    .stButton {
        text-align: center;
    }
    .st-emotion-cache-1cfn047{
        background-color: #339933;
    }
    .st-emotion-cache-1cfn047:hover{
        color: white !important;
        border-color: black !important;;
        background-color: #00CCFF !important;
    }
    .st-emotion-cache-1cfn047:focus:not(:active) {
        color: white !important;
        border-color: black !important;;
    }
    .st-b6 {
        font-size: 6rem;
    }
    .st-emotion-cache-eq2h7m p {
        font-size: 3rem;
    }
</style>
"""

# CSSを適用
st.markdown(custom_css, unsafe_allow_html=True)

# セッションステートを使用して質問と応答を管理
if 'question' not in st.session_state:
    st.session_state.question = ""
if 'response' not in st.session_state:
    st.session_state.response = ""

# タイトル
st.session_state.question = st.text_area("ご質問内容", value=st.session_state.question, height=400)

# AIの回答表示エリア
st.session_state.response = st.text_area("生成AIの回答", value=st.session_state.response, height=500)

# 2つのカラムに分割
col1, col2 = st.columns(2)

# 各カラムにボタンを配置
with col1:
    # クリアボタン (なぜか2回押さないとクリアされない)
    if st.button("表示クリア（会話履歴は残す）"):
        # ボタンを押した際にセッションステートを更新
        st.session_state.question = ""
        st.session_state.response = ""

with col2:
    if st.button("会話履歴クリア（新規に質問する場合）"):
        st.session_state.question = ""
        st.session_state.response = ""
        # historyをクリアする処理
