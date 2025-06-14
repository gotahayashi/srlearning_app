import streamlit as st

st.set_page_config(page_title="SR Learning App", page_icon="📘", layout="centered")

st.title("📘 Self-Regulated Learning App")
st.subheader("ようこそ！")

st.markdown("""
このアプリは、大学生が自己調整学習（SRL）を実践するために開発されました。  
以下の各ページを活用して、あなたの英語学習をより効果的に管理しましょう。

---

### 📋 利用できるページ（左のサイドバーから選択）：

- ✅ **ビジョン設定**
- 📝 **学習ログの記録**
- 📊 **ログの一覧表示**

---

### 👉 左のメニューからページを選んでください。
""")

st.info("※このアプリは東京経済大学のゼミ活動の一環として使用されています。")
st.markdown("---")
st.caption("© 2025 Gota Hayashi Lab")
