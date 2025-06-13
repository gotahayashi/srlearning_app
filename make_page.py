import streamlit as st
import pandas as pd
import os

def show_input_page(worksheet):
    st.title("📝 学習ログの記録")

    name = st.text_input("名前")
    study_time = st.number_input("学習時間(分)", min_value=0)
    memo = st.text_area("メモ")

    if st.button("記録を保存"):
        import datetime
        new_row = {
            "timestamp": datetime.datetime.now().isoformat(),
            "name": name,
            "study_time": study_time,
            "memo": memo
        }
        worksheet.append_row(list(new_row.values()))
        st.success("記録を保存しました！")
