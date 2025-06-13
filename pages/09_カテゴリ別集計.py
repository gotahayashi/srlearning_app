# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

st.set_page_config(page_title="カテゴリ別集計", layout="wide")
st.title("📊 カテゴリ別の学習記録")

# 🎌 日本語フォント設定（ipaexg.ttf を fonts フォルダに入れておく）
FONT_PATH = os.path.join("fonts", "ipaexg.ttf")
if os.path.exists(FONT_PATH):
    jp_font = fm.FontProperties(fname=FONT_PATH)
else:
    jp_font = None

DATA_PATH = "data/logs.csv"

if os.path.exists(DATA_PATH):
    df = pd.read_csv(DATA_PATH)

    if "category" in df.columns:
        st.markdown("### カテゴリごとの件数（棒グラフ）")

        category_counts = df["category"].value_counts()

        fig_bar, ax = plt.subplots()
        category_counts.plot(kind="bar", ax=ax)
        ax.set_ylabel("件数", fontproperties=jp_font)
        ax.set_xlabel("カテゴリ", fontproperties=jp_font)
        ax.set_title("カテゴリ別件数", fontproperties=jp_font)
        plt.xticks(rotation=45, fontproperties=jp_font)
        plt.yticks(fontproperties=jp_font)
        st.pyplot(fig_bar)

        st.markdown("### カテゴリごとの割合（円グラフ）")

        fig_pie, ax2 = plt.subplots()
        category_counts.plot(kind="pie", autopct="%1.1f%%", ax=ax2)
        ax2.set_ylabel("")
        ax2.set_title("カテゴリ比率", fontproperties=jp_font)
        plt.setp(ax2.texts, fontproperties=jp_font)
        st.pyplot(fig_pie)

    else:
        st.warning("カテゴリ列が見つかりませんでした。データに 'category' 列が必要です。")
else:
    st.warning
