from re import I
import traceback
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

        try:

            n = 0
            for write_element in write_list:

                name_stock_pickle = self.folder_names[0]+ self.stocks_name[n] + self.type_names[0]
                name_stock_csv = self.folder_names[1]+ self.stocks_name[n] + self.type_names[1]

                if exists(name_stock_pickle):
                    
                    # Pega o arquivo pickle salvo
                    unpickle_stock = pd.read_pickle(name_stock_pickle, compression='bz2')

                    # Numero de linhas do dataframe
                    num_linhas = unpickle_stock.shape[0]

                    # Defini que até onde o sort será realizado
                    num_linhas =  11520 if num_linhas > 11520 else num_linhas 

                    # Separa em dataframe antes de depois do num_linhas
                    unpickle_stock_part_1 = unpickle_stock.iloc[:-num_linhas, :]
                    unpickle_stock_part_2 = unpickle_stock.iloc[-num_linhas:, :]

                    # Concatena a parte 2 com os novos dados
                    unpickle_stock_part_2 = pd.concat([unpickle_stock_part_2, write_element])

                    # Realiza a ordenação do dataframe concatenado
                    unpickle_stock_part_2 = unpickle_stock_part_2.sort_index()

                    # Traz a coluna datetimeindex como coluna normal
                    unpickle_stock_part_2.reset_index(inplace=True)

                    # Apaga as linhas duplicadas
                    unpickle_stock_part_2 = unpickle_stock_part_2.drop_duplicates()

                    # Defini a coluna datetime novamente como datetimeindex
                    unpickle_stock_part_2 = unpickle_stock_part_2.set_index(['Datetime'])

                    # Junta a parte 1 com a parte 2
                    unpickle_stock_full = pd.concat([unpickle_stock_part_1,unpickle_stock_part_2])

                    # Salva os dados
                    unpickle_stock_full.to_pickle(name_stock_pickle, compression='bz2')
                    unpickle_stock_full.to_csv(name_stock_csv)

                else:

                    write_element.to_pickle(name_stock_pickle, compression='bz2')
                    write_element.to_csv(name_stock_csv )
                    
                n += 1

            print("Gravação foi um sucesso !!!")

        except Exception:
            print(traceback.format_exc()) 
            print()
            print("Aconteceu um erro na gravação.")

    def reading_list(self, read_stocks):

        unpickle_stocks = []

        n = 0
        for read_stock in read_stocks:

            name_stock_pickle = self.folder_names[0] + read_stock + self.type_names[0]

            unpickle_stock = pd.read_pickle(name_stock_pickle, compression='bz2')  

            # Traz a coluna datetimeindex como coluna normal
            unpickle_stock.reset_index(inplace=True)
        
            unpickle_stocks.append(unpickle_stock)

        return unpickle_stocks
