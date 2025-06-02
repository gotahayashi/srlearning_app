import os
import platform
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

# Cloud向けフォント設定（再キャッシュ含む）
if platform.system() == "Linux":
    os.system("apt-get update && apt-get install -y fonts-ipafont")

    # フォントキャッシュ削除 & 再構築
    import shutil
    cache_dir = os.path.expanduser("~/.cache/matplotlib")
    if os.path.exists(cache_dir):
        shutil.rmtree(cache_dir)
    matplotlib.rcParams['font.family'] = 'IPAexGothic'
else:
    matplotlib.rcParams['font.family'] = 'Yu Gothic'

# データ読み込み
DATA_PATH = "data/logs.csv"
st.title("📈 学習時間の推移")

try:
    df = pd.read_csv(DATA_PATH)
    df['date'] = pd.to_datetime(df['date'])

    users = df['name'].unique()
    selected_user = st.selectbox("ユーザーを選択してください", users)

    user_data = df[df['name'] == selected_user]
    summary = user_data.groupby('date')['study_time'].sum().reset_index()

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
