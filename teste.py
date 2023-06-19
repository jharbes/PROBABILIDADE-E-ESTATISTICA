"""
Este script realiza a extração e análise de dados de Fundos de Investimento Imobiliário (FIIs) 
do site "https://www.fundamentus.com.br/fii_resultado.php".
Ele utiliza a biblioteca Pandas para realizar a leitura de uma tabela HTML.
além disso também realiza a limpeza e transformação os dados, 
e a biblioteca BeautifulSoup para fazer o scraping dos dados da página web.
Este script utiliza o streamlit para criar uma aplicação web para visualizar os dados.

Requisitos:
- pandas
- requests
- beautifulsoup4
- streamlit

Uso:
1. Certifique-se de ter todas as bibliotecas necessárias instaladas.
2. Execute o script para extrair os dados dos FIIs do site e realizar a limpeza dos dados.
3. Os dados limpos serão salvos em um dataframe.
4. Por meio da biblioteca streamlit os dados são exibidos em uma ambiente web
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup
import streamlit as st

URL = "https://www.fundamentus.com.br/fii_resultado.php"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                  "(KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
}

response = requests.get(URL, headers=headers, timeout=10)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    tabela_html = soup.find('table')

    df_fii = pd.read_html(str(tabela_html))[0]

    # Realizar a limpeza dos dados durante a leitura do HTML
    df_fii['FFO Yield'] = df_fii['FFO Yield'].str.replace(
        '%', '').str.replace(',', '').astype(float)

    df_fii['Vacância Média'] = df_fii['Vacância Média'].str.replace(
        '%', '').str.replace(',', '').astype(float)

    df_fii['Cap Rate'] = df_fii['Cap Rate'].str.replace(
        '%', '').str.replace(',', '').astype(float)

    df_fii['Dividend Yield'] = df_fii['Dividend Yield'].str.replace(
        '%', '', regex=True).str.replace(',', '').str.replace('.', '').astype(float)

    df_fii['Cotação'] = df_fii['Cotação'].str.replace(
        '.', '', regex=True).str.replace(',', '').astype(float)

    df_fii['Valor de Mercado'] = df_fii['Valor de Mercado'].str.replace(
        '.', '', regex=True).astype(float)

    df_fii['Liquidez'] = df_fii['Liquidez'].str.replace(
        '.', '', regex=True).astype(float)

    df_fii['Preço do m2'] = df_fii['Preço do m2'].str.replace(
        '.', '', regex=True).str.replace(',', '').astype(float)

    df_fii['Aluguel por m2'] = df_fii['Aluguel por m2'].str.replace(
        '.', '', regex=True).str.replace(',', '').astype(float)

    df_fii.rename(columns={'FFO Yield': 'FFO Yield(%)',
                           'Vacância Média': 'Vacância Média(%)',
                           'Cap Rate': 'Cap Rate(%)',
                           'Dividend Yield': 'Dividend Yield(%)'},
                  inplace=True)

    df_fii['Cotação'] = df_fii['Cotação'] / 100
    df_fii['FFO Yield(%)'] = df_fii['FFO Yield(%)'] / 100
    df_fii['P/VP'] = df_fii['P/VP'] / 100
    df_fii['Preço do m2'] = df_fii['Preço do m2'] / 100
    df_fii['Aluguel por m2'] = df_fii['Aluguel por m2'] / 100
    df_fii['Dividend Yield(%)'] = df_fii['Dividend Yield(%)'] / 100
    df_fii['Cap Rate(%)'] = df_fii['Cap Rate(%)'] / 100
    df_fii['Vacância Média(%)'] = df_fii['Vacância Média(%)'] / 100

else:
    print("Erro ao acessar a página")

# tirar liquidez igual 0

# alocando as variáveis importantes para parametros
max_valor_mercado = df_fii['Valor de Mercado'].max()
min_valor_mercado = df_fii['Valor de Mercado'].min()

min_liquidez = df_fii['Liquidez'].min()
max_liquidez = df_fii['Liquidez'].max()

min_vacancia = df_fii['Vacância Média(%)'].min()
max_vacancia = df_fii['Vacância Média(%)'].max()

# Utilizando o streamlit

st.set_page_config(
    page_title="Visão Geral",
    page_icon="📈",
    # layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
    }
)

st.write("# Análise dos Fundos Imobiliários do Brasil")
st.dataframe(df_fii)

st.sidebar.text("Filtros:")

valor_max = st.sidebar.number_input("Valor máximo da Cota:")

maior_dividend = st.sidebar.number_input("Dividend Yield maior que:")

filtro_pvp = st.sidebar.slider(
    "P/VP entre:",
    min_value=0.0,
    max_value=2.0,
    value=[0.4, 1.1])
pvp_menor = filtro_pvp[0]
pvp_maior = filtro_pvp[1]

filtro_mercado = st.sidebar.slider(
    "Valor de Mercado maior que:",
    min_value=float(min_valor_mercado),
    max_value=float(max_valor_mercado),
    value=[400000000.0, 650000000.0])
mercado_menor = filtro_mercado[0]
mercado_maior = filtro_mercado[1]

filtro_liquidez = st.sidebar.slider(
    "Liquidez maior que:",
    min_value=float(min_liquidez),
    max_value=float(max_liquidez),
    value=760000.0)

filtro_vacancia = st.sidebar.slider(
    "Vacância média menor que:",
    min_value=float(min_vacancia),
    max_value=float(max_vacancia),
    value=5.0)

# mostrando os gráficos
