import streamlit as st

st.title("数据安全管理")


from data_stack.governance.lineage import data_lineage, job_lineage

tab_data_lineage, tab_job_lineage = st.tabs(["数据血缘", "作业血缘"])

dl_graph = data_lineage.to_graph()
tab_data_lineage.graphviz_chart(dl_graph)

jl_graph = job_lineage.to_graph()
tab_job_lineage.graphviz_chart(jl_graph)
