import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib

# 日本語フォントの設定
matplotlib.rcParams['font.family'] = 'MS Gothic'

st.set_page_config(page_title="学習傾向の可視化", layout="wide")
st.title("📊 学習傾向の可視化")

DATA_PATH = "data/logs.csv"

if os.path.exists(DATA_PATH):
    logs = pd.read_csv(DATA_PATH)

    # 日付の型変換
    if "date" in logs.columns:
        logs["date"] = pd.to_datetime(logs["date"], errors="coerce")

    # 数値変換（必要な列がある場合）
    logs["study_time"] = pd.to_numeric(logs["study_time"], errors="coerce")
    logs["focus"] = pd.to_numeric(logs["focus"], errors="coerce")

    # 学習環境ごとの集中度平均
    if "environment" in logs.columns and "focus" in logs.columns:
        st.subheader("環境別の平均集中度")
        env_focus = logs.groupby("environment")["focus"].mean().reset_index()
        fig1, ax1 = plt.subplots()
        sns.barplot(data=env_focus, x="environment", y="focus", ax=ax1)
        ax1.set_title("学習環境と集中度の関係")
        st.pyplot(fig1)

    # 教材ごとの平均学習時間
    if "material" in logs.columns and "study_time" in logs.columns:
        st.subheader("教材別の平均学習時間")
        mat_time = logs.groupby("material")["study_time"].mean().reset_index()
        fig2, ax2 = plt.subplots()
        sns.barplot(data=mat_time, x="material", y="study_time", ax=ax2)
        ax2.set_title("教材と平均学習時間の関係")
        plt.xticks(rotation=45)
        st.pyplot(fig2)

else:
    st.warning("まだ記録が存在しません。まずは記録を入力してください。")
