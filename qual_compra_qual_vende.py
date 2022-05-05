import traceback

def calcula_qual_comprar_e_qual_vender(maior,menor, resultado):

    if resultado == 0:
        return  'Comprar {} e vender {} !!!'.format(maior, menor)
    elif resultado == 1:
        return 'Comprar {} e vender {} !!!'.format(menor, maior)
    else:
        return "Erro, entrada de dados inexistente"

if __name__ == '__main__':

    maior = input("Informe a ação maior: ")
    menor = input("Informe a ação menor: ")
    print() 
    try:
        resultado = int(input("Informe 0 se você espera que a diferença aumente, ou informe 1 se você espera que a diferença diminua: "))

        solucao = calcula_qual_comprar_e_qual_vender(maior,menor,resultado) 

        print(solucao)

    except Exception:
        print()
        print(traceback.format_exc()) 
        print("Aconteceu algum erro exception")
        print()

