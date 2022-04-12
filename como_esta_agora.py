
def dif_and_div_atual(maior, menor):

    dif = float(maior) - float(menor)
    div = float(maior)/float(menor)
    return  'Diferença: {:.2f} -  Divisão {:.4f} '.format(dif, div)

if __name__ == '__main__':
    print()
    maior = input("Informe a ação maior: ")
    print()
    menor = input("Informe a ação menor: ")
    print() 

    solucao = dif_and_div_atual(maior, menor) 

    print(solucao)
    print() 
