import pandas as pd
import numpy as np
import streamlit as st


# arquivo
@st.cache_data
def load_data(path):
    df = pd.read_parquet(path=path)
    df.index = df['COMPETÊNCIA']  # type: ignore
    df.drop(labels='COMPETÊNCIA', axis='columns', inplace=True)
    return df


# Conversão dos dados para arquivo de download
@st.cache_data
def convert_df(df):
    return df.to_csv().encode('utf8')


# Dados agrupados mensalmente
@st.cache_data
def load_data_month(df):
    df_month = df.resample('MS').sum(numeric_only=True)
    df_month.loc[df_month['TOTAL LIQUIDO'] == 0, 'TOTAL LIQUIDO'] = np.nan
    df_month['TOTAL ACUMULADO'] = df_month['TOTAL LIQUIDO'].cumsum()
    df_month['dif'] = df_month['TOTAL LIQUIDO'].diff(1)
    return df_month


# Dados agrupados anualmente
@st.cache_data
def load_data_year(df):
    df_year = df.resample('Y').sum(numeric_only=True)
    df_year.loc[df_year['TOTAL LIQUIDO'] == 0, 'TOTAL LIQUIDO'] = np.nan
    return df_year
