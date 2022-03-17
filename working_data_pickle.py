
import pandas as pd
import matplotlib.pyplot as plt
from calendar import monthrange
import datetime
import sys
import numpy as np
import rw_pickle as rw

def data_periodo(inicio, final):
    inicio = '{} 10:10:00'.format(inicio)
    final = '{} 16:54:00'.format(final)
    periodo = (inicio,final)
    return periodo

def stocks_tables_date_dataframe(stocks_names, stocks_tables, inicio, dias):

    stocks_tables_date = []

    for stock_table in stocks_tables:
        dataframe = stock_table
        dataframe['date_time'] = pd.to_datetime(dataframe['Datetime'])
        dataframe = dataframe.set_index('date_time')
        dataframe.drop(['Datetime'], axis=1, inplace=True)

        periodo = data_periodo(inicio, inicio)

        result_table = dataframe.loc[periodo[0]:periodo[1]]

        if dias > 1:
            inicio_date_format = datetime.datetime.strptime(inicio, '%Y-%m-%d')
            # inicio  formato = 'AAAA-MM-dd'
            for counter_dias in range(1, dias):

                inicio_for = inicio_date_format + datetime.timedelta(days=counter_dias)

                periodo_for = data_periodo(inicio_for, inicio_for)

                result_table_for = dataframe.sort_index().loc[periodo_for[0]:periodo_for[1]]

                result_table = result_table.append(result_table_for)

            stocks_tables_date.append(result_table)

        else:
            stocks_tables_date.append(result_table)

    stocks_tables_date_name = []

    n = 0
    for stock_table_date in stocks_tables_date:
        stock_table_date_name = stock_table_date.rename({'Close': stocks_names[n]}, axis=1)
        stocks_tables_date_name.append(stock_table_date_name)
        n += 1

    return stocks_tables_date_name

# with open('diff_table2.txt', 'w') as file:
#    diff_table.to_string(file)

def diferenca_stocks(dataframe1, dataframe2):

    #dataframe_result1 = dataframe1.reset_index()

    #dataframe_result2 = dataframe2.reset_index()

    #dataframe_result = pd.concat([dataframe_result1, dataframe_result2], join='inner')

    dataframe_result = pd.concat([dataframe1, dataframe2], axis=1, join='inner')

    #create_a_table_txt(dataframe_result,'dataframe_result2')

    dataframe_result['Diff'] = dataframe_result.iloc[:,0] - dataframe_result.iloc[:,1]

    return dataframe_result

def divisao_stocks(dataframe1, dataframe2):

    dataframe_result = pd.concat([dataframe1, dataframe2], axis=1, join='inner')

    dataframe_result['Div'] = dataframe_result.iloc[:,0] / dataframe_result.iloc[:,1]

    return dataframe_result


# criar tabelas txt da lista de stocks informada
def create_tables_stocks_txt(lista, stocks_parametro):
    n = 0
    for elemento in lista:
        nome_arq = 'stocks_db_analises\{}_db.txt'.format(stocks_parametro[n])
        with open(nome_arq, 'w') as file:
            elemento.to_string(file)

        n += 1

def create_a_table_txt(dataframe, nome):
    nome_arq = 'stocks_db_analises\{}_db.txt'.format(nome)
    with open(nome_arq, 'w') as file:
        dataframe.to_string(file)


#df = pd.DataFrame(table1, columns=['Datetime', 'Close'])

#df.plot(x='Datetime', y='Close', kind='line')
#plt.show()

def plot_visualization(table_diff, coluna):

    table_diff.plot(y=coluna, kind='line')
    table_diff.plot(y=coluna, kind='hist')
    plt.show()

def get_last_day_price(stocks_names, stocks_tables):


    #def stocks_tables_date_dataframe(stocks_names, stocks_tables, inicio, dias):

    stocks_values = []

    dataframe_data = stocks_tables[0]
    dataframe_data = dataframe_data.at[dataframe_data.index[-1], 'Datetime']
    dataframeString = str(dataframe_data)
    day_last_stock = dataframeString[0:10]
    datetime_today = '{} 16:54:00'.format(day_last_stock)


    for stock_table in stocks_tables:
        dataframe = stock_table
        dataframe['date_time'] = pd.to_datetime(dataframe['Datetime'])
        dataframe = dataframe.set_index('date_time')
        dataframe.drop(['Datetime'], axis=1, inplace=True)

        dataframe = dataframe[datetime_today: datetime_today]

        dataframe = dataframe[datetime_today:datetime_today]

        result_value = dataframe['Close'].values

        result_value = np.array2string(result_value,
                                       formatter={'float_kind':lambda result_value: "%.2f" % result_value})

        result_value = result_value.replace('[', '')
        result_value = result_value.replace(']', '')

        stocks_values.append(result_value)

    return stocks_values


if __name__ == '__main__':

    print("\t0 para usar a lista PN reduzida")
    print('\t1 para usar a lista PN full')
    print('\t2 para usar a lista setores')

    folder_names = []
    folder_names.append('stocks_data_pkl/')
    folder_names.append('stocks_data_csv/')
    type_names = []
    type_names.append('.pkl')
    type_names.append('.csv')

    lista_stock_escolha = int(input('\nDigite: '))

    if lista_stock_escolha == 0:

        stocks = ['ELET3', 'ELET6', 'PETR3', 'PETR4', 'BBDC3', 'BBDC4']
        nome_arquivo = 'sqlite:///stocks.db'
        data_minima = '2021-04-08'

    elif lista_stock_escolha == 1:

        stocks =['ELET3', 'ELET6', 'PETR3', 'PETR4', 'BBDC3', 'BBDC4', 'ITSA3', 'ITSA4',
                 'ITUB3', 'ITUB4', 'USIM3', 'USIM5', 'CMIG3', 'CMIG4']
        nome_arquivo = 'sqlite:///stocks_pn.db'
        data_minima = '2021-05-03'

    elif lista_stock_escolha == 2:

        stocks = ['ELET3', 'ELET6', 'PETR3', 'PETR4', 'BBDC3', 'BBDC4', 'ITSA3', 'ITSA4', 'ITUB3',
                  'ITUB4', 'USIM3', 'USIM5', 'CMIG3', 'CMIG4', 'SANB11', 'BBAS3', 'BPAC11', 'BIDI3', 'BIDI4', 'BRSR6',
                  'BPAN4', 'ABCB4', 'GGBR4', 'CSNA3', 'VALE3']

        nome_arquivo = 'sqlite:///stocks_setores.db'
        data_minima = '2021-05-03'

    else:
        print('\t\tArgumento digitado incorreto, programa encerrado!!!')
        sys.exit()


    reading_file_pickle = rw.Rw_pickle(stocks, folder_names, type_names)

    stocks_tables = reading_file_pickle.reading_list(stocks)

    #create_tables_stocks_txt(stocks_tables, stocks)

    print()

    stocks_close_values = get_last_day_price(stocks, stocks_tables)

    i = 0
    for index, stock in enumerate(stocks):
        print('{:2d}    {:^9}    {:6}'.format(index, stock, stocks_close_values[i]))
        i += 1

    print()

    index_primeiro_stock = int(input('Digite o index do primeiro stock a ser comparado: '))
    index_segundo_stock = int(input('Digite o index do segundo stock a ser comparado: '))

    print()

    print("\nData miníma: {}".format(data_minima))
    data_entrada = input("Digite a data no formato AAAA-MM-dd: ")
    n_dias_entrada = int(input("Digite o número de dias sendo o inicial o numero 1: "))

    print('\nSe a diferença entre stock 1 e stock 2 for muito grande será também necessária uma análise por divisão')
    tem_divisao = input("Necessita de calculo pela divisão, digite 's' ou 'n': ")

    # formato stocks (nomes) , stocks_tables (tabela do banco de daddos), '2021-04-08' (dia de inicio), 1 (a se pegar)
    # data inicio '2021-04-08'
    stocks_dates = stocks_tables_date_dataframe(stocks, stocks_tables, data_entrada, n_dias_entrada)

    #for stock_date in stocks_dates:
    #    print(stock_date)

    diferenca_de_acoes = diferenca_stocks(stocks_dates[index_primeiro_stock], stocks_dates[index_segundo_stock])
    divisao_de_acoes = divisao_stocks(stocks_dates[index_primeiro_stock], stocks_dates[index_segundo_stock])

    print('\t\t\tDiferença Stocks')

    print(diferenca_de_acoes)

    if tem_divisao == 's':

        print('\n\t\t\tDivisão Stocks')

        print(divisao_de_acoes)

    print('---------------------------------------------------------------------------')

    #create_a_table_txt(diferenca_de_acoes,'diferenca_elet')

    plot_visualization(diferenca_de_acoes, "Diff")
    if tem_divisao == 's':
        plot_visualization(divisao_de_acoes, "Div")

    #print(diferenca_de_acoes.loc[:, 'Diff'].mean())
    #print(diferenca_de_acoes.loc[:, 'Diff'].min())

    #print(diferenca_de_acoes.loc[:, 'Diff'].max())

    perc = [0.15, 0.50, 0.85]

    print('\t\t\tDiferença Stocks')
    print(diferenca_de_acoes.loc[:, 'Diff'].describe(percentiles=perc))
    print()
    if tem_divisao == 's':
        print('\t\t\tDivisão Stocks')
        print(divisao_de_acoes.loc[:, 'Div'].describe(percentiles=perc))


    #create_tables_stocks_txt(stocks_dates, stocks)