import os

# diretorio de pesquisa
diretorio = '/Users/dalton/Desktop/workspace/code/HERBIA/Feira-2024/Images/'

# criando arquivo de saida
f = open('DadosFeira2024.txt', 'a')

header = 'ID,Imagem,Produto,Valor,Desconto,Estoque'
f.write(header + '\n')

lista_diretorios = [f for f in os.listdir(diretorio) if os.path.isdir(os.path.join(diretorio, f))]
print('Total de', len(lista_diretorios), 'diretorios', lista_diretorios)

total = 0
seq = 0
for item in lista_diretorios:
    print('==> [', item, ']')
    path = diretorio + '/' + item
    arq = sorted(os.listdir(path))
    qtd = 0
    for i in range(0, len(arq)):
        total += 1
        qtd += 1
        seq += 1
        # renomeando arquivo trocando espaço em branco por hifen
        if os.path.basename(arq[i]).count(" ") != 0:
            old_name = diretorio + item + '/' + arq[i]
            new_name = diretorio + item + '/' + arq[i].replace(" ", "-")
            print('old_name', old_name, '---> new_name', new_name)
            os.rename(old_name, new_name)
        print(str(qtd), arq[i])
        # definindo o registro para escrever no arquivo
        numero = 'P' + str(seq).zfill(2)
        produto = arq[i][:-4].replace("-", " ")
        valor = '[20, 10, 0]'
        desconto = '5'
        estoque = '100'
        registro = numero + ',' + './Images/' + item + '/' + arq[i].replace(" ", "-") + ',' + produto + ',' + valor + ',' + desconto + ','+ estoque
        f.write(registro + '\n')

print('Total de arquivos:', total)
f.close()
