import pandas as pd
import streamlit as st

st.set_page_config(
    page_title='蔡大胖数据分析看板'
)

### 获取数据
df_raw = pd.read_csv('df_irv_table.csv')
st.dataframe(df_raw.head())

### sidebar
