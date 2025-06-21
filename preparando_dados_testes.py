# separa_valores.py
import csv

def separar_em_csv(input_path, antes_path, depois_path):
    with open(input_path, 'r') as f:
        tokens = f.read().split()

    # Lista dos valores antes e depois da vírgula
    antes = []
    depois = []
    for token in tokens:
        if ',' in token:
            a, d = token.split(',', 1)
            antes.append(a)
            depois.append(d)

    # Escreve antes.csv – todos valores separados por vírgula
    with open(antes_path, 'w', newline='') as fa:
        writer = csv.writer(fa)
        writer.writerow(antes)

    # Escreve depois.csv
    with open(depois_path, 'w', newline='') as fb:
        writer = csv.writer(fb)
        writer.writerow(depois)

if __name__ == '__main__':
    separar_em_csv('/home/sakod/Documentos/projetos/MSteroide_1/testosterona_ms.txt', 'mz_testosterona.csv', 'int_testosterona.csv')
