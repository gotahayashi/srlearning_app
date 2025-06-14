import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

st.set_page_config(page_title="ホーム", layout="wide")
st.title("🏠 ホーム - リマインド機能")

# スコープと認証
scope = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
credentials = Credentials.from_service_account_info(
    st.secrets["google_service_account"],
    scopes=scope
)

SHEET_URL = "https://docs.google.com/spreadsheets/d/1vkAHTQwf4yNkJuJKv1A735wR5GG6feRmJQrAJPsYJ_Q"

try:
    gc = gspread.authorize(credentials)
    worksheet = gc.open_by_url(SHEET_URL).sheet1
    records = worksheet.get_all_records()
    df = pd.DataFrame(records)

    # 👇 正確な列名に合わせて修正（全角かっこ含む）
    df["日付（timestamp)"] = pd.to_datetime(df["日付（timestamp)"], errors="coerce")
    df = df.dropna(subset=["日付（timestamp)", "名前"])

    latest_by_user = df.groupby("名前")["日付（timestamp)"].max().reset_index()
    today = datetime.today()

    for _, row in latest_by_user.iterrows():
        name = row["名前"]
        last_date = row["日付（timestamp)"]
        days_diff = (today - last_date).days

        if days_diff > 7:
            st.warning(f"⚠️ {name} さんは {days_diff} 日間記録がありません。忘れず記録しましょう！")
        else:
            st.success(f"✅ {name} さんは {days_diff} 日前に記録しています。")

except Exception as e:
    st.error(f"データの読み込みに失敗しました: {e}")
