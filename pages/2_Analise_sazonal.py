import streamlit as st
import datetime
import pandas as pd
import numpy as np
import plotly.express as px


# Configurações da página
st.set_page_config(page_title='App repasses FUNDEB',
                   page_icon='chart_with_upwards_trend',
                   layout='wide')


# Carregamento dos dados
@st.cache_data
def load_data(path):
    df = pd.read_parquet(path=path)
    df.index = df['COMPETÊNCIA']
    df.drop(labels='COMPETÊNCIA', axis='columns', inplace=True)
    return df


# Conversão dos dados para arquivo de download
@st.cache_data
def convert_df(df):
    return df.to_csv().encode('utf8')


# Dados Brutos
df = load_data(path='./DATASETS/summarized_data.parquet')

with st.sidebar:
    st.markdown("# Esfera Estadual")
    st.markdown("## Filtros")

    # Filtro das esferas
    state_level_filter = st.selectbox(label='Esfera',
                                      options=df.ESFERA.unique())
    filter = df.ESFERA == state_level_filter
    df = df[filter]

    # Filtro estadual
    states_filter = st.multiselect(label='Estados',
                                   options=sorted(df.UF.unique()),
                                   placeholder='Selecione algum Estado')
    if states_filter:
        filter = df.UF.isin(states_filter)
        df = df[filter]

    # Filtro de repasse
    transfer_filter = st.multiselect(label='Categoria',
                                     options=sorted(
                                         df.CATEGORIA.unique()),
                                     placeholder='Selecione algum Recurso')
    if transfer_filter:
        filter = df.CATEGORIA.isin(transfer_filter)
        df = df[filter]

    # Botão de download dos arquivo principal
    file = convert_df(df=df)
    st.download_button(
        label='Download dos dados',
        data=file,
        file_name='dados.csv',
        mime='text/csv'
    )


# Dados agrupados mensalmente
df_month = df.resample('MS').sum(numeric_only=True)
df_month.loc[df_month['TOTAL LIQUIDO'] == 0, 'TOTAL LIQUIDO'] = np.nan
df_month['TOTAL ACUMULADO'] = df_month['TOTAL LIQUIDO'].cumsum()
df_month['dif'] = df_month['TOTAL LIQUIDO'].diff(1)

# Dados agrupados anualmente
df_year = df.resample('Y').sum(numeric_only=True)
df_year.loc[df_year['TOTAL LIQUIDO'] == 0, 'TOTAL LIQUIDO'] = np.nan

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
