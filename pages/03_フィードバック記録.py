import streamlit as st
from datetime import datetime
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="フィードバック記録", layout="centered")
st.title("🗣️ フィードバック記録")

# Google Sheets 認証
scope = ["https://www.googleapis.com/auth/spreadsheets"]
credentials = Credentials.from_service_account_info(
    st.secrets["google_service_account"],
    scopes=scope
)
client = gspread.authorize(credentials)

# Google Sheets 設定
SPREADSHEET_ID = "1vkAHTQwf4yNkJuJKv1A735wR5GG6feRmJQrAJPsYJ_Q"
LOG_SHEET = "logs"
FEEDBACK_SHEET = "feedback"

# 名前リスト取得（logsシートから）
try:
    logs_df = pd.DataFrame(client.open_by_key(SPREADSHEET_ID).worksheet(LOG_SHEET).get_all_records())
    names = sorted(logs_df["name"].dropna().unique())
except Exception as e:
    st.error("logs シートの読み込みに失敗しました。")
    st.exception(e)
    st.stop()

if not names:
    st.warning("まだ学習記録がありません。先に記録ページで名前を登録してください。")
    st.stop()

selected_name = st.selectbox("フィードバックを送る学生を選んでください", names)

# フィードバック入力フォーム
st.subheader("✏️ コメントを入力")
with st.form("feedback_form"):
    comment = st.text_area("コメント（アドバイス、励ましなど）")
    submitted = st.form_submit_button("保存")

    if submitted:
        if not comment.strip():
            st.warning("コメントが空です。入力してください。")
        else:
            try:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                feedback_ws = client.open_by_key(SPREADSHEET_ID).worksheet(FEEDBACK_SHEET)
                feedback_ws.append_row([timestamp, selected_name, comment])
                st.success("コメントを保存しました。")
            except Exception as e:
                st.error("保存に失敗しました。")
                st.exception(e)

# 過去のフィードバック表示
try:
    feedback_df = pd.DataFrame(client.open_by_key(SPREADSHEET_ID).worksheet(FEEDBACK_SHEET).get_all_records())
    student_feedback = feedback_df[feedback_df["name"] == selected_name]
    if not student_feedback.empty:
        st.subheader("📋 過去のフィードバック一覧")
        st.dataframe(student_feedback.sort_values("timestamp", ascending=False))
    else:
        st.info("この学生への過去のフィードバックはまだありません。")
except Exception as e:
    st.error("過去のフィードバック表示に失敗しました。")
    st.exception(e)
