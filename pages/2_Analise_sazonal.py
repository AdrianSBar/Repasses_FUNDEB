import streamlit as st
import datetime
import pandas as pd
import numpy as np
import plotly.express as px
from PROJECT_LIBRARY.Project_functions import *


# Configurações da página
st.set_page_config(page_title='App repasses FUNDEB',
                   page_icon='chart_with_upwards_trend',
                   layout='wide')


# Dados Brutos
df = load_data(path='./DATASETS/summarized_data.parquet')
temp = df.copy()

with st.sidebar:
    st.markdown("# Filtros")

    # Filtro das esferas
    state_level_filter = st.selectbox(label='Esfera',
                                      options=temp.ESFERA.unique())
    filter = temp.ESFERA == state_level_filter
    temp = temp[filter]

    # Filtro estadual
    states_filter = st.multiselect(label='Estados',
                                   options=sorted(temp.UF.unique()),
                                   placeholder='Selecione algum Estado')
    if states_filter:
        filter = temp.UF.isin(states_filter)
        temp = temp[filter]

    # Filtro de repasse
    transfer_filter = st.multiselect(label='Categoria',
                                     options=sorted(
                                         temp.CATEGORIA.unique()),
                                     placeholder='Selecione algum Recurso')
    if transfer_filter:
        filter = temp.CATEGORIA.isin(transfer_filter)
        temp = temp[filter]

    # Botão de download dos arquivo principal
    file = convert_df(df=temp)
    st.download_button(
        label='Download dos dados',
        data=file,
        file_name='dados.csv',
        mime='text/csv'
    )


# Dados agrupados mensalmente
df_month = load_data_month(temp)

# Dados agrupados anualmente
df_year = load_data_year(temp)

# Gráfico de oscilações mensais
fig = px.bar(data_frame=df_month,
             x=df_month.index,
             y='dif',
             text='dif',
             title='Análise de variação histórica')
fig.update_yaxes(showticklabels=False)
fig.update_traces(texttemplate='%{text:.3s}',
                  textposition='outside',
                  hovertemplate='R$%{text:,.2f}')
fig.update_layout(hovermode='x unified')
st.plotly_chart(fig, use_container_width=True)

# Gráfico de oscilações mensais médias
df_month['media'] = df_month['TOTAL LIQUIDO'].rolling(window=7).mean()
df_month['saz'] = df_month['TOTAL LIQUIDO'].diff(1)
df_month = df_month['saz'].groupby(df_month.index.month).mean()

fig = px.bar(data_frame=df_month,
             x=df_month.index,
             y='saz',
             text='saz',
             title='Sazonalidade média mensal')
fig.update_yaxes(showticklabels=False)
fig.update_traces(texttemplate='%{text:.3s}',
                  textposition='outside',
                  hovertemplate='R$%{text:,.2f}')
fig.update_layout(hovermode='x unified')
st.plotly_chart(fig, use_container_width=True)
