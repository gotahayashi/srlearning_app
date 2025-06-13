# -*- coding: utf-8 -*-
import streamlit as st

st.set_page_config(page_title='ダッシュボード表示', layout='wide')

st.title('📊 Looker Studio ダッシュボード')

st.markdown('以下は学習記録の可視化ダッシュボードです。')

st.components.v1.iframe(
    src='https://lookerstudio.google.com/embed/reporting/979a66db-39cd-471b-986e-3e61d519628d/page/wVPNF',
    width=1200,
    height=800,
    scrolling=True
)
