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

        stocks = ['ELET3', 'ELET6', 'PETR3', 'PETR4', 'BBDC3', 'BBDC4', 'ITSA3', 'ITSA4', 'ITUB3',
                  'ITUB4', 'USIM3', 'USIM5', 'CMIG3', 'CMIG4', 'SANB11', 'BBAS3', 'BPAC11', 'BIDI3', 'BIDI4', 'BRSR6',
                  'BPAN4', 'ABCB4', 'GGBR4', 'CSNA3', 'VALE3']
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
