import pandas as pd
import streamlit as st

### 获取数据
df_raw = pd.read_csv('df_irv_table.csv')

st.dataframe(df_raw.head())