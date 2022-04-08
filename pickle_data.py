import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine
import sys
import rw_pickle as rw


def database_settings(periodo):

    folder_names = []
    folder_names.append('stocks_data_pkl/')
    folder_names.append('stocks_data_csv/')
    type_names = []
    type_names.append('.pkl')
    type_names.append('.csv')

    print("\t0 para usar a lista PN reduzida")
    print('\t1 para usar a lista PN full')
    print('\t2 para usar a lista setores')

    lista_stock_escolha = int(input('\nDigite: '))

    if lista_stock_escolha == 0:

        stocks = ['ELET3', 'ELET6', 'PETR3', 'PETR4', 'BBDC3', 'BBDC4']

    elif lista_stock_escolha == 1:

        stocks =['ELET3', 'ELET6', 'PETR3', 'PETR4', 'BBDC3', 'BBDC4', 'ITSA3', 'ITSA4',
                 'ITUB3', 'ITUB4', 'USIM3', 'USIM5', 'CMIG3', 'CMIG4']
    elif lista_stock_escolha == 2:

        stocks = ["ABCB4", "ABEV3", "AESB3", "ALPA4", "ALSO3", "AMER3", "ARZZ3", "ASAI3", "AURE3", "AZUL4", "B3SA3",
        "BBAS3", "BBDC3", "BBDC4", "BBSE3", "BEEF3", "BIDI11", "BIDI3", "BIDI4", "BPAN4", 
        "BPAC11", "BRAP4", "BRFS3", "BRKM5", "BRML3", "BRSR6", "CCRO3", "CMIN3", "CMIG3", 
        "CMIG4", "CIEL3", "CPFE3", "CPLE3", "CPLE6", "CRFB3", "CSAN3", "CSNA3", 
        "CSMG3", "CXSE3", "CYRE3", "DXCO3", "EGIE3", "ELET3", "ELET6", "ECOR3", "EMBR3", 
        "ENAT3", "ENBR3", "ENEV3", "ENGI11", "EQTL3", "GGBR4", "FLRY3", "GMAT3", "GOAU4", 
        "HAPV3", "GRND3", "ITSA3", "ITSA4", "ITUB3", "ITUB4", "HYPE3", "INTB3", "JBSS3", 
        "KLBN11", "KLBN4", "LCAM3", "LREN3", "LWSA3", "MGLU3", "MDIA3", "MOVI3", "MRFG3", 
        "MRVE3", "MULT3", "NTCO3", "NEOE3", "ODPV3", "OIBR3", "OIBR4", "PCAR3", "PETR3", "PETR4","PETZ3", 
        "PRIO3", "PSSA3", "RADL3", "RAIL3", "RDOR3", "RENT3", "RAIZ4", "SBSP3", "SANB11", 
        "SANB4", "RRRP3", "SAPR11", "SAPR4", "SBFG3", "SLCE3", "SMFT3", "SMTO3", "SOMA3", 
        "STBP3", "SUZB3", "SULA11", "TAEE11", "TASA4", "TIMS3", "TOTS3", "TRPL4", "UGPA3", 
        "UNIP6", "VBBR3", "VIVT3", "VALE3", "WEGE3", "USIM3", "USIM5", "VAMO3", "VIIA3", "VIVA3", 
        "YDUQ3"]

    else:
        print('\t\tArgumento digitado incorreto, programa encerrado!!!')
        sys.exit()

    stocks_SA = ['{}.SA'.format(stock) for stock in stocks]

    print(stocks)

    #ticker_list = [yf.Ticker(stock) for stock in stocks]

    ticker_list = [yf.Ticker(stock) for stock in stocks_SA]

    results_history = [ticker.history(period=periodo, interval='1m') for ticker in ticker_list]
    #results_history = [ticker.history(period='7d', interval='1m') for ticker in ticker_list]

    results_close_history = [result[['Close']] for result in results_history]

    Writing_file = rw.Rw_pickle(stocks, folder_names, type_names)

    print("Escrevendo os arquivos na base de dados")

    Writing_file.writing_list(results_close_history)



"""
    n = 0
    for result in results_close_history:
        result.to_pickle('stocks_data/'+ stocks[n] + '.pkl', compression='bz2')
        n += 1

"""

#elet3 = yf.Ticker('ELET3.SA')

#result = elet3.history(period='7d', interval='1m')

#first_data = pd.read_csv("dados_second.txt", sep='\s\s', header=0, names=["Close"], infer_datetime_format=True,
#                         index_col='Datetime', engine='python')
# print(first_data)


#first_data.index = pd.to_datetime(first_data.index)
#first_data.index = first_data.index.tz_convert('America/Sao_Paulo')
#print(first_data.index)

#with open('dados_first.txt', 'w') as file:
#    first_data.to_string(file)

# with open('dados_14.txt', 'w') as file:
#    print(result.columns)
#    result_formatado = result[['Close']]
#    print(type(result_formatado))
#    result_formatado.to_string(file)

#    print(result.index)

if __name__ == '__main__':
    # '7d' é o inicial
    # '1d' é o incremental

    escolha_dos_dias = input('\nDigite o numero de dias de 1 à 7: ')

    dias_formatado = escolha_dos_dias+'d'

    database_settings(dias_formatado)
