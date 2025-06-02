import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.title("🗣️ フィードバック記録")

# ファイルパス
FEEDBACK_PATH = "data/feedback.csv"

# nameリスト取得（logs.csv から）
try:
    logs = pd.read_csv("data/logs.csv")
    names = sorted(logs["name"].dropna().unique())
except FileNotFoundError:
    names = []

if not names:
    st.warning("まだ学習記録がありません。先に記録ページで名前を登録してください。")
    st.stop()

selected_name = st.selectbox("フィードバックを送る学生を選んでください", names)

with st.form("feedback_form"):
    comment = st.text_area("コメント（アドバイス、励ましなど）")
    submitted = st.form_submit_button("保存")

    if submitted:
        new_entry = pd.DataFrame([{
            "name": selected_name,
            "date": datetime.today().strftime("%Y-%m-%d"),
            "comment": comment
        }])
        if os.path.exists(FEEDBACK_PATH):
            feedback_df = pd.read_csv(FEEDBACK_PATH)
            feedback_df = pd.concat([feedback_df, new_entry], ignore_index=True)
        else:
            feedback_df = new_entry

        feedback_df.to_csv(FEEDBACK_PATH, index=False)
        st.success("フィードバックを保存しました。")

# 既存フィードバックの表示
if os.path.exists(FEEDBACK_PATH):
    feedback_data = pd.read_csv(FEEDBACK_PATH)
    student_feedback = feedback_data[feedback_data["name"] == selected_name]

    if not student_feedback.empty:
        st.subheader("📋 過去のフィードバック一覧")
        st.dataframe(student_feedback.sort_values("date", ascending=False))
    else:
        st.info("この学生への過去のフィードバックはまだありません。")
