import streamlit as st

st.title("数据资产管理")

from data_stack.meta import job_meta, data_meta

st.markdown(f"### 数据目录")
for data_asset in data_meta.registered_data_assets.keys():
    st.markdown(f"- {data_asset}")
