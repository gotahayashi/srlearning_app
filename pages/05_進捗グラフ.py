import os
import platform
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

# 🔤 日本語フォントの設定（Cloud / ローカル 両対応）
if platform.system() == "Linux":
    os.system("apt-get update && apt-get install -y fonts-ipafont")
    matplotlib.rc('font', family='IPAexGothic')
else:
    matplotlib.rc('font', family='Yu Gothic')

# 📄 CSVファイル読み込み
DATA_PATH = "data/logs.csv"

# 📊 グラフページ本体
st.title("📈 学習時間の推移")

try:
    df = pd.read_csv(DATA_PATH)
    df['date'] = pd.to_datetime(df['date'])

    # ユーザー選択（フィルター）
    users = df['name'].unique()
    selected_user = st.selectbox("ユーザーを選択してください", users)

    # フィルター適用
    user_data = df[df['name'] == selected_user]

    # 日付ごとの学習時間の合計を表示
    summary = user_data.groupby('date')['study_time'].sum().reset_index()

    # グラフ描画
    fig, ax = plt.subplots()
    ax.plot(summary['date'], summary['study_time'], marker='o')
    ax.set_xlabel("日付")
    ax.set_ylabel("学習時間（分）")
    ax.set_title(f"{selected_user} さんの学習時間の推移")
    plt.xticks(rotation=45)
    st.pyplot(fig)

except FileNotFoundError:
    st.warning(f"学習ログファイルが見つかりませんでした: {DATA_PATH}")
except Exception as e:
    st.error(f"エラーが発生しました: {e}")
