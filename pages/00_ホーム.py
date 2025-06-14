import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import gspread
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="リマインド機能", layout="centered")
st.title("🔔 リマインド機能（記録未入力者の確認）")

# Google Sheets 認証
scope = ["https://www.googleapis.com/auth/spreadsheets"]
credentials = Credentials.from_service_account_info(
    st.secrets["google_service_account"],
    scopes=scope
)
client = gspread.authorize(credentials)

# シート設定
SPREADSHEET_ID = "1vkAHTQwf4yNkJuJKv1A735wR5GG6feRmJQrAJPsYJ_Q"
LOGS_SHEET_NAME = "logs"

# データ読み込み
try:
    logs_ws = client.open_by_key(SPREADSHEET_ID).worksheet(LOGS_SHEET_NAME)
    logs_df = pd.DataFrame(logs_ws.get_all_records())
except Exception as e:
    st.error("データの読み込みに失敗しました。")
    st.exception(e)
    st.stop()

# 日付列を変換
try:
    logs_df["日付（timestamp)"] = pd.to_datetime(logs_df["日付（timestamp)"], errors="coerce")
except KeyError:
    st.error("列名 '日付（timestamp)' が見つかりません。Google Sheets のカラム名を確認してください。")
    st.stop()

# 今日の日付と7日前
today = datetime.now()
threshold = today - timedelta(days=7)

# 学生ごとの最新記録日を抽出
latest_logs = logs_df.sort_values("日付（timestamp)").drop_duplicates("名前", keep="last")
inactive_students = latest_logs[latest_logs["日付（timestamp)"] < threshold]

# 表示
st.subheader("🛎 リマインド対象の学生一覧（1週間以上記録なし）")

if inactive_students.empty:
    st.success("全員が最近記録をつけています！")
else:
    st.dataframe(inactive_students[["名前", "日付（timestamp)", "カテゴリ", "分数"]].reset_index(drop=True))
