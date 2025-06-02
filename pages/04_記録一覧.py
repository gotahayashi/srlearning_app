import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="記録一覧", layout="wide")
st.title("📚 学習記録一覧")

DATA_PATH = "data/logs.csv"

if os.path.exists(DATA_PATH):
    logs = pd.read_csv(DATA_PATH)

    # 日付を日付型に変換
    if "date" in logs.columns:
        logs["date"] = pd.to_datetime(logs["date"], errors="coerce")

    # 学生名で絞り込み
    names = logs["name"].dropna().unique()
    selected_name = st.selectbox("学生を選択", ["すべて"] + list(names))
    if selected_name != "すべて":
        logs = logs[logs["name"] == selected_name]

    # 学期で絞り込み
    if "period" in logs.columns:
        selected_period = st.multiselect("学期で絞り込み", options=logs["period"].dropna().unique())
        if selected_period:
            logs = logs[logs["period"].isin(selected_period)]

    # 学習環境で絞り込み
    if "environment" in logs.columns:
        selected_env = st.multiselect("学習環境で絞り込み", options=logs["environment"].dropna().unique())
        if selected_env:
            logs = logs[logs["environment"].isin(selected_env)]

    # 教材で絞り込み
    if "textbook" in logs.columns:
        selected_material = st.multiselect("教材で絞り込み", options=logs["textbook"].dropna().unique())
        if selected_material:
            logs = logs[logs["textbook"].isin(selected_material)]

    # 表示
    st.dataframe(logs)

    # CSVダウンロード
    csv = logs.to_csv(index=False, encoding="utf-8-sig")
    st.download_button("📥 CSVとしてダウンロード", data=csv, file_name="filtered_logs.csv", mime="text/csv")
else:
    st.warning("まだ記録が存在しません。")
