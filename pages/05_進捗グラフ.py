import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 🎌 フォントファイルを直接読み込んで FontProperties を作成
FONT_PATH = os.path.join("fonts", "ipaexg.ttf")
if os.path.exists(FONT_PATH):
    font_prop = fm.FontProperties(fname=FONT_PATH)
else:
    font_prop = None  # fallback

# 📄 CSVファイルの読み込み
DATA_PATH = "data/logs.csv"
st.title("📈 学習時間の推移")

try:
    df = pd.read_csv(DATA_PATH)
    df['date'] = pd.to_datetime(df['date'])

    users = df['name'].unique()
    selected_user = st.selectbox("ユーザーを選択してください", users)

    user_data = df[df['name'] == selected_user]
    summary = user_data.groupby('date')['study_time'].sum().reset_index()

    # 📊 グラフ描画
    fig, ax = plt.subplots()
    ax.plot(summary['date'], summary['study_time'], marker='o')

    ax.set_xlabel("日付", fontproperties=font_prop)
    ax.set_ylabel("学習時間（分）", fontproperties=font_prop)
    ax.set_title(f"{selected_user} さんの学習時間の推移", fontproperties=font_prop)
    plt.xticks(rotation=45, fontproperties=font_prop)
    plt.yticks(fontproperties=font_prop)

    st.pyplot(fig)

except FileNotFoundError:
    st.warning(f"学習ログファイルが見つかりませんでした: {DATA_PATH}")
except Exception as e:
    st.error(f"エラーが発生しました: {e}")
