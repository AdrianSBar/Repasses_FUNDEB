import os
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import re
import xlrd
import streamlit as st
import plotly.express as px
from PROJECT_LIBRARY.Data_extraction import *


# Função criada para extração dos nomes de todas as abas do arquivo excel que é emitidos por ano
def get_all_sheet_names_on_files(fold):
    # Lista ordenada de todos os nomes dos arquivos dentro da pasta dados
    file_names = sorted(os.listdir(path=fold))
    # Gerando uma lista com o nome de todas as abas únicas que existem em todos os arquivos
    all_sheet_names = []
    for file_name in file_names:
        # Listando o nome de todas as abas dentro de um arquivo constante dentro da pasta
        sheet_names = xlrd.open_workbook(
            filename=f'{fold}/{file_name}').sheet_names()
        for sheet_name in sheet_names:
            # Adicionando o nome da aba do arquivo dentro de lista casa ainda não esteja dentro
            if sheet_name not in all_sheet_names:
                all_sheet_names.append(sheet_name)
    # Retornando uma lista ordenada de todos os nomes dos arquivos dentro da pasta dados
    return all_sheet_names


# Função de tratamento dos dados do fundeb de até de 2019
def preprocessing_data_until_2019(io, sheet_name, skiprows, header):
    # leitura do arquivo
    df01 = pd.read_excel(io=io, sheet_name=sheet_name,
                         skiprows=skiprows, header=header)
    # Ajustes nos nomes das colunas
    df01.columns = [i.strip() for i in df01.columns]
    # Remoção da coluna total
    df01 = df01.drop(columns='TOTAL')
    # Remoção das linhas com valores nulos na coluna UF
    df01 = df01.dropna(axis='rows', subset='UF')
    df01 = df01.loc[df01.UF.str.len() == 2]
    # Substituição dos valores nulos por 0
    df01 = df01.fillna(0)
    # Reconfiguração dos dados para uma tabela onde constem apenas as variáveis UF, COMPETÊNCIA e o NOME DA ABA DO ARQUIVO
    df01 = pd.melt(
        frame=df01,
        id_vars=['UF'],
        value_vars=['JANEIRO', 'FEVEREIRO', 'MARÇO', 'ABRIL', 'MAIO', 'JUNHO',
                    'JULHO', 'AGOSTO', 'SETEMBRO', 'OUTUBRO', 'NOVEMBRO', 'DEZEMBRO'],
        var_name='COMPETÊNCIA',
        value_name=f'{sheet_name}')
    # Ajuste do valores mensais para paríodos de tempo de acordo com o mês e o ano do arquivo
    ano = re.findall(pattern=r'\d+', string=io)[0]
    map_months = {'JANEIRO': '1', 'FEVEREIRO': '2', 'MARÇO': '3', 'ABRIL': '4', 'MAIO': '5', 'JUNHO': '6',
                  'JULHO': '7', 'AGOSTO': '8', 'SETEMBRO': '9', 'OUTUBRO': '10', 'NOVEMBRO': '11', 'DEZEMBRO': '12'}
    df01['COMPETÊNCIA'] = pd.to_datetime(
        arg=df01['COMPETÊNCIA'].map(map_months)+f'/{ano}', format=f'%m/%Y')
    # Ordenamento dos dados para UF e COMPETÊNCIA
    df01 = df01.sort_values(by=['UF', 'COMPETÊNCIA']).reset_index(drop=True)
    return df01


# Função de tratamento dos dados de 2020 em diante
def preprocessing_data_from_2020_onwards(io, sheet_name, skiprows, header):
    # leitura do arquivo das tabelas principais
    df01 = pd.read_excel(io=io, sheet_name=sheet_name,
                         skiprows=skiprows, header=header, nrows=30)
    df02 = pd.read_excel(io=io, sheet_name=sheet_name,
                         skiprows=skiprows+39, header=header, nrows=30)
    # Ajustes nos nomes das colunas
    df01.columns = [i.strip() for i in df01.columns]
    df02.columns = [i.strip() for i in df02.columns]
    # Remoção da coluna total
    df01 = df01.drop(columns='TOTAL')
    df02 = df02.drop(columns='TOTAL')
    # Remoção das linhas com valores nulos na coluna UF
    df01 = df01.dropna(axis='rows', subset='UF')
    df02 = df02.dropna(axis='rows', subset='UF')
    # Substituição dos valores nulos por 0
    df01 = df01.fillna(0)
    df02 = df02.fillna(0)
    # Reconfiguração dos dados para uma tabela onde constem apenas as variáveis UF, COMPETÊNCIA e o NOME DA ABA DO ARQUIVO
    df01 = pd.melt(
        frame=df01,
        id_vars=['UF'],
        value_vars=['JANEIRO', 'FEVEREIRO', 'MARÇO', 'ABRIL', 'MAIO', 'JUNHO',
                    'JULHO', 'AGOSTO', 'SETEMBRO', 'OUTUBRO', 'NOVEMBRO', 'DEZEMBRO'],
        var_name='COMPETÊNCIA',
        value_name=f'{sheet_name}')
    df02 = pd.melt(
        frame=df02,
        id_vars=['UF'],
        value_vars=['JANEIRO', 'FEVEREIRO', 'MARÇO', 'ABRIL', 'MAIO', 'JUNHO',
                    'JULHO', 'AGOSTO', 'SETEMBRO', 'OUTUBRO', 'NOVEMBRO', 'DEZEMBRO'],
        var_name='COMPETÊNCIA',
        value_name='A_'+f'{sheet_name}')
    # Ajuste do valores mensais para paríodos de tempo de acordo com o mês e o ano do arquivo
    map_months = {'JANEIRO': '1', 'FEVEREIRO': '2', 'MARÇO': '3', 'ABRIL': '4', 'MAIO': '5', 'JUNHO': '6',
                  'JULHO': '7', 'AGOSTO': '8', 'SETEMBRO': '9', 'OUTUBRO': '10', 'NOVEMBRO': '11', 'DEZEMBRO': '12'}
    ano = re.findall(pattern=r'\d+', string=io)[0]
    df01['COMPETÊNCIA'] = pd.to_datetime(
        arg=df01['COMPETÊNCIA'].map(map_months)+f'/{ano}', format=f'%m/%Y')
    df02['COMPETÊNCIA'] = pd.to_datetime(
        arg=df02['COMPETÊNCIA'].map(map_months)+f'/{ano}', format=f'%m/%Y')
    # Ordenamento dos dados para UF e COMPETÊNCIA
    df01 = df01.sort_values(by=['UF', 'COMPETÊNCIA']).reset_index(drop=True)
    df02 = df02.sort_values(by=['UF', 'COMPETÊNCIA']).reset_index(drop=True)
    return df01, df02


# Função de automatização do tratamento de todos os dados dentro de uma pasta
def consolidation_data(fold):
    # Captando lista de todoas os nomes de abas dentro dos arquivos
    all_sheet_names = get_all_sheet_names_on_files(fold)
    # Lista de nome de abas que serão removidas
    remove_sheet_names = ['E_Tot1_U', 'E_Tot2_E', 'E_TOTAL',
                          'M_Tot1_U', 'M_Tot2_E', 'M_TOTAL', 'Resumo']
    # Gerando nova lista com o nome de todas as abas úteis
    useful_sheet_names = [
        iten for iten in all_sheet_names if iten not in remove_sheet_names]
    # Iniciando lista para armazenar os dataframes das planilhas de cada aba
    sheet_datas = []
    # Gerando dataframe onde serão agrupadas todas as abas de um arquivo
    sheet_datas_merged = pd.DataFrame({'UF': [], 'COMPETÊNCIA': []})
    # Iniciando lista para armazenar todas os dataframes agrupados de cada arquivo
    file_datas = []
    # Loop para percorrer todos os arquivos dentro da pasta selecionada
    file_names = sorted(os.listdir(path=fold))
    for file in file_names:
        # Loop para percorrer todas as abas úteis que constam dentro do arquivo
        for sheet_name in useful_sheet_names:
            # Trasnformação para cada arquivo com dados até 2019
            if int(re.findall(pattern=r'\d+', string=file)[0]) <= 2019:
                # Tentar ler o arquivo com as abas úteis, caso a aba não exista no arquivo, será analisada aba seguinte da lista de abas úteis
                try:
                    # Tentar ler o arquivo após 9 linhas, caso contrário, lerá após 7 linhas
                    try:
                        df01 = preprocessing_data_until_2019(
                            io=f'{fold}/{file}', sheet_name=sheet_name, skiprows=9, header=0)
                        sheet_datas.append(df01)
                    except:
                        df01 = preprocessing_data_until_2019(
                            io=f'{fold}/{file}', sheet_name=sheet_name, skiprows=7, header=0)
                        sheet_datas.append(df01)
                except:
                    pass
            # Transformação para cada arquivo com dados de 2020 em diante
            elif int(re.findall(pattern=r'\d+', string=file)[0]) >= 2020:
                # Tentar ler o arquivo com as abas úteis, caso a aba não exista no arquivo, será analisada aba seguinte da lista de abas úteis
                try:
                    df01, df_ajuste = preprocessing_data_from_2020_onwards(
                        io=f'{fold}/{file}', sheet_name=sheet_name, skiprows=7, header=0)
                    sheet_datas.append(df01)
                    sheet_datas.append(df_ajuste)
                except ValueError:
                    pass
        # Loop de consolidação de todos os dataframes de cada aba de um arquivo
        for sheet_data in sheet_datas:
            # Consolidação de cada dataframe gerado com o posterior arquivodo na lista de dataframes
            sheet_datas_merged = pd.merge(left=sheet_datas_merged, right=sheet_data, on=[
                                          'UF', 'COMPETÊNCIA'], how='outer')
        # adição da consolidação de todas as abas de um arquivo a lista de dataframes agrupados
        file_datas.append(sheet_datas_merged)
        # Reinicialização da lista sheet_datas para armazenamento das abas do proximo arquivo
        sheet_datas = []
        # Reinicialização dos dataframes agrupados para o o agrupamento do próximo arquivo
        sheet_datas_merged = pd.DataFrame({'UF': [], 'COMPETÊNCIA': []})
    # Concatenação de todos os dataframes agrupados de cada arquivo
    df01 = pd.concat(file_datas, axis='rows')
    # Substituição de valores nulos por 0
    df01 = df01.fillna(0)
    # Reorganização do index para a variável COMPETÊNCIA
    df01 = df01.set_index(keys='COMPETÊNCIA', drop=True)
    # Ordenamento das variáveis por ordem alfabética
    df01 = df01[sorted(df01.columns)]
    df01 = df01.reset_index()
    df01.to_parquet('./DATASETS/consolidated_data.parquet')
    return df01


# Acabamento final dos dados (Competência, uf, esfera, descrição, repasse, total)
def summarization_data(fold):
    df = consolidation_data(fold=fold)
    # Nome das variáveis numéricas decimais
    num_vars = df.dtypes[(df.dtypes.values == 'float64')].index
    # Convertendo colunas para uma variável
    df_melted = df.melt(id_vars=[
                        'COMPETÊNCIA', 'UF'], value_vars=num_vars, var_name='DESCRIÇÃO', value_name='TOTAL')
    # Criando coluna "Esfera"
    df_melted['ESFERA'] = df_melted['DESCRIÇÃO'].map(lambda x: 'Estadual' if (
        x.startswith('E')) or (x.startswith('A_E')) else 'Municipal')
    # Criando coluna do tipo de repasse
    df_melted['TIPO DE REPASSE'] = df_melted['DESCRIÇÃO'].map(
        lambda x: 'TOTAL LIQUIDO' if (x.startswith('E')) or (x.startswith('M')) else 'TOTAL AJUSTE')
    # Criando coluna do nome do repasse
    df_melted['REPASSE'] = df_melted['DESCRIÇÃO'].str.split(pat='_').map(
        lambda x: [i for i in x if i not in ['E', 'M', 'A']]).str.join(sep='_')
    # Reordenado variáveis
    df_melted[['COMPETÊNCIA', 'ESFERA', 'UF',
               'TIPO DE REPASSE', 'REPASSE', 'TOTAL']]
    # Convertendo coluna "COMPETÊNCIA" para datetime
    df_melted['COMPETÊNCIA'] = pd.to_datetime(
        df_melted['COMPETÊNCIA'], format=f'%Y-%m-%d')
    # Gerando tabela final
    df_pivoted = pd.pivot_table(data=df_melted, values='TOTAL', index=[
                                'ESFERA', 'UF', 'COMPETÊNCIA', 'REPASSE'], columns='TIPO DE REPASSE', aggfunc='sum', fill_value=0).reset_index()
    map = {'AFE_EC123': 'Outros',
           'Ajuste': 'Outros',
           'COUN': 'Outros',
           'COUN_VAAF': 'Complementação VAAF',
           'COUN_VAAR': 'Complementação VAAR',
           'COUN_VAAT': 'Complementação VAAT',
           'FPE': 'FPE',
           'FPM': 'FPM',
           'ICMS': 'ICMS',
           'IPI': 'IPI',
           'IPVA': 'IPVA',
           'ITCMD': 'ITCMD',
           'ITR': 'ITR',
           'LC8796': 'Outros'}
    df_pivoted['CATEGORIA'] = df_pivoted.REPASSE.map(map)
    cat_vars = df_pivoted.dtypes[df_pivoted.dtypes == 'O'].index
    for var in cat_vars:
        df_pivoted[var] = df_pivoted[var].astype('category')
    df_pivoted.to_parquet('./DATASETS/summarized_data.parquet')
    return df_pivoted


# Atualização dos dados
def upgrade_data(fold, update=True):
    if update == True:
        download_all_excel_datas(destiny_fold=fold)
        consolidation_data(fold=fold)
        summarization_data(fold=fold)
    else:
        try:
            consolidation_data(fold=fold)
            summarization_data(fold=fold)
        except:
            print('Erro! Talvez não haja arquivo na pasta informada!')
