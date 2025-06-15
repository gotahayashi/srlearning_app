import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import pandas as pd

# --- Google Sheets 認証設定 ---
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
creds = Credentials.from_service_account_info(
    st.secrets["google_service_account"], scopes=SCOPES
)
gc = gspread.authorize(creds)

# --- スプレッドシートと logs シートを指定 ---
SPREADSHEET_ID = "1vkAHTQwf4yNkJuJKv1A735wR5GG6feRmJQrAJPsYJ_Q"
sheet = gc.open_by_key(SPREADSHEET_ID).worksheet("logs")  # ← logsシートを明示的に指定

# --- タイトル ---
st.title("📘 英語学習記録フォーム")

# --- 入力フォーム ---
name = st.text_input("🧑 名前（任意）")
category = st.selectbox("📚 学習カテゴリ", ["読む", "聞く", "話す", "書く", "単語", "文法", "その他"])
minutes = st.number_input("⏱ 学習時間（分）", min_value=1, step=1)
comment = st.text_area("📝 コメント・振り返り")

# --- 記録送信 ---
if st.button("✅ Google Sheetsに保存"):
    new_row = [
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        name or "",
        category or "",
        str(minutes),
        comment or ""
    ]

    st.write("📤 送信予定データ:")
    st.json(new_row)

    try:
        result = sheet.append_row(new_row)
        st.success("✅ Google Sheets に保存されました！（logsシート）")
    except Exception as e:
        st.error("❌ Google Sheets への保存に失敗しました")
        st.code(str(e))
        result = None

    # --- ログを try の外で出力 ---
    st.write("📌 append_row の戻り値:", result)
    st.write("✅ 認証中のサービスアカウント:", creds.service_account_email)
    st.write("✅ 接続中のシート名:", sheet.title)  # ← ← ← シート名を確認
    worksheets = gc.open_by_key(SPREADSHEET_ID).worksheets()
    st.write("📋 スプレッドシート内のシート一覧:", [ws.title for ws in worksheets])
    st.write("📄 現在のシート内容（先頭5行）:", sheet.get_all_values()[:5])

# --- 区切り線と記録一覧の見出し ---
st.markdown("---")
st.subheader("📄 過去の記録一覧")

# --- 一覧表示 ---
try:
    records = sheet.get_all_values()
    if len(records) > 1:
        headers = ["日付（timestamp）", "名前", "カテゴリ", "分数", "コメント"]
        data = records[1:]
        df = pd.DataFrame(data, columns=headers)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("まだ記録がありません。")
except Exception as e:
    st.error("❌ データ取得エラー")
    st.code(str(e))
