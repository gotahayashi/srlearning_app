import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns

# 🎌 日本語フォントの読み込み
FONT_PATH = os.path.join("fonts", "ipaexg.ttf")
if os.path.exists(FONT_PATH):
    font_prop = fm.FontProperties(fname=FONT_PATH)
else:
    font_prop = None

# 📄 データ読み込み
DATA_PATH = "data/logs.csv"
st.title("📅 学期ごとの学習時間比較")

try:
    df = pd.read_csv(DATA_PATH)
    df['date'] = pd.to_datetime(df['date'])

    users = df['name'].unique()
    selected_user = st.selectbox("ユーザーを選択してください", users)

    user_data = df[df['name'] == selected_user]

    # 学期（period）ごとの合計学習時間
    summary = user_data.groupby('period')['study_time'].sum().reset_index()

    fig, ax = plt.subplots()
    sns.barplot(data=summary, x='period', y='study_time', ax=ax)

    # ラベルとタイトルにフォントを明示指定（ここが超重要）
    ax.set_xlabel("学期", fontproperties=font_prop)
    ax.set_ylabel("合計学習時間（分）", fontproperties=font_prop)
    ax.set_title(f"{selected_user} さんの学期ごとの学習時間", fontproperties=font_prop)
    ax.set_xticklabels(ax.get_xticklabels(), fontproperties=font_prop)
    ax.set_yticklabels(ax.get_yticklabels(), fontproperties=font_prop)

    st.pyplot(fig)

except FileNotFoundError:
    st.warning(f"学習ログファイルが見つかりませんでした: {DATA_PATH}")
except Exception as e:
    st.error(f"エラーが発生しました: {e}")
