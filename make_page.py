import os

folder_path = "pages"
file_name = "04_記録一覧.py"
file_path = os.path.join(folder_path, file_name)

page_code = '''
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
'''

os.makedirs(folder_path, exist_ok=True)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(page_code)

print(f"{file_path} を作成しました。")
