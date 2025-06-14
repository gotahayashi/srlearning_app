import streamlit as st
import pandas as pd
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="フィードバック記録", layout="centered")
st.title("🗣️ フィードバック記録")

# --- Google Sheets 認証 ---
scope = ["https://www.googleapis.com/auth/spreadsheets"]
credentials = Credentials.from_service_account_info(
    st.secrets["google_service_account"],
    scopes=scope
)
client = gspread.authorize(credentials)

# --- スプレッドシートIDとシート名 ---
SPREADSHEET_ID = "1vkAHTQwf4yNkJuJKv1A735wR5GG6feRmJQrAJPsYJ_Q"
LOGS_SHEET_NAME = "logs"
FEEDBACK_SHEET_NAME = "feedback"

# --- logs シートから名前リストを取得 ---
try:
    logs_ws = client.open_by_key(SPREADSHEET_ID).worksheet(LOGS_SHEET_NAME)
    logs_df = pd.DataFrame(logs_ws.get_all_records())
    logs_df.columns = [c.strip() for c in logs_df.columns]  # 念のため空白除去

    if "名前" not in logs_df.columns:
        st.error("logsシートに「名前」列が見つかりません。")
        st.stop()

    names = sorted(logs_df["名前"].dropna().astype(str).unique())

except Exception as e:
    st.error("logs シートの読み込みに失敗しました。")
    st.exception(e)
    st.stop()

if not names:
    st.warning("まだ学習記録がありません。先に記録ページで名前を登録してください。")
    st.stop()

selected_name = st.selectbox("フィードバックを送る学生を選んでください", names)

# --- フィードバック記入フォーム ---
st.subheader("✏️ フィードバックを記入")
with st.form("feedback_form"):
    comment_type = st.radio("コメントの種類を選択", ["vision", "logs", "reflection"])
    comment = st.text_area("コメント内容を入力してください")
    submitted = st.form_submit_button("送信")

    if submitted:
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            feedback_ws = client.open_by_key(SPREADSHEET_ID).worksheet(FEEDBACK_SHEET_NAME)
            feedback_ws.append_row([timestamp, selected_name, comment_type, comment])
            st.success("フィードバックを保存しました。")
        except Exception as e:
            st.error("フィードバックの保存に失敗しました。")
            st.exception(e)

# --- フィードバック一覧の表示 ---
try:
    feedback_ws = client.open_by_key(SPREADSHEET_ID).worksheet(FEEDBACK_SHEET_NAME)
    feedback_df = pd.DataFrame(feedback_ws.get_all_records())
    feedback_df.columns = [c.strip().lower() for c in feedback_df.columns]  # 列名を整える

    # デバッグ用に列名確認したい場合（必要に応じて）
    # st.write("列名:", feedback_df.columns.tolist())

    if "name" not in feedback_df.columns:
        st.error("feedbackシートに 'name' 列が見つかりません。")
        st.stop()

    student_feedback = feedback_df[feedback_df["名前"] == selected_name]

    if not student_feedback.empty:
        st.subheader("📋 過去のフィードバック一覧")
        st.dataframe(student_feedback.sort_values("timestamp", ascending=False))
    else:
        st.info("この学生へのフィードバックはまだありません。")

except Exception as e:
    st.warning("フィードバック一覧の読み込みに失敗しました。")
    st.exception(e)
