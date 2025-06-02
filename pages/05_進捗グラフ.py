import streamlit as st
import pandas as pd
import os
import matplotlib
import matplotlib.pyplot as plt
matplotlib.rcParams['font.family'] = 'MS Gothic'

st.set_page_config(page_title="学習時間の推移", layout="wide")
st.title("📈 学習時間の推移")

DATA_PATH = "data/logs.csv"

if os.path.exists(DATA_PATH):
    logs = pd.read_csv(DATA_PATH)

    if "date" in logs.columns:
        logs["date"] = pd.to_datetime(logs["date"], errors="coerce")

    names = logs["name"].dropna().unique()
    selected_name = st.selectbox("学生を選んでください", names)

    student_logs = logs[logs["name"] == selected_name].copy()
    student_logs["study_time"] = pd.to_numeric(student_logs["study_time"], errors="coerce")
    student_logs = student_logs.dropna(subset=["date"])

    student_logs["week"] = student_logs["date"].dt.to_period("W").astype(str)
    weekly_summary = student_logs.groupby("week")["study_time"].sum().reset_index()
    weekly_summary["week_str"] = weekly_summary["week"]

    # 色分け
    colors = []
    icons = []
    for val in weekly_summary["study_time"]:
        if val >= 3:
            colors.append("green")
            icons.append("✅")
        elif val >= 1:
            colors.append("orange")
            icons.append("🟠")
        else:
            colors.append("red")
            icons.append("⚠️")

    # グラフ
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(weekly_summary["week_str"], weekly_summary["study_time"], color=colors)
    ax.set_title(f"{selected_name}さんの週ごとの学習時間", fontsize=16)
    ax.set_xlabel("週の開始日", fontsize=12)
    ax.set_ylabel("学習時間（時間）", fontsize=12)
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # カード風のアイコン付きメッセージ
    for week, hour, icon in zip(weekly_summary["week_str"], weekly_summary["study_time"], icons):
        st.markdown(
            f"""
            <div style="background-color:#f9f9f9; padding:10px; margin:5px 0; border-left:5px solid #4CAF50;">
                <strong>{icon} {week}</strong>：{hour} 時間
            </div>
            """,
            unsafe_allow_html=True
        )

    # 💡 アドバイスメッセージの追加（ここがDay23の追加ポイント！）
    total_hours = weekly_summary["study_time"].sum()
    st.subheader("💡 学習アドバイス")
    if total_hours >= 3:
        st.success("素晴らしい取り組みですね！この調子で続けましょう💪")
    elif total_hours >= 1:
        st.info("もう少し学習時間を確保してみましょう⌛")
    else:
        st.warning("毎日少しずつでも学習を習慣にしましょう📘")

else:
    st.warning("まだ記録が存在しません。まずは記録を入力してください。")
