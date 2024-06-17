#######################################
#   HERBIA BIOBRAZIL 2024 DASHBOARD   #
#   Author: Dalton Hardt              #
#   Date:  JUNHO/24                   #
#######################################
from datetime import datetime
from pathlib import Path
import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
import locale


################################################################################################
# DEFINICOES GERAIS

locale.setlocale(locale.LC_ALL, 'pt_BR') 

# DIRETORIO DO ARQUIVO DE VENDAS
dir_vendas = str(Path.home()) + '/Desktop/VendasFeira2024'

# ARQUIVO QUE VAI CONTER OS DADOS DAS VENDAS
arq_venda_total = dir_vendas + '/TotalVendasFeira2024.csv'

# COLUNAS QUE SERÃO GRAVADAS NO ARQUIVO
colunas_venda = ['TICKET', 'DATA', 'HORA', 'TIPO-VENDA', 'FORMA-PAGO', 'CODIGO', 'PRODUTO', 'QTDE', 'VALOR-ITEM',
                 'TOTAL-ITEM', 'DESCONTO', 'TOTAL', 'TOTAL-COMPRA', 'VALOR-COBRADO']

# DIA DE HOJE NO FORMATO dd-mm-aaaa
today = datetime.now()
hoje = today.strftime('%d-%m-%Y')
hora = today.strftime('%H:%M:%S')

# DIAS DA SEMANA EM PORTUGUES
dias_semana = ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado', 'Domingo']
wkday = today.weekday()


################################################################################################
# Para mostrar todas as linhas e colunas do Dataframe
#pd.set_option('display.max_rows', None)
#pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
pd.set_option('max_colwidth', 25)

warnings.filterwarnings('ignore')

################################################################################################

st.set_page_config(page_title='Herbia Dashboard', page_icon=':bar_chart:', layout='wide')
#st.image('/Users/dalton/Desktop/workspace/code/HERBIA/Feira-2024/Images/Logo-Herbia.png')
st.title(':bar_chart: Herbia Dashboard BioBrazil 2024')
# st.divider()
st.markdown('<style>div.block-container{padding-top:2rem;}</style>', unsafe_allow_html=True)

# arquivo = st.file_uploader(':file_folder: Upload file', type=(['csv']))
# Lendo o arquivo CSV
arquivo = st.sidebar.file_uploader('Escolha o arquivo (.csv)', type='csv')

if arquivo:
    filename = arquivo.name
    # print('filename:', filename)
    #st.write(filename, encoding='utf-8')
    df = pd.read_csv(filename, date_format='%d/%m/%Y', encoding='utf-8')
    df = df.drop('HORA', axis=1)

    col1, col2, col3 = st.columns((3))
    col4, col5, col6 = st.columns((3))
    col7, col8 = st.columns((2))

    # print('convertendo a coluna DATA para o formato datetime')
    df['DATA'] = pd.to_datetime(df['DATA'], format='%d/%m/%Y')
    df['DIA'] = df['DATA'].dt.strftime('%d-%m-%Y')
    # df['DIA'] = pd.to_datetime(df['DATA'], format='%d/%m/%Y')
    df['TICKET'] = df['TICKET'].astype(str)
    #print('\n===dataframe:\n', df)

    df_total_venda_feira = df.copy()
    df_total_venda_feira = df_total_venda_feira.drop_duplicates(['TICKET'])
    df_total_venda_feira = df_total_venda_feira['VALOR-COBRADO'].sum()
    str_total_venda_feira = locale.format_string('R$ %.2f', df_total_venda_feira, True)

    # pegando a minima e maxima data
    startDate = pd.to_datetime(df['DATA']).min()
    #print('startDate:', startDate)
    endDate = pd.to_datetime(df['DATA']).max()
    #print('endDate:', endDate)


    st.sidebar.header('Escolha um filtro:')

    # Datas do intervalo das vendas
    date1 = pd.to_datetime(st.sidebar.date_input('Data inicio', startDate, format="DD/MM/YYYY"))
    date2 = pd.to_datetime(st.sidebar.date_input('Data fim', endDate, format="DD/MM/YYYY"))
    df = df[(df['DATA'] >= date1) & (df['DATA'] <= date2)]
    
    df_valor_cobrado = df.drop_duplicates(['TICKET'])
    # print('df_valor_cobrado:\n', df_valor_cobrado)

    df_total_venda_periodo = df_valor_cobrado['VALOR-COBRADO'].sum()
    str_total_venda_periodo = locale.format_string('R$ %.2f', df_total_venda_periodo, True)

    with col1:
        st.markdown(
            """
            <style>
            [data-testid="stMetricValue"] {
                font-size: 50px;
            }
            </style>
            """,
                unsafe_allow_html=True,
            )
        st.metric(label='TOTAL VENDAS NA FEIRA', value=str_total_venda_feira)
        st.divider()

    # Cria filtro para o Tipo de Venda
    tipoVenda = st.sidebar.multiselect('Escolha o tipo de Venda', df['TIPO-VENDA'].unique())
    if not tipoVenda:
        df2 = df.copy()
    else:
        df2 = df[df['TIPO-VENDA'].isin(tipoVenda)]
    
    # Cria filtro para o tipo de pagamento
    formaPago = st.sidebar.multiselect('Escolha a forma de pagamento', df2['FORMA-PAGO'].unique())
    if not formaPago:
        df3 = df2.copy()
    else:
        df3 = df2[df['FORMA-PAGO'].isin(formaPago)]
    
    # Cria filtro para o produto
    lista_produtos = df3['PRODUTO'].unique()
    lista_produtos.sort()
    produto = st.sidebar.multiselect('Escolha o Produto', lista_produtos)
    
    # Filtrando os dados do dataframe baseado em tipoVenda, formaPago e produto
    #print('\ntipoVenda:', tipoVenda)
    #print('formaPago:', formaPago)
    #print('produto:', produto)
    if not tipoVenda and not formaPago and not produto:
        df_filtrado = df
        filtro = ' dos produtos'
    elif not formaPago and not produto:
        df_filtrado = df[df['TIPO-VENDA'].isin(tipoVenda)]
        filtro = 'para ' + ', '.join(tipoVenda)
    elif not tipoVenda and not produto:
        df_filtrado = df[df['FORMA-PAGO'].isin(formaPago)]
        filtro = 'no ' + ', '.join(formaPago)
    elif not tipoVenda and not formaPago:
        df_filtrado = df[df['PRODUTO'].isin(produto)]
        filtro = ', '.join(produto)
    elif produto and formaPago and tipoVenda:
        df_filtrado = df3[df3['TIPO-VENDA'].isin(tipoVenda) & 
                            df3['FORMA-PAGO'].isin(formaPago) & 
                            df3['PRODUTO'].isin(produto)]
        filtro = 'para ' + ', '.join(tipoVenda) + ' no '+ ', '.join(formaPago)
    elif tipoVenda and formaPago:
        df_filtrado = df3[df['TIPO-VENDA'].isin(tipoVenda) & df3['FORMA-PAGO'].isin(formaPago)]
        filtro = 'para '+ ', '.join(tipoVenda) + ' no '+ ', '.join(formaPago)
    elif tipoVenda and produto:
        df_filtrado = df3[df['TIPO-VENDA'].isin(tipoVenda) & df3['PRODUTO'].isin(produto)]
        filtro = 'para '+ ', '.join(tipoVenda)
    elif formaPago and produto:
        df_filtrado = df3[df['FORMA-PAGO'].isin(formaPago) & df3['PRODUTO'].isin(produto)]
        filtro = 'no '+ ', '.join(formaPago)
    elif produto:
        df_filtrado = df3[df3['PRODUTO'].isin(produto)]
        filtro = ' dos produtos'
    
    # reset no indice do dataframe
    df_filtrado.reset_index(inplace=True, drop=True)

    df_produto = df_filtrado.groupby(by=['PRODUTO'], as_index=False)['TOTAL'].sum()
    #print('df_produto:\n', df_produto)
    #print('df_filtrado:\n', df_filtrado)

    df_valor_cobrado = df_filtrado.drop_duplicates(['TICKET'])
    # print('df_valor_cobrado:\n', df_valor_cobrado)

    df_total_venda_periodo = df_valor_cobrado['VALOR-COBRADO'].sum()
    str_total_venda_periodo = locale.format_string('R$ %.2f', df_total_venda_periodo, True)

    # calculando percentual dos itens filtrados sobre o valor total de vendas
    percentual_filtrado = df_total_venda_periodo / df_total_venda_feira

    # calculando a quantidade de pedidos (TICKETS)
    num_tickets = len(df_filtrado.groupby(by=['TICKET']))
    #print('======= Numero de Tickets:', num_tickets)
    # calculando o ticket médio do periodo
    str_ticket_medio_periodo = locale.format_string('R$ %.2f', df_total_venda_periodo/num_tickets, True)

    # somando a quantidade de itens vendidos
    total_itens = df_filtrado['QTDE'].sum()
    #print('total_itens:', total_itens)

    # filtrando o dataframe para pegar somente os produtos e quantidades
    df_filtrado_qtde = df_filtrado.groupby(['PRODUTO'])[['QTDE']].sum().sort_values('QTDE', ascending=False)
    df_filtrado_qtde.reset_index(inplace=True)
    #print('df_filtrado_qtde:\n', df_filtrado_qtde)

    with col4:
        st.metric(label='\# TICKETS:', value=num_tickets)
        st.divider()
    with col5:
        st.metric(label='QUANTIDADE PRODUTOS:', value=total_itens)
        st.divider()
    if 'BRINDE' not in tipoVenda:
        with col6:
            st.metric(label='TICKET MÉDIO:', value=str_ticket_medio_periodo)
            st.divider()

    if produto or formaPago or tipoVenda or date1 != startDate or date2 != endDate:
        if not (len(tipoVenda) == 1 and 'BRINDE' in tipoVenda):
            with col2:
                st.markdown(
                    """
                    <style>
                    [data-testid="stMetricValue"] {
                        font-size: 50px;
                    }
                    </style>
                    """,
                        unsafe_allow_html=True,
                    )
                st.metric(label='TOTAL VENDAS FILTRADAS', value=str_total_venda_periodo)
                st.divider()
            with col3:
                st.markdown(
                    """
                    <style>
                    [data-testid="stMetricValue"] {
                        font-size: 50px;
                    }
                    </style>
                    """,
                        unsafe_allow_html=True,
                    )
                st.metric(label="Percentual", value="{:.2%}".format(percentual_filtrado), label_visibility="hidden")
                st.divider()

    with col7:
            st.subheader('Quantidade de produtos')
            # df_filtrado_qtde = df_filtrado_qtde.sort_values('QTDE')
            fig = px.bar(df_filtrado_qtde, x='PRODUTO', y='QTDE', text = [format(x) for x in df_filtrado_qtde["QTDE"]])
            fig.update_traces(marker_color='green')
            st.plotly_chart(fig,use_container_width=True)


    if not (len(tipoVenda) == 1 and 'BRINDE' in tipoVenda):
        with col8:
            df_produto = df_produto.sort_values(['TOTAL'], ascending=[False])
            st.subheader(f'Total Vendas {filtro}')
            fig = px.bar(df_produto, x='PRODUTO', y='TOTAL', text = ['R$ {:,.2f}'.format(x) for x in df_produto["TOTAL"]],
                            template='gridon', hover_data=['TOTAL'])
            st.plotly_chart(fig, use_container_width=True)  
        
    #print('df_filtrado:\n', df_filtrado)
    #st.write(df_filtrado)
    st.dataframe(df_filtrado, column_order=("DIA", "TICKET", "TIPO-VENDA", "FORMA-PAGO",
                                            "PRODUTO", "QTDE", "VALOR-ITEM", "TOTAL-ITEM",
                                            "DESCONTO", "TOTAL", "TOTAL-COMPRA", "VALOR-COBRADO"))
