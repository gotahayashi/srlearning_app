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

# --- スプレッドシートID（あなたのものを使用） ---
SPREADSHEET_ID = "14KIy8KofniCny13t7qcYhFvUK_DwJ26ftM8lXyDbdE0"  # ← 必ず自分のIDに置き換えてください！
worksheet = gc.open_by_key(SPREADSHEET_ID).sheet1

# --- Streamlit UI ---
st.title("📋 Google Sheets 記録アプリ")

# Secrets 確認（Cloud用デバッグ）
st.write("client_email:", st.secrets["google_service_account"]["client_email"])

name = st.text_input("名前を入力してください")
content = st.text_input("記録内容を入力してください")

if st.button("Google Sheets に記録する"):
    if name and content:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            worksheet.append_row([now, name, content])
            st.success("✅ Google Sheets に記録されました！")
        except Exception as e:
            st.error(f"❌ 書き込み失敗: {e}")
    else:
        st.warning("⚠️ 名前と記録内容を両方入力してください。")
