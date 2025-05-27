import streamlit as st

from data_stack.governance.quality import DataQualityRule

st.title("数据质量管理")


st.markdown(f"### 质量规则")
rules = DataQualityRule.values()
for rule in rules:
    st.markdown(f"- {rule}")

