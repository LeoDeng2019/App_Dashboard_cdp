import pandas as pd
import streamlit as st
import plotly_express as px

### 页面设置
st.set_page_config(
    page_title='CBW数据分析看板',
    layout='wide'
)

### 获取数据
@st.cache_data
def get_df():
    df_raw = pd.read_csv('data_cbw.csv')
    return df_raw
df_raw = get_df()

### 处理数据
dict_change = {'开放平台-扫码点餐': '开放平台', '开放平台-淳乐送': '开放平台'}
df_raw['businessname'] = df_raw['businessname'].apply(lambda x: x[:4])
dff = df_raw[df_raw['businessname'].isin(['到店销售', '开放平台'])]

### sidebar
st.sidebar.markdown('---')
business = st.sidebar.radio(
    '请选择渠道：',
    (dff['businessname'].unique()[0], dff['businessname'].unique()[1])
)
st.sidebar.markdown('---')
month_s = st.sidebar.selectbox(
    '请选择月份：',
    (dff['month'].unique())
)

### KPI
dff_select = dff.query("businessname==@business & month==@month_s")

# Row A
st.header(f'2021年{month_s}月 CBW销售数据看板')
st.markdown('---')
a1, a2, a3, a4 = st.columns(4)

a1.metric(
    '总销售额（万元）',
    round(dff_select['dealtotal'].sum()/10000,1),
    '3%'
)

a2.metric(
    '净利润（万元）',
    round(dff_select['dealtotal'].sum()/10000*0.15,1),
    '5%'
)

a3.metric(
    '客单量（万）',
    round(dff_select['billcount'].sum()/10000, 1),
    '1%'
)

a4.metric(
    '客单价（元）',
    round(dff_select['dealtotal'].sum()/dff_select['billcount'].sum(),1),
    '-1%'
)

# Row B
b1, b2 = st.columns(2)

dff_b1 = dff.groupby('month', as_index=False)['dealtotal'].sum()
fig_bar = px.bar(
    x = dff_b1['month'],
    y = dff_b1['dealtotal'],
    labels = {'month': '月份', 'dealtotal': '销售额'},
    title = '销售额趋势（月份）'
)
b1.plotly_chart(fig_bar, use_container_width=True)

dff_b2 = dff.groupby('businessname', as_index=False)['dealtotal'].sum()
fig_pie = px.pie(
    dff_b2,
    values='dealtotal',
    names='businessname',
    title='销售额占比',
    hole=0.5
)
b2.plotly_chart(fig_pie, use_container_width=True)

st.dataframe(dff_select.head())