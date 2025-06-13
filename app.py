import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# --- 認証設定 ---
scope = ["https://www.googleapis.com/auth/spreadsheets"]
credentials = Credentials.from_service_account_info(
    st.secrets["google_service_account"], scopes=scope
)
gc = gspread.authorize(credentials)

# --- Google Sheets 設定 ---
SPREADSHEET_KEY = "1vkAHTQwf4yNkJuJKv1A735wR5GG6feRmJQrAJPsYJ_Q"
worksheet = gc.open_by_key(SPREADSHEET_KEY).worksheet("Sheet1")  # Sheet名に合わせて変更可

# --- Streamlit UI ---
st.title("英語学習記録アプリ（クラウド版）")

name = st.text_input("お名前を入力してください")
activity = st.text_area("今日の学習内容を記録してください")
submitted = st.button("記録を送信")

if submitted and name and activity:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    worksheet.append_row([now, name, activity])
    st.success("記録がGoogle Sheetsに保存されました！")
elif submitted:
    st.warning("全ての項目を入力してください。")
