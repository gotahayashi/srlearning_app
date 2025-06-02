import streamlit as st
import pandas as pd

st.title("🔍 学習フィードバック")

try:
    logs = pd.read_csv("data/logs.csv")
except FileNotFoundError:
    st.warning("まだ学習記録が保存されていません。")
    st.stop()

# 名前選択
names = sorted(logs["name"].dropna().unique())
selected_name = st.selectbox("学生を選んでください", names)

# 選択された学生のデータ取得
student_logs = logs[logs["name"] == selected_name]

# study_time と focus を数値に変換（安全策）
student_logs["study_time"] = pd.to_numeric(student_logs["study_time"], errors="coerce")
student_logs["focus"] = pd.to_numeric(student_logs["focus"], errors="coerce")

# 平均値などを計算
average_time = student_logs["study_time"].mean()
average_focus = student_logs["focus"].mean()

st.write(f"📊 {selected_name} さんの学習フィードバック")

if pd.isna(average_time) or pd.isna(average_focus):
    st.info("学習時間または集中度のデータが不足しています。")
else:
    st.write(f"- 平均学習時間: **{average_time:.2f} 時間**")
    st.write(f"- 平均集中度: **{average_focus:.2f} / 5**")

    # フィードバック表示
    if average_time >= 4 and average_focus >= 4:
        st.success("とても良い学習習慣ができています！この調子で続けましょう！")
    elif average_time >= 2:
        st.info("学習時間は確保できています。集中度を少し意識してみましょう。")
    else:
        st.warning("学習時間が少ないようです。毎週4時間を目指しましょう！")
