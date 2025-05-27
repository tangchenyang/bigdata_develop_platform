import os

import streamlit as st


def run():
    st.set_page_config(layout="wide", page_title="数据智能治理")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    ng = st.navigation([
        st.Page(f'{current_dir}/pages/index.py', title="首页"),
        st.Page(f'{current_dir}/pages/data_asset_management_page.py',title="数据资产管理"),
        st.Page(f'{current_dir}/pages/data_quality_management_page.py', title="数据质量管理"),
        st.Page(f'{current_dir}/pages/data_security_management_page.py', title="数据安全管理"),
        st.Page(f'{current_dir}/pages/metadata_management_page.py', title="元数据管理"),
    ])
    ng.run()


"""
data_asset_management_page.py
data_quality_management_page.py
data_security_management_page.py
index.py
metadata_management_page.py
"""
