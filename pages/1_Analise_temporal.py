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


# Dados
df = load_data(path='./DATASETS/summarized_data.parquet')

with st.sidebar:
    st.markdown("# Filtros")

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
    filter = (df.index >= str(initial_date)) & (
        df.index <= str(final_date))
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
df_month['mean'] = df_month['TOTAL LIQUIDO'].rolling(6).mean()

# Dados agrupados anualmente
df_year = df.resample('Y').sum(numeric_only=True)
df_year.loc[df_year['TOTAL LIQUIDO'] == 0, 'TOTAL LIQUIDO'] = np.nan

# TABS
tab1, tab2 = st.tabs(
    tabs=['**Análise temporal**', '**Chat-gpt**'])
with tab1:
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
        output = df.copy()
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
        output = df.copy()
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


with tab2:
    "Em produção..."
