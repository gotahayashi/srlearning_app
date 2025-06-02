import streamlit as st

st.set_page_config(page_title="英語学習アプリ", layout="centered")

st.title("🎓 英語の自己調整学習アプリ")
st.markdown("ゼミ生の皆さん、ようこそ！このアプリでは、あなたの英語学習を記録・分析し、学習習慣をサポートします。")

st.markdown("---")

st.subheader("🔗 ナビゲーションメニュー")

page = st.selectbox("📂 ページを選んで移動できます", [
    "🏠 ホーム",
    "📝 記録入力",
    "🎯 目標と記録の比較",
    "📘 ビジョン設定",
    "🗒️ フィードバック記録",
    "📚 学習フィードバック",
    "📋 記録一覧",
    "📈 進捗グラフ",
    "📊 学期ごとの比較",
    "📚 学習傾向の可視化"
])

# ファイル名に対応するページ遷移（Cloudで必須）
if page == "🏠 ホーム":
    st.switch_page("pages/00_ホーム.py")
elif page == "📝 記録入力":
    st.switch_page("pages/01_記録入力.py")
elif page == "🎯 目標と記録の比較":
    st.switch_page("pages/02_目標と記録の比較.py")
elif page == "📘 ビジョン設定":
    st.switch_page("pages/03_ビジョン設定.py")
elif page == "🗒️ フィードバック記録":
    st.switch_page("pages/03_フィードバック記録.py")
elif page == "📚 学習フィードバック":
    st.switch_page("pages/03_学習フィードバック.py")
elif page == "📋 記録一覧":
    st.switch_page("pages/04_記録一覧.py")
elif page == "📈 進捗グラフ":
    st.switch_page("pages/05_進捗グラフ.py")
elif page == "📊 学期ごとの比較":
    st.switch_page("pages/07_学期ごとの比較.py")
elif page == "📚 学習傾向の可視化":
    st.switch_page("pages/06_学習傾向の可視化.py")
