import streamlit as st
import datetime
from src.data_cleaning import *
from src.streamlit_utils import *
from src.update_data import *


# Configurações iniciais da página
st.set_page_config(page_title='Repasses FUNDEB',
                   page_icon='chart_with_upwards_trend',
                   layout='wide')


# Header
corrent_year = datetime.datetime.today().year
st.write('# Duvidas e sugestões')
st.write('## 1. Informações')
st.write(
    f'''Nesse app você pode encontrar informações relativas aos repasses financeiros destinados ao FUNDEB ao longo do tempo e por região. As informações foram extraídas do site [gov.com](https://www.tesourotransparente.gov.br/publicacoes/transferencias-ao-fundo-de-manutencao-e-desenvolvimento-da-educacao-basica-fundeb/2023/114?ano_selecionado=2023) e processadas para as devidas análises. Sinta-se a vontade para utilizar a base de dados processados por download!''')


# Dados
df = load_data(path='./data/processed/summarized_data_1.parquet')
file = convert_df(df=df)
st.download_button(
    label='Download da base de dados',
    data=file,
    file_name='dados.csv',
    mime='text/csv'
)


st.write('## 2. Duvidas e sugestões')
# Dúvidas e sugestões
st.write('Caso haja alguma outra duvida ou sugestão, por favor, deixe seu recado abaixo:')

mail = st.text_input(
    label='E-mail')
text = st.text_area(label='Duvida ou sugestão')

button = st.button(label='Enviar')
if button:
    st.success('Mensagem enviada!', icon="✅")
