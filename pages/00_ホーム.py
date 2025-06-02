import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

st.set_page_config(page_title="ホーム", layout="wide")
st.title("🏠 ホーム - リマインド機能")

DATA_PATH = "data/logs.csv"

if os.path.exists(DATA_PATH):
    logs = pd.read_csv(DATA_PATH)
    if "date" in logs.columns:
        logs["date"] = pd.to_datetime(logs["date"], errors="coerce")
        recent_logs = logs.dropna(subset=["name", "date"])

        # 最終記録日を取得
        latest_by_student = recent_logs.groupby("name")["date"].max().reset_index()
        today = datetime.today()

        for _, row in latest_by_student.iterrows():
            name = row["name"]
            last_date = row["date"]
            days_diff = (today - last_date).days

            if days_diff > 7:
                st.warning(f"⚠️ {name} さんは {days_diff} 日間記録がありません。忘れず記録しましょう！")
            else:
                st.success(f"✅ {name} さんは {days_diff} 日前に記録しています。")

    else:
        st.info("記録に 'date' 列がありません。正しい形式で保存されているか確認してください。")
else:
    st.warning("まだ記録が存在しません。まずは記録を入力してください。")
