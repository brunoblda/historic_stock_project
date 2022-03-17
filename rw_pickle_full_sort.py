from re import I
import pandas as pd
from os.path import exists
from os.path import split
import sys

class Rw_pickle:

    def __init__(self, stocks_name, folder_names, type_names):

        self.stocks_name = stocks_name
        self.folder_names = folder_names
        self.type_names = type_names 

    def writing_list(self, write_list):

        n = 0
        for write_element in write_list:

            name_stock_pickle = self.folder_names[0]+ self.stocks_name[n] + self.type_names[0]
            name_stock_csv = self.folder_names[1]+ self.stocks_name[n] + self.type_names[1]

            if exists(name_stock_pickle):
                unpickle_stock = pd.read_pickle(name_stock_pickle, compression='bz2')  

                print(unpickle_stock.columns)

                print(unpickle_stock.index)

                # Concatena os dados que estão no banco de dados com os novos dados
                unpickle_stock = pd.concat([unpickle_stock, write_element])

                # Realiza a ordenação pelo index
                unpickle_stock = unpickle_stock.sort_index()
                
                print(type(unpickle_stock))
                print(unpickle_stock.head())

                # Transforma o index em coluna
                unpickle_stock.reset_index(inplace=True)

                print(type(unpickle_stock))
                print(unpickle_stock.head())

                # Elimina as colunas duplicadas
                unpickle_stock = unpickle_stock.drop_duplicates()

                print(unpickle_stock.head())
                
                print(unpickle_stock.columns)

                print(unpickle_stock.index)

                # Transforma o Datetime novamente em index
                unpickle_stock = unpickle_stock.set_index(['Datetime'])

                print("-----------------")

                print(unpickle_stock.head())
                
                print(unpickle_stock.columns)

                print(unpickle_stock.index)

                unpickle_stock.to_pickle(name_stock_pickle, compression='bz2')
                unpickle_stock.to_csv(name_stock_csv)

            else:

                print(write_element.columns)

                print(write_element.index)

                write_element.to_pickle(name_stock_pickle, compression='bz2')
                write_element.to_csv(name_stock_csv )
                
            n += 1

        print("Gravação foi um sucesso !!!")


    def reading_list(self, read_stocks):

        unpickle_stocks = []

        n = 0
        for read_stock in read_stocks:

            name_stock_pickle = self.folder_names[0] + read_stock + '.pkl'

            unpickle_stock = pd.read_pickle(name_stock_pickle, compression='bz2')  
        
            unpickle_stocks.append(unpickle_stock)

        return unpickle_stocks