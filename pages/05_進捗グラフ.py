import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime, timedelta

st.set_page_config(page_title="📊 週間学習時間", layout="centered")
st.title("📊 ユーザー別・直近1週間の学習時間")

# 🎌 日本語フォント（存在する場合に使う）
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
    logs_df = pd.DataFrame(logs_ws.get_all_records())

    # ✅ 日本語列名を英語に変換（前後の空白も対応）
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

    # ⏱️ 日付・数値変換 + 欠損除去
    logs_df['date'] = pd.to_datetime(logs_df['date'], errors='coerce')
    logs_df['study_time'] = pd.to_numeric(logs_df['study_time'], errors='coerce')
    logs_df = logs_df.dropna(subset=['date', 'study_time', 'name'])

    # 📆 直近7日間に絞る
    today = datetime.today()
    one_week_ago = today - timedelta(days=7)
    recent_logs = logs_df[logs_df['date'] >= one_week_ago]

    # 👥 ユーザー別に合計時間を算出
    summary = recent_logs.groupby('name')['study_time'].sum().sort_values(ascending=True)

    if summary.empty:
        st.info("直近1週間の記録が見つかりませんでした。")
    else:
        # 📊 横棒グラフ描画
        fig, ax = plt.subplots()
        ax.barh(summary.index, summary.values)

        ax.set_xlabel("学習時間（分）", fontproperties=font_prop)
        ax.set_title("直近1週間の学習時間（ユーザー別）", fontproperties=font_prop)
        plt.xticks(fontproperties=font_prop)
        plt.yticks(fontproperties=font_prop)

        st.pyplot(fig)

except Exception as e:
    st.error(f"エラーが発生しました: {e}")
