import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from datetime import datetime
from make_vision_page import show_vision_page
from make_page import show_input_page

# --- ページ全体の設定はここだけ ---
st.set_page_config(page_title="英語学習ログ", layout="wide")

# Google認証設定
scope = ["https://www.googleapis.com/auth/spreadsheets"]
credentials = Credentials.from_service_account_info(
    st.secrets["google_service_account"], scopes=scope
)
gc = gspread.authorize(credentials)

# Google Sheets設定
SPREADSHEET_KEY = "1vkAHTQwf4yNkJuJKv1A735wR5GG6feRmJQrAJPsYJ_Q"
worksheet = gc.open_by_key(SPREADSHEET_KEY).worksheet("logs")

# サイドバー メニュー設定
st.sidebar.title("📘 メニュー")
page = st.sidebar.radio("ページを選択", ["🌟 Visionの作成", "📝 学習ログの記録", "📊 ログの一覧"])

# ページごと表示
if page == "🌟 Visionの作成":
    show_vision_page()

elif page == "📝 学習ログの記録":
    show_input_page(worksheet)

elif page == "📊 ログの一覧":
    st.subheader("📊 ログ一覧")
    data = worksheet.get_all_records()
    df = pd.DataFrame(data)
    if not df.empty:
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df = df.sort_values("timestamp", ascending=False)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("まだ記録がありません。")
