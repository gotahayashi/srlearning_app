import streamlit as st

st.set_page_config(page_title="英語学習アプリ", layout="centered")

st.title("🎓 英語の自己調整学習アプリ")
st.markdown("ゼミ生の皆さん、ようこそ！このアプリでは、あなたの英語学習を記録・分析し、学習習慣をサポートします。")

st.markdown("---")

# 📱 ナビゲーション
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

# ✅ ページタイトルで正確に分岐（Cloudで確実に動く）
if page == "📘 学習ビジョンの設定":
    st.switch_page("📘 学習ビジョンの設定")
elif page == "📝 学習記録の入力":
    st.switch_page("📝 学習記録の入力")
elif page == "📋 記録一覧":
    st.switch_page("📋 記録一覧")
elif page == "📈 学習時間の推移":
    st.switch_page("📈 学習時間の推移")
elif page == "📊 学期ごとの比較":
    st.switch_page("📊 学期ごとの比較")
elif page == "📚 学習傾向の可視化":
    st.switch_page("📚 学習傾向の可視化")
elif page == "🔔 リマインドメッセージ":
    st.switch_page("🔔 リマインドメッセージ")
