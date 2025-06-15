import streamlit as st
import pandas as pd
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="ビジョンのふりかえり", layout="centered")
st.title("🎯 ビジョンのふりかえり")

# Google Sheets 認証設定
scope = ["https://www.googleapis.com/auth/spreadsheets"]
credentials = Credentials.from_service_account_info(
    st.secrets["google_service_account"],
    scopes=scope
)
client = gspread.authorize(credentials)

# Google Sheets ID（スプレッドシートのIDのみ）
SPREADSHEET_ID = "1vkAHTQwf4yNkJuJKv1A735wR5GG6feRmJQrAJPsYJ_Q"

# visions・reflections シートの読み込み
try:
    visions_ws = client.open_by_key(SPREADSHEET_ID).worksheet("visions")
    reflections_ws = client.open_by_key(SPREADSHEET_ID).worksheet("reflections")
    visions_df = pd.DataFrame(visions_ws.get_all_records())
    visions_df.columns = visions_df.columns.str.strip()  # ← カラム名の前後スペースを除去
except Exception as e:
    st.error("Google Sheets の読み込みに失敗しました。")
    st.exception(e)
    st.stop()

# デバッグ用: カラム名表示（必要なら有効化）
# st.write("カラム名一覧:", visions_df.columns.tolist())

# 名前の選択
names = sorted(visions_df["名前"].dropna().unique())
if not names:
    st.info("まだビジョンが登録されていません。")
    st.stop()

selected_name = st.selectbox("名前を選んでください", names)

# 選択された学生の最新ビジョンを取得
student_visions = visions_df[visions_df["名前"] == selected_name]
if student_visions.empty:
    st.warning("ビジョンが見つかりません。")
    st.stop()

latest = student_visions.iloc[-1]
title = latest["目標タイトル"]
vision = latest["目標内容"]
deadline = latest["達成期限"]

# ビジョンの表示
st.subheader("🎯 目標タイトル")
st.write(title)

st.subheader("📝 目標内容")
st.write(vision)

st.subheader("📅 達成期限")
st.write(deadline)

# 振り返りコメント入力
st.subheader("💬 振り返りコメント")
reflection = st.text_area("自由にふりかえってみましょう（例：達成できたか、難しかったこと、工夫したことなど）")

# コメント送信処理
if st.button("コメントを送信する"):
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        reflections_ws.append_row([timestamp, selected_name, vision, reflection])
        st.success("コメントを保存しました。おつかれさまでした！")
    except Exception as e:
        st.error("コメントの保存に失敗しました。")
        st.exception(e)
