# Programa gerador de dados em JavaScript
# Função: gerar o arquivo de dados que é usado no sistema de Vendas
# Input: arquivo tipo .txt que contém os produtos que serão vendidos
#        incluindo:  ID,arquivo da Imagem,nome do Produto,Valor,quantidade em Estoque 
# Output: arquivo tipo .js com as instrução em javaScript
# Autor:  Dalton Hardt   Mar-2024

# diretorio de pesquisa
diretorio = './Images'

# abrindo o arquivo de Entrada
fileInput = open('DadosFeira2024.txt', 'r')

# criando o arquivo de Saida
fileOutput = open('src/data.js', 'a')

# gravando a primeira linha
fileOutput.write('let shopItemsData = [' + '\n')

# gravando as demais linhas lendo do arquivo de entrada
Lines = fileInput.readlines()
i = 0
for line in Lines:
    if i == 0:
        i += 1
        continue
    else:
        reg = line.split(",")
        print('reg: ', reg)
        registro = '\t{\n' + '\t\tid:"' + reg[0] + '",\n' + '\t\tname:"' + reg[2] + '",\n' + '\t\tprice:' + reg[3] + \
                    ',' + reg[4] + ',' + reg[5] + ',\n' + '\t\tmaxItemDiscount:' + reg[6] + ',\n' + \
                    '\t\titemStock:' + reg[7][:-1] + ',\n' + '\t\timg:"' + reg[1].replace(" ", "-") + '" \n\t},\n'
        # print(registro)
        fileOutput.write(registro)

fileOutput.write('];\n')
fileInput.close()
fileOutput.close()
