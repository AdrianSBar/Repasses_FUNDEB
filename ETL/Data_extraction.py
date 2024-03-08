import os
import shutil
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import numpy as np
import pandas as pd
import re
import datetime
import time
import xlrd
import streamlit as st
import plotly.express as px


# EXTRAÇÃO DOS DADOS
# - Função de download de um arquivo excel do site por ano
def download_one_excel_data(ano):
    # Iniciando o webdriver manager do navegador google chrome na sua ultima versão correspondente
    driver = webdriver.Chrome(ChromeDriverManager().install())
    if ano != 2022:
        # URL da página que contém o botão de download
        url = f"https://www.tesourotransparente.gov.br/publicacoes/transferencias-ao-fundo-de-manutencao-e-desenvolvimento-da-educacao-basica-fundeb/{ano}/114?ano_selecionado={ano}"
        # Acessando url
        driver.get(url)
        # Clicando no botão de download
        driver.find_element(
            by='xpath',
            value='//*[@id="publicacao"]/div/div[2]/section/div[4]/a').click()
        time.sleep(10)
        driver.quit()
    else:
        # URL da página que contém o botão de download
        url = 'https://www.tesourotransparente.gov.br/publicacoes/transferencias-ao-fundo-de-manutencao-e-desenvolvimento-da-educacao-basica-fundeb/2022/114-2?ano_selecionado=2022'
        # Acessando url
        driver.get(url)
        # Clicando no botão de download
        driver.find_element(
            by='xpath',
            value='//*[@id="publicacao"]/div/div[2]/section/div[4]/a').click()
        time.sleep(10)
        driver.quit()


# - Função de regras de nomeação e destinação dos arquivos
def excel_file_name(ano):
    if ano in [2007, 2009, 2010, 2011, 2013]:
        # Especifique o caminho completo do arquivo que você deseja mover
        origin = os.path.join(os.path.expanduser(
            '~'), 'Downloads', f'Fundeb{ano}.xls')
    elif ano == 2008:
        # Especifique o caminho completo do arquivo que você deseja mover
        origin = os.path.join(os.path.expanduser(
            '~'), 'Downloads', f'Fundeb_{ano}.xls')
    elif ano in [2012, 2014, 2015, 2016, 2017]:
        # Especifique o caminho completo do arquivo que você deseja mover
        origin = os.path.join(os.path.expanduser(
            '~'), 'Downloads', f'pge_fundeb_{ano}.xls')
    else:
        # Especifique o caminho completo do arquivo que você deseja mover
        origin = os.path.join(os.path.expanduser(
            '~'), 'Downloads', f'Fundeb {ano}.xls')
    return origin


# - Função para efetuar o download de todos os arquivos até o ano corrente caso não hajam dentro da pasta
def download_all_excel_datas(destiny_fold):
    # Criando variável do ano corrente
    corrent_year = datetime.datetime.today().year
    # Loop para baixar todos os arquivos a partir de 2007 até o ano corrente
    for ano in range(2007, corrent_year+1, 1):
        if f'Fundeb {ano}.xls' not in os.listdir(path=destiny_fold):
            print(f'Arquivo {ano} não encontrado, efetuando download.')
            # Efetuando o download do arquivo
            download_one_excel_data(ano)
            # Especificando pasta de destino padrão - Downloads
            origin = excel_file_name(ano=ano)
            # Especifique o caminho completo da pasta de destino
            destiny = f"{destiny_fold}/Fundeb {ano}.xls"
            # Ajustando pasta
            # Mova o arquivo para a pasta de destino
            shutil.move(origin, destiny)
        else:
            # Especifique o caminho completo do arquivo que você deseja verificar
            destiny = f"{destiny_fold}/Fundeb {ano}.xls"
            # Obtenha os metadados do arquivo, incluindo a data de modificação
            info = os.stat(destiny)
            # Acesse a data de modificação do arquivo
            last_modification = info.st_mtime
            # Converta a data de modificação para um formato legível
            data_formatada = time.ctime(last_modification)
            if (int(data_formatada[-5:]) < corrent_year) or (ano == corrent_year):
                print(f'Arquivo {ano} desatualizado, refazendo download.')
                # Efetuando o download do arquivo
                download_one_excel_data(ano)
                # Especificando pasta de destino padrão - Downloads
                origin = excel_file_name(ano=ano)
                # Substituindo o arquivo para a pasta de destino
                shutil.copy(origin, destiny)
