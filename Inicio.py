import streamlit as st
import pandas as pd
import datetime


# Configurações da página
st.set_page_config(page_title='App repasses FUNDEB',
                   page_icon='🧊',
                   layout='wide')
# BARRA LATERAL
with st.sidebar:
    st.markdown('# Home')
    st.write('Seja bem vindo!')


# MENU PRINCIPAL
# arquivo
@st.cache_data
def load_data(path):
    df = pd.read_csv(path,
                     parse_dates=['COMPETÊNCIA'],
                     index_col='COMPETÊNCIA')
    return df


# Texto menu principal - informações sobre o app
corrent_year = datetime.datetime.today().year
st.write('# Bem vindo(a)!')
st.write(
    f'Nesse app você pode encontrar informações acerca dos repasses financeiros recebidos pelo FUNDEB por estado de 2007 à {corrent_year}! Tanto para as esferas estaduais, quanto para as municipais.')
st.write(
    'As informações foram extraídas do site [gov.com](https://www.tesourotransparente.gov.br/publicacoes/transferencias-ao-fundo-de-manutencao-e-desenvolvimento-da-educacao-basica-fundeb/2023/114?ano_selecionado=2023).')


@st.cache_data
def convert_df(df):
    return df.to_csv().encode('utf8')


# Visualização dos dados caso necessário
df = load_data(path='./data.csv')
checkbox_1 = st.checkbox(label='Visualizar dados')
if checkbox_1:
    with st.sidebar:
        st.write('# Filtros')
        # Ajuste dos dados para visualização
        # Aplicando filtro pelo tempo
        col1_sb, col2_sb = st.columns(2)
        with col1_sb:
            initial_date = st.date_input(label='Data inicial',
                                         min_value=datetime.date(
                                             2007, 1, 1),
                                         max_value=datetime.date.today(),
                                         value=datetime.date(
                                             datetime.date.today().year, 1, 1),
                                         format='DD/MM/YYYY')
        with col2_sb:
            final_date = st.date_input(label='Data final',
                                       min_value=datetime.date(
                                           datetime.date.today().year, 1, 1),
                                       max_value=datetime.date.today(),
                                       value=datetime.date.today(),
                                       format='DD/MM/YYYY')

        spheres_filter = st.multiselect(label='Esfera',
                                        options=sorted(df.ESFERA.unique()),
                                        placeholder='Selecione alguma Esfera')

        states_filter = st.multiselect(label='Estados',
                                       options=sorted(df.UF.unique()),
                                       placeholder='Selecione algum Estado')

        transfer_filter = st.multiselect(label='Categoria',
                                         options=sorted(df.CATEGORIA.unique()),
                                         placeholder='Selecione algum Recurso')

    # Aplicando filtros apenas para visualização
    temp = df.copy()
    if spheres_filter:
        temp = temp[temp.ESFERA.isin(spheres_filter)]
    if states_filter:
        temp = temp[temp.UF.isin(states_filter)]
    if transfer_filter:
        temp = temp[temp.CATEGORIA.isin(transfer_filter)]

    st.dataframe(temp, use_container_width=True)


# Botão de download dos arquivo principal
st.write('Caso necessite, segue o arquivo consolidado completo para download:')
file = convert_df(df=df)
st.download_button(
    label='Download',
    data=file,
    file_name='dados.csv',
    mime='text/csv'
)


# # Dúvidas e sugestões
# st.write('Caso haja alguma duvida ou sugestão:')
# mail = st.text_input(
#     label='E-mail')
# text = st.text_area(label='Duvida ou sugestão')

# button = st.button(label='Enviar')
# if button:
#     st.success('Mensagem enviada!', icon="✅")
