import streamlit as st
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

st.set_page_config(page_title="フィードバック記録", layout="centered")
st.title("🗣️ フィードバック記録")

# Google Sheets 認証
scope = ["https://www.googleapis.com/auth/spreadsheets"]
credentials = Credentials.from_service_account_info(
    st.secrets["google_service_account"],
    scopes=scope
)
client = gspread.authorize(credentials)

# スプレッドシート設定
SPREADSHEET_ID = "1vkAHTQwf4yNkJuJKv1A735wR5GG6feRmJQrAJPsYJ_Q"
FEEDBACK_SHEET_NAME = "feedback"

# フィードバック入力フォーム
st.subheader("✏️ フィードバックを記入")
with st.form("feedback_form"):
    comment = st.text_area("コメント内容を入力してください")
    submitted = st.form_submit_button("送信")

    if submitted:
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            feedback_ws = client.open_by_key(SPREADSHEET_ID).worksheet(FEEDBACK_SHEET_NAME)
            feedback_ws.append_row([timestamp, comment])
            st.success("フィードバックを保存しました。")
        except Exception as e:
            st.error("保存に失敗しました。")
            st.exception(e)

# 過去のフィードバック表示
try:
    feedback_ws = client.open_by_key(SPREADSHEET_ID).worksheet(FEEDBACK_SHEET_NAME)
    feedback_df = pd.DataFrame(feedback_ws.get_all_records())

    if not feedback_df.empty:
        st.subheader("📋 過去のフィードバック一覧")
        st.dataframe(feedback_df.sort_values("timestamp", ascending=False))
    else:
        st.info("まだフィードバックは記録されていません。")

except Exception as e:
    st.warning("フィードバック一覧の読み込みに失敗しました。")
    st.exception(e)
