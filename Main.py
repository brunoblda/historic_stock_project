import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine
import sys


def database_settings(periodo):

    print("\t0 para usar a lista PN reduzida")
    print('\t1 para usar a lista PN full')
    print('\t2 para usar a lista setores')

    lista_stock_escolha = int(input('\nDigite: '))

    if lista_stock_escolha == 0:

        stocks = ['ELET3', 'ELET6', 'PETR3', 'PETR4', 'BBDC3', 'BBDC4', 'LAME4', 'LAME3']
        nome_arquivo = 'sqlite:///stocks.db'

    elif lista_stock_escolha == 1:

        stocks =['ELET3', 'ELET6', 'PETR3', 'PETR4', 'BBDC3', 'BBDC4', 'LAME3', 'LAME4', 'ITSA3', 'ITSA4',
                 'ITUB3', 'ITUB4', 'USIM3', 'USIM5', 'CMIG3', 'CMIG4']
        nome_arquivo = 'sqlite:///stocks_pn.db'
    elif lista_stock_escolha == 2:

        stocks = ['ELET3', 'ELET6', 'PETR3', 'PETR4', 'BBDC3', 'BBDC4', 'LAME3', 'LAME4', 'ITSA3', 'ITSA4', 'ITUB3',
                  'ITUB4', 'USIM3', 'USIM5', 'CMIG3', 'CMIG4', 'SANB11', 'BBAS3', 'BPAC11', 'BIDI3', 'BIDI4', 'BRSR6',
                  'BPAN4', 'ABCB4', 'GGBR4', 'CSNA3', 'VALE3']
        nome_arquivo = 'sqlite:///stocks_setores.db'
    else:
        print('\t\tArgumento digitado incorreto, programa encerrado!!!')
        sys.exit()


    stocks = ['{}.SA'.format(stock) for stock in stocks]

    print(stocks)

    #ticker_list = [yf.Ticker(stock) for stock in stocks]

    ticker_list = [yf.Ticker(stock) for stock in stocks]

    results_history = [ticker.history(period=periodo, interval='1m') for ticker in ticker_list]
    #results_history = [ticker.history(period='7d', interval='1m') for ticker in ticker_list]

    results_close_history = [result[['Close']] for result in results_history]

    engine = create_engine(nome_arquivo, echo=True)

    with engine.connect() as sqlite_connection:
        n = 0
        for result in results_close_history:
            result.to_sql(stocks[n], sqlite_connection, if_exists='append')
            n += 1


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
    database_settings('7d')
