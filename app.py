import streamlit as st

st.set_page_config(page_title="英語学習アプリ", layout="centered")

st.title("🎓 英語の自己調整学習アプリ")
st.markdown("ゼミ生の皆さん、ようこそ！このアプリでは、あなたの英語学習を記録・分析し、学習習慣をサポートします。")

st.markdown("---")

# 📱 モバイル対応ナビゲーション
st.subheader("🔗 ナビゲーションメニュー")

page = st.selectbox("📂 ページを選んで移動できます", [
    "📘 学習ビジョンの設定",
    "📝 学習記録の入力",
    "📋 記録一覧",
    "📈 学習時間の推移",
    "📊 学期ごとの比較",
    "📚 学習傾向の可視化",
    "🔔 リマインドメッセージ"
])

# ✅ ファイルパスで分岐（これがCloudで動く正しい方法！）
if page == "📘 学習ビジョンの設定":
    st.switch_page("pages/01_学習ビジョンの設定.py")
elif page == "📝 学習記録の入力":
    st.switch_page("pages/02_学習記録の入力.py")
elif page == "📋 記録一覧":
    st.switch_page("pages/03_記録一覧.py")
elif page == "📈 学習時間の推移":
    st.switch_page("pages/05_進捗グラフ.py")
elif page == "📊 学期ごとの比較":
    st.switch_page("pages/07_学期ごとの学習時間比較.py")
elif page == "📚 学習傾向の可視化":
    st.switch_page("pages/06_学習傾向の可視化.py")
elif page == "🔔 リマインドメッセージ":
    st.switch_page("pages/08_リマインドメッセージ.py")
