import os

folder_path = "pages"
file_name = "03_ビジョン設定.py"
file_path = os.path.join(folder_path, file_name)

page_code = '''
import streamlit as st
import pandas as pd
from datetime import date
import os

st.set_page_config(page_title="ビジョン設定", layout="centered")
st.title("🌟 ビジョン設定フォーム")

VISION_CSV = "data/visions.csv"
os.makedirs("data", exist_ok=True)

with st.form("vision_form"):
    name = st.text_input("名前")
    grade = st.selectbox("学年", ["1年", "2年", "3年", "4年"])
    title = st.text_input("目標タイトル（例：TOEIC600点達成）")
    content = st.text_area("目標内容（例：毎週4時間、英語の動画を視聴する）")
    deadline = st.date_input("達成期限", value=date.today())

    submitted = st.form_submit_button("保存する")

    if submitted:
        new_data = pd.DataFrame([{
            "name": name,
            "grade": grade,
            "title": title,
            "content": content,
            "deadline": deadline
        }])

        if os.path.exists(VISION_CSV):
            existing = pd.read_csv(VISION_CSV)
            updated = pd.concat([existing, new_data], ignore_index=True)
        else:
            updated = new_data

        updated.to_csv(VISION_CSV, index=False)
        st.success("ビジョンを保存しました！")
'''

os.makedirs(folder_path, exist_ok=True)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(page_code)

print(f"{file_path} を作成しました。")
