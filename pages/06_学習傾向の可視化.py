import os
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 🎌 日本語フォントを読み込む
FONT_PATH = os.path.join("fonts", "ipaexg.ttf")
if os.path.exists(FONT_PATH):
    font_prop = fm.FontProperties(fname=FONT_PATH)
else:
    font_prop = None

# 📄 データ読み込み
DATA_PATH = "data/logs.csv"
st.title("📊 学習傾向の可視化")

try:
    df = pd.read_csv(DATA_PATH)

    users = df['name'].unique()
    selected_user = st.selectbox("ユーザーを選択してください", users)

    user_data = df[df['name'] == selected_user]

    # seaborn でカテゴリ別の平均学習時間を可視化
    fig, ax = plt.subplots()
    sns.barplot(
        data=user_data,
        x='task',
        y='study_time',
        estimator='mean',
        ci=None,
        ax=ax
    )

    ax.set_xlabel("タスク", fontproperties=font_prop)
    ax.set_ylabel("平均学習時間（分）", fontproperties=font_prop)
    ax.set_title(f"{selected_user} さんの学習傾向", fontproperties=font_prop)
    plt.xticks(rotation=45, fontproperties=font_prop)
    plt.yticks(fontproperties=font_prop)

    st.pyplot(fig)

except FileNotFoundError:
    st.warning(f"学習ログファイルが見つかりませんでした: {DATA_PATH}")
except Exception as e:
    st.error(f"エラーが発生しました: {e}")
