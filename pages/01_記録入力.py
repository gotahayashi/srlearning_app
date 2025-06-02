import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="記録入力", layout="centered")
st.title("📝 今日の学習記録を入力")

DATA_PATH = "data/logs.csv"

with st.form("log_form", clear_on_submit=True):
    st.markdown("### 🔽 以下のフォームに入力してください")

    # 🧾 2列レイアウト
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("名前", placeholder="例：Gota Hayashi", help="自分の名前を入力してください")
        grade = st.selectbox("学年", ["1年", "2年", "3年", "4年"])
        date = st.date_input("学習日", value=datetime.today())
        study_time = st.number_input("学習時間（時間）", min_value=0.0, step=0.1, help="例：1時間30分 → 1.5")
    with col2:
        textbook = st.text_input("使用教材", placeholder="例：DUO, 英文法", help="使用した教材を入力")
        task = st.text_input("学習内容", placeholder="例：Unit3復習, 英作文など", help="具体的な学習内容を記入")
        environment = st.radio("学習場所", ["自宅", "カフェ", "図書館", "その他"])
        focus = st.slider("集中度（1＝低い〜5＝高い）", 1, 5)
        period = st.selectbox("期間", ["学期1", "夏休み", "学期2", "春休み"])

    submitted = st.form_submit_button("保存する")

    if submitted:
        # ✅ 必須チェック
        if not name or not textbook or not task:
            st.error("⚠️ 名前・教材・学習内容はすべて入力してください。")
        else:
            if study_time > 10:
                st.warning("⚠️ 長時間の入力です。内容をご確認ください。")

            new_data = pd.DataFrame([{
                "name": name,
                "grade": grade,
                "date": date,
                "study_time": study_time,
                "textbook": textbook,
                "task": task,
                "environment": environment,
                "focus": focus,
                "period": period
            }])

            if os.path.exists(DATA_PATH):
                old_data = pd.read_csv(DATA_PATH)
                all_data = pd.concat([old_data, new_data], ignore_index=True)
            else:
                all_data = new_data

            all_data.to_csv(DATA_PATH, index=False)
            st.success("✅ 記録が保存されました！")

            # 入力内容を表示
            st.markdown("### 🕒 保存された記録")
            st.dataframe(new_data)
