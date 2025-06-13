
import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="記録一覧", layout="wide")
st.title("📖 学習記録一覧")

DATA_PATH = "data/logs.csv"

if os.path.exists(DATA_PATH):
    logs = pd.read_csv(DATA_PATH)

    if "date" in logs.columns:
        logs["date"] = pd.to_datetime(logs["date"], errors="coerce")

    names = logs["name"].dropna().unique()
    selected_name = st.selectbox("学生を選択", ["すべて"] + list(names))

    if selected_name != "すべて":
        logs = logs[logs["name"] == selected_name]

    st.dataframe(logs)

else:
    st.warning("まだ記録が存在しません。まずは記録を入力してください。")
