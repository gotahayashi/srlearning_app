import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# ページ設定
st.set_page_config(page_title="ホーム", layout="wide")
st.title("🏠 ホーム - リマインド機能")

# スコープと認証
scope = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
credentials = Credentials.from_service_account_info(
    st.secrets["google_service_account"],  # secrets.toml に定義されている情報を使用
    scopes=scope
)

# Google Sheets のURL
SHEET_URL = "https://docs.google.com/spreadsheets/d/1vkAHTQwf4yNkJuJKv1A735wR5GG6feRmJQrAJPsYJ_Q"

try:
    # シート接続
    gc = gspread.authorize(credentials)
    worksheet = gc.open_by_url(SHEET_URL).sheet1
    records = worksheet.get_all_records()
    df = pd.DataFrame(records)

    # 日付変換とデータ整形
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df = df.dropna(subset=["timestamp", "名前"])

    # 各ユーザーの最新記録取得
    latest_by_user = df.groupby("名前")["timestamp"].max().reset_index()
    today = datetime.today()

    # メッセージ表示
    for _, row in latest_by_user.iterrows():
        name = row["名前"]
        last_date = row["timestamp"]
        days_diff = (today - last_date).days

        if days_diff > 7:
            st.warning(f"⚠️ {name} さんは {days_diff} 日間記録がありません。忘れず記録しましょう！")
        else:
            st.success(f"✅ {name} さんは {days_diff} 日前に記録しています。")

except Exception as e:
    st.error(f"データの読み込みに失敗しました: {e}")
