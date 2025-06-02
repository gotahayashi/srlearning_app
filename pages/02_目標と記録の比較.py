import streamlit as st
import pandas as pd
from datetime import datetime

st.title("🎯 目標と記録の比較")

# データ読み込み
try:
    goals = pd.read_csv("data/goals.csv")
    logs = pd.read_csv("data/logs.csv")
except FileNotFoundError:
    st.warning("データファイルが見つかりません。記録または目標を先に入力してください。")
    st.stop()

# 日付変換（logsのみ）
logs["date"] = pd.to_datetime(logs["date"], format="ISO8601", errors="coerce")

# 名前の選択肢（NaNを除く）
names = sorted(logs["name"].dropna().unique())

if not names:
    st.info("まだ記録が入力されていないようです。先に記録ページで学習を記録してください。")
    st.stop()

selected_name = st.selectbox("確認する学生を選んでください", names)

# 今週の開始日（月曜日）
today = datetime.today()
start_of_week = today - pd.Timedelta(days=today.weekday())

# 選択された学生の今週の記録を抽出
student_logs = logs[(logs["name"] == selected_name) & (logs["date"] >= start_of_week)]
student_logs["study_time"] = pd.to_numeric(student_logs["study_time"], errors="coerce")
total_hours = student_logs["study_time"].sum()

# 目標取得
student_goal = goals[goals["name"] == selected_name]
if student_goal.empty:
    st.warning(f"{selected_name} の目標がまだ登録されていません。")
else:
    short_term_goal = student_goal.iloc[-1]["short_term_goal"]
    st.subheader("📌 今週の目標")
    st.write(short_term_goal)

st.subheader("📊 今週の学習時間")
st.write(f"合計: **{total_hours} 時間**")

# 目標との差の可視化（仮に4時間を基準）
RECOMMENDED_HOURS = 4.0
difference = total_hours - RECOMMENDED_HOURS

if difference >= 0:
    st.success(f"よくがんばりました！目標を {difference:.1f} 時間 上回っています。")
else:
    st.error(f"あと {-difference:.1f} 時間 がんばりましょう！")

# 今週の記録表示（デバッグや確認用）
with st.expander("📄 今週の記録詳細を確認する"):
    st.dataframe(student_logs)
