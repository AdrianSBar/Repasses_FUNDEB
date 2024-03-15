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


# Dados
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

    # Aplicando filtro pelo tempo
    col1_sb, col2_sb = st.columns(2)

    with col1_sb:
        date = datetime.date.today()
        if date.month <= 2:
            date = datetime.date(datetime.date.today().year-1, 1, 1)
        else:
            date = datetime.date(datetime.date.today().year, 1, 1)

        initial_date = st.date_input(label='Data inicial',
                                     min_value=datetime.date(
                                         2007, 1, 1),
                                     max_value=datetime.date.today(),
                                     value=date,
                                     format='DD/MM/YYYY')
    with col2_sb:
        final_date = st.date_input(label='Data final',
                                   min_value=initial_date,
                                   max_value=datetime.date.today(),
                                   value=datetime.date.today(),
                                   format='DD/MM/YYYY')
    filter = (temp.index >= str(initial_date)) & (
        temp.index <= str(final_date))
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


# Separação em colunas
col1, col2 = st.columns(2)
with col1:
    # Plot gráfico dos repasses mensais estaduais
    if (initial_date.year < datetime.date.today().year) and (initial_date.month > 2):
        y = ['TOTAL LIQUIDO', 'mean']
    else:
        y = 'TOTAL LIQUIDO'

    fig = px.line(data_frame=df_month,
                  x=df_month.index,
                  y=y,
                  title='Total de repasses no período')
    fig.update_traces(hovertemplate='R$ %{y:,.2f}')
    fig.update_layout(hovermode='x unified')
    st.plotly_chart(fig, use_container_width=True)

    # Plot gráfico dos repasses por fonte
    output = temp.copy()
    output = output.groupby('CATEGORIA')['TOTAL LIQUIDO'].sum().reset_index(
        level=0).sort_values(by='TOTAL LIQUIDO', ascending=False)
    fig = px.bar(data_frame=output,
                 x='CATEGORIA',
                 y='TOTAL LIQUIDO',
                 color='CATEGORIA',
                 text='TOTAL LIQUIDO',
                 title='Total de repasses no período por fonte de recurso')
    fig.update_traces(hovertemplate='R$ %{y:,.2f}',
                      texttemplate='%{text:,.3s}',
                      textposition='outside')
    fig.update_yaxes(showticklabels=False)
    fig.update_layout(hovermode='x unified')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    if (initial_date.year >= datetime.date.today().year-1):
        output = df_month.copy()
        input = 'TOTAL ACUMULADO'
        title = 'Total de repasses acumulados no período'
    else:
        output = df_year.copy()
        input = 'TOTAL LIQUIDO'
        title = 'Total de repasses acumulados por ano no período'

    # Plot gráfico cumulativo mensal/anual
    fig = px.bar(data_frame=output,
                 x=output.index,
                 y=input,
                 text=input,
                 title=title)
    fig.update_traces(hovertemplate='R$ %{y:,.2f}',
                      texttemplate='%{text:,.3s}',
                      textposition='outside')
    fig.update_yaxes(showticklabels=False)
    fig.update_layout(hovermode='x unified')
    st.plotly_chart(fig, use_container_width=True)

    # Plot gráfico dos repasses por estado
    output = temp.copy()
    output = output.groupby('UF')['TOTAL LIQUIDO'].sum().reset_index(
        level=0).sort_values(by='TOTAL LIQUIDO', ascending=False)
    fig = px.bar(data_frame=output,
                 x='UF',
                 y='TOTAL LIQUIDO',
                 color='UF',
                 text='TOTAL LIQUIDO',
                 title='Total de repasses por estado')
    fig.update_traces(hovertemplate='R$ %{y:,.2f}',
                      texttemplate='%{text:,.3s}',
                      textposition='outside')
    fig.update_yaxes(showticklabels=False)
    fig.update_layout(hovermode='x unified')
    st.plotly_chart(fig, use_container_width=True)
