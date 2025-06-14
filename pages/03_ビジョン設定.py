import streamlit as st
import pandas as pd
from datetime import date
import gspread
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="ビジョン設定", layout="centered")
st.title("🌟 ビジョン設定フォーム")

# Google認証設定
scope = ["https://www.googleapis.com/auth/spreadsheets"]
credentials = Credentials.from_service_account_info(
    st.secrets["google_service_account"],
    scopes=scope
)
gc = gspread.authorize(credentials)

# 接続するスプレッドシートとシート名
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1vkAHTQwf4yNkJuJKv1A735wR5GG6feRmJQrAJPsYJ_Q"
worksheet = gc.open_by_url(SPREADSHEET_URL).worksheet("visions")  # ← 必ずシート名"visions"と一致

# 入力フォーム
with st.form("vision_form"):
    name = st.text_input("名前")
    grade = st.selectbox("学年", ["1年", "2年", "3年", "4年"])
    title = st.text_input("目標タイトル（例：TOEIC600点達成）")
    content = st.text_area("目標内容（例：毎週4時間、英語の動画を視聴する）")
    deadline = st.date_input("達成期限", value=date.today())

    submitted = st.form_submit_button("保存する")

    if submitted:
        new_row = [name, grade, title, content, str(deadline)]
        worksheet.append_row(new_row)
        st.success("✅ ビジョンをGoogle Sheetsに保存しました！")
