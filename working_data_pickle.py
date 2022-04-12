
import pandas as pd
import matplotlib.pyplot as plt
from calendar import monthrange
import datetime
import sys
import numpy as np
import rw_pickle as rw

def data_periodo(dia):
    inicio = '{} 10:10:00'.format(dia)
    final = '{} 16:54:00'.format(dia)
    periodo = (inicio,final)
    return periodo

def stocks_tables_date_dataframe(stocks_names, stocks_tables, dia_inicial, dias):

    stocks_tables_date = []

    for stock_table in stocks_tables:
        dataframe = stock_table
        dataframe['date_time'] = pd.to_datetime(dataframe['Datetime'])
        dataframe = dataframe.set_index('date_time')
        dataframe.drop(['Datetime'], axis=1, inplace=True)

        horario_inicial, horario_final= data_periodo(dia_inicial)

        # resulta em um dataframe do primeiro dia escolhido do inicio do dia ao final do dia 
        result_table = dataframe.loc[horario_inicial:horario_final]

        if dias > 1:
            inicio_date_format = datetime.datetime.strptime(dia_inicial, '%Y-%m-%d')
            # inicio  formato = 'AAAA-MM-dd'

            # resulta em um dataframe para cada dia após o primeiro  
            for counter_dias in range(1, dias):

                inicio_for = inicio_date_format + datetime.timedelta(days=counter_dias)
                horario_for_inicial, horario_for_final = data_periodo(inicio_for)
                result_table_for = dataframe.sort_index().loc[horario_for_inicial:horario_for_final]
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

def plot_visualization(list_table_diff_div, coluna):
    for i in range(len(list_table_diff_div)):
        list_table_diff_div[i].plot(y=coluna[i], kind='line')
        list_table_diff_div[i].plot(y=coluna[i], kind='hist')
    plt.show()

def get_last_day_price(stocks_tables):

    stocks_values = []

    dataframe_data = stocks_tables[0]
    dataframe_data = dataframe_data.at[dataframe_data.index[-1], 'Close']

    for stock_table in stocks_tables:
        dataframe = stock_table

        dataframe['date_time'] = pd.to_datetime(dataframe['Datetime'])
        dataframe = dataframe.set_index('date_time')
        dataframe.drop(['Datetime'], axis=1, inplace=True)
        dataframe = dataframe[-1:]

        result_value = dataframe['Close'].values

        result_value = np.array2string(result_value,
                                       formatter={'float_kind':lambda result_value: "%.2f" % result_value})

        result_value = result_value.replace('[', '')
        result_value = result_value.replace(']', '')

        stocks_values.append(result_value)

    return stocks_values

def data_distribution_percentil(data_analise):

    data_15 = data_analise[4]
    data_50 = data_analise[5]
    data_75 = data_analise[6]

    data_rel_1 = data_50 - data_15
    data_rel_2 = data_75 - data_50

    data_rel_R = 0.0

    if data_rel_1 < data_rel_2:
        data_rel_R = data_rel_1/data_rel_2
    else:
        data_rel_R = data_rel_2/data_rel_1

    return data_rel_R

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
        
        nome_arquivo = 'sqlite:///stocks_setores.db'
        data_minima = '2021-05-03'

    else:
        print('\t\tArgumento digitado incorreto, programa encerrado!!!')
        sys.exit()


    reading_file_pickle = rw.Rw_pickle(stocks, folder_names, type_names)

    stocks_tables = reading_file_pickle.reading_list(stocks)

    #create_tables_stocks_txt(stocks_tables, stocks)

    print()

    stocks_close_values = get_last_day_price(stocks_tables)

    #print(stocks_close_values)

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

    """
    Este codigo realizava a contagem de todas as ações presentes nos arquivos

    # formato stocks (nomes) , stocks_tables (tabela do banco de daddos), '2021-04-08' (dia de inicio), 1 (a se pegar)
    # data inicio '2021-04-08'
    stocks_dates = stocks_tables_date_dataframe(stocks, stocks_tables, data_entrada, n_dias_entrada)

    #for stock_date in stocks_dates:
    #    print(stock_date)

    diferenca_de_acoes = diferenca_stocks(stocks_dates[index_primeiro_stock], stocks_dates[index_segundo_stock])
    divisao_de_acoes = divisao_stocks(stocks_dates[index_primeiro_stock], stocks_dates[index_segundo_stock])
    """

    #Este codigo realiza a mesma função que o codigo acima, o indice escolhido antes.
    stock_date_1 = stocks_tables_date_dataframe([stocks[index_primeiro_stock],], [stocks_tables[index_primeiro_stock],], data_entrada, n_dias_entrada)
    stock_date_2 = stocks_tables_date_dataframe([stocks[index_segundo_stock],], [stocks_tables[index_segundo_stock],], data_entrada, n_dias_entrada)

    #for stock_date in stocks_dates:
    #    print(stock_date)

    diferenca_de_acoes = diferenca_stocks(stock_date_1[0], stock_date_2[0])
    divisao_de_acoes = divisao_stocks(stock_date_1[0], stock_date_2[0])


    print('\t\t\tDiferença Stocks')

    print(diferenca_de_acoes)

    if tem_divisao == 's':

        print('\n\t\t\tDivisão Stocks')

        print(divisao_de_acoes)

    print('---------------------------------------------------------------------------')

    #create_a_table_txt(diferenca_de_acoes,'diferenca_elet')

    perc = [0.15, 0.50, 0.85]

    print('\t\t\tDiferença Stocks')
    dados_analise_diferenca = diferenca_de_acoes.loc[:, 'Diff'].describe(percentiles=perc) 
    print(dados_analise_diferenca)
    print()
    data_rel_R = data_distribution_percentil(dados_analise_diferenca)
    print("Relação da distribuição")
    print(data_rel_R)
    
    if tem_divisao == 's':
        print('\t\t\tDivisão Stocks')
        dados_analise_divisao = divisao_de_acoes.loc[:, 'Div'].describe(percentiles=perc) 
        print(dados_analise_divisao)
        print()
        data_rel_R = data_distribution_percentil(dados_analise_divisao)
        print("Relação da distribuição")
        print(data_rel_R)

    """
    # Analise de dados por distribuição normal

    numpy_serie_dif = diferenca_de_acoes.loc[:, 'Diff'].to_numpy()

    def normal_dist(x , mean , sd):
        prob_density = (np.pi*sd) * np.exp(-0.5*((x-mean)/sd)**2)
        return prob_density

    mean = np.mean(numpy_serie_dif)
    sd = np.std(numpy_serie_dif)

    pdf = normal_dist(numpy_serie_dif,mean, sd)

    plt.plot(numpy_serie_dif,pdf , color = 'red')
    plt.xlabel('Data points')
    plt.ylabel('Probability Density')
    """
    list_diff_and_div = []
    string_diff_and_div = []

    if tem_divisao == 's':
        
        list_diff_and_div.append(diferenca_de_acoes)
        list_diff_and_div.append(divisao_de_acoes)

        string_diff_and_div.append("Diff")
        string_diff_and_div.append("Div")

        plot_visualization(list_diff_and_div, string_diff_and_div)

    else:

        list_diff_and_div.append(diferenca_de_acoes)
        string_diff_and_div.append("Diff")

        plot_visualization(list_diff_and_div, string_diff_and_div)

    #print(diferenca_de_acoes.loc[:, 'Diff'].mean())
    #print(diferenca_de_acoes.loc[:, 'Diff'].min())
    #print(diferenca_de_acoes.loc[:, 'Diff'].max())
    #create_tables_stocks_txt(stocks_dates, stocks)