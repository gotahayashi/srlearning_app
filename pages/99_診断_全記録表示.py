import streamlit as st
import pandas as pd

st.title("📋 全記録の診断ページ（フィルターなし）")

try:
    df = pd.read_csv("data/logs.csv", encoding="utf-8-sig")
    st.success("✅ logs.csv を正常に読み込みました。")

    st.subheader("全データ一覧")
    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 CSVとしてダウンロード",
        data=csv,
        file_name="全記録_確認用.csv",
        mime="text/csv"
    )

except FileNotFoundError:
    st.error("❌ logs.csv が見つかりません。正しい場所に置いてください。")
except Exception as e:
    st.error(f"❌ 読み込み中にエラーが発生しました: {e}")
