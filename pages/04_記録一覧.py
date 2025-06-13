import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

# --- Google Sheets 認証設定 ---
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
try:
    creds = Credentials.from_service_account_info(
        st.secrets["google_service_account"], scopes=SCOPES
    )
    gc = gspread.authorize(creds)
except Exception as e:
    st.error("❌ Google認証に失敗しました")
    st.code(str(e))
    st.stop()

# --- 新しいスプレッドシートIDに接続 ---
SPREADSHEET_ID = "1vkAHTQwf4yNkJuJKv1A735wR5GG6feRmJQrAJPsYJ_Q"
try:
    spreadsheet = gc.open_by_key(SPREADSHEET_ID)
    sheet = spreadsheet.worksheet("Sheet1")
except Exception as e:
    st.error("❌ Google Sheetsへの接続に失敗しました")
    st.code(str(e))
    st.stop()

# --- 接続診断ログ（初期デバッグ用） ---
st.markdown("### ✅ Google Sheets 接続診断ログ")
st.write("📧 使用中のサービスアカウント:", creds.service_account_email)
st.write("📘 スプレッドシート名:", spreadsheet.title)
st.write("📄 シート一覧:", [ws.title for ws in spreadsheet.worksheets()])
st.write("🗂 使用中のシート:", sheet.title)

# --- 記録一覧の表示 ---
st.markdown("---")
st.subheader("📋 英語学習記録 一覧")

try:
    records = sheet.get_all_values()
    if len(records) > 1:
        headers = ["日付（timestamp）", "名前", "カテゴリ", "分数", "コメント"]
        df = pd.DataFrame(records[1:], columns=headers)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("まだ記録がありません。")
except Exception as e:
    st.error("❌ データ取得時にエラーが発生しました")
    st.code(str(e))
