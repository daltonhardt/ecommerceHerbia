import os

diretorio = '/Users/dalton/Desktop/workspace/code/HERBIA/Feira-2024/Images'

lista_diretorios = [f for f in os.listdir(diretorio) if os.path.isdir(os.path.join(diretorio, f))]
print('Total de', len(lista_diretorios), 'diretorios', lista_diretorios)

total = 0

for item in lista_diretorios:
    print('==> [', item, ']')
    path = diretorio + '/' + item
    arq = sorted(os.listdir(path))
    qtd = 0
    for i in range(0, len(arq)):
        total += 1
        qtd += 1
        print(str(qtd), arq[i])
print('Total de arquivos:', total)
