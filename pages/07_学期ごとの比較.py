import streamlit as st
import pandas as pd
import os
import matplotlib
import matplotlib.pyplot as plt
matplotlib.rcParams['font.family'] = 'MS Gothic'

st.set_page_config(page_title="学期ごとの比較", layout="wide")
st.title("📊 学期ごとの学習時間比較")

DATA_PATH = "data/logs.csv"

if os.path.exists(DATA_PATH):
    logs = pd.read_csv(DATA_PATH)

    if "date" in logs.columns:
        logs["date"] = pd.to_datetime(logs["date"], errors="coerce")

    # 必要な列の整形
    logs["study_time"] = pd.to_numeric(logs["study_time"], errors="coerce")
    logs["period"] = logs["period"].fillna("未設定")

    # 学期ごとの合計学習時間を算出
    period_summary = logs.groupby("period")["study_time"].sum().reset_index()

    # グラフ描画
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(period_summary["period"], period_summary["study_time"], color='skyblue')
    ax.set_title("学期ごとの学習時間", fontsize=16)
    ax.set_xlabel("学期", fontsize=12)
    ax.set_ylabel("学習時間（時間）", fontsize=12)
    st.pyplot(fig)

else:
    st.warning("まだ記録が存在しません。まずは記録を入力してください。")
