import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import gspread
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="📈 進捗グラフ", layout="centered")
st.title("📈 学習時間の推移（Google Sheets版）")

# 🎌 日本語フォント読み込み（存在すれば）
FONT_PATH = os.path.join("fonts", "ipaexg.ttf")
font_prop = fm.FontProperties(fname=FONT_PATH) if os.path.exists(FONT_PATH) else None

# 🔐 Google Sheets 認証
scope = ["https://www.googleapis.com/auth/spreadsheets"]
credentials = Credentials.from_service_account_info(
    st.secrets["google_service_account"],
    scopes=scope
)
gc = gspread.authorize(credentials)

# 📄 シート読み込み
SPREADSHEET_ID = "1vkAHTQwf4yNkJuJKv1A735wR5GG6feRmJQrAJPsYJ_Q"

try:
    logs_ws = gc.open_by_key(SPREADSHEET_ID).worksheet("logs")
    visions_ws = gc.open_by_key(SPREADSHEET_ID).worksheet("visions")

    # 🧮 データ取得
    logs_df = pd.DataFrame(logs_ws.get_all_records())
    visions_df = pd.DataFrame(visions_ws.get_all_records())

    # ✅ 列名の柔軟変換（前後の空白を除去して判定）
    rename_map = {}
    for col in logs_df.columns:
        col_clean = col.strip()
        if "日付" in col_clean:
            rename_map[col] = "date"
        elif "名前" in col_clean:
            rename_map[col] = "name"
        elif "分数" in col_clean:
            rename_map[col] = "study_time"
    logs_df.rename(columns=rename_map, inplace=True)

    # ✅ 日付・数値変換 + 欠損除外
    logs_df['date'] = pd.to_datetime(logs_df['date'], errors='coerce')
    logs_df['study_time'] = pd.to_numeric(logs_df['study_time'], errors='coerce')
    logs_df = logs_df.dropna(subset=['date', 'study_time', 'name'])

    # 📋 ユーザー選択
    users = logs_df['name'].unique()
    selected_user = st.selectbox("ユーザーを選択してください", users)

    # 📊 ユーザーの学習ログから推移を集計
    user_logs = logs_df[logs_df['name'] == selected_user]
    summary = user_logs.groupby('date')['study_time'].sum().reset_index()

    # 🎯 Vision 表示（あれば）
    user_vision = visions_df[visions_df['name'] == selected_user]
    if not user_vision.empty:
        st.info(f"🎯 ビジョン: {user_vision.iloc[0].get('vision', '（未記入）')}")

    # 📈 グラフ表示
    fig, ax = plt.subplots()
    ax.plot(summary['date'], summary['study_time'], marker='o')

    ax.set_title(f"{selected_user} さんの学習時間の推移", fontproperties=font_prop)
    ax.set_xlabel("日付", fontproperties=font_prop)
    ax.set_ylabel("学習時間（分）", fontproperties=font_prop)
    plt.xticks(rotation=45, fontproperties=font_prop)
    plt.yticks(fontproperties=font_prop)

    st.pyplot(fig)

except Exception as e:
    st.error(f"エラーが発生しました: {e}")
