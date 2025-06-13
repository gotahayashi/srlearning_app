import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Google Sheets のURLまたはID
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/10gxpNJFQ2x0HqkP0nOvixieAI-HTl1kCMiGivt9sO6M/edit#gid=0"

# スコープの定義
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# secrets.tomlから資格情報を取得
credentials = ServiceAccountCredentials.from_json_keyfile_dict(
    st.secrets["google_service_account"], scopes=scope
)

# Google Sheetsに接続
gc = gspread.authorize(credentials)
spreadsheet = gc.open_by_url(SPREADSHEET_URL)
worksheet = spreadsheet.sheet1  # 最初のシートを使用

st.title("📝 学習記録の送信")

# 入力フォーム
with st.form("input_form"):
    name = st.text_input("名前")
    date = st.date_input("日付")
    study_time = st.number_input("学習時間（分）", min_value=0)
    focus = st.slider("集中度（1〜5）", 1, 5)
    environment = st.selectbox("学習環境", ["自宅", "図書館", "カフェ", "その他"])
    textbook = st.text_input("教材")
    period = st.text_input("学期（例：2024春）")

    submitted = st.form_submit_button("送信")

    if submitted:
        # シートに追記
        worksheet.append_row([
            name, str(date), study_time, focus, environment, textbook, period
        ])
        st.success("✅ 記録が送信されました！")
