from os import listdir, mkdir
from ler import ler_dados_simulacao
import numpy as np

def metrica (infos, t):
    D = 0
    for i in range(infos['N']):
        corpo = infos['corpos'][i]
        D += np.dot(corpo['posicoes'][t],corpo['momentos'][t])
    return D

def metrica_parametrizada (t):
    m = -0.01316330664340204
    M =  0.01319129510054462
    return - 0.5 * (M-m) * np.sin(1.9 * np.pi * t) + 0.5 * (M+m)

def metrica_lista (diretorio:str, nome_out:str, h:float, qnt_em_qnt=10):
    # Captura os arquivos do diretorio
    arquivos = listdir(diretorio)

    # dir_out = f'metricas/{nome_out}'
    # mkdir(dir_out)

    string = ""

    # Le cada um e calcula as metricas
    for arquivo in arquivos:
        
        nome_split = arquivo.replace('.txt', '').split("_")
        xv, yv = nome_split[1:]

        infos = ler_dados_simulacao(f'{diretorio}/{arquivo}/data.csv', qnt_em_qnt)

        metricas = []
        param = []
        difs = []

        # Calcula a metrica para a trajetoria
        for t in range(len(infos['corpos'][0]['posicoes'])):
            medida = metrica(infos, t)
            metricas.append(medida)

            medida_param = metrica_parametrizada(t*h)
            param.append(medida_param)

            dif = np.linalg.norm(np.array(metricas) - np.array(param))
            difs.append(str(dif))

        # Agora salva
        string += f"{xv},{yv} / {','.join(difs)}\n"
    
    with open(f'metricas/{nome_out}.txt', 'w') as arq:
        arq.write(string)

def ler_metrica_lista (diretorio:str):    
    with open(diretorio, 'r') as arq:
        texto = arq.read().split('\n')[:-1]
        tamanho = int(np.sqrt(len(texto)))
        qntd_metricas = len(texto[0].split('/')[1].split(','))
        matrizes = [
            [
            [[] for _ in range(tamanho)]
            for i in range(tamanho)
            ] for j in range(qntd_metricas)
        ]
        for linha in texto:
            xvyv, met = linha.split('/')
            xv, yv = xvyv.split(',')
            for i, m in enumerate(met.split(',')):
                matrizes[i][int(xv)][int(yv)] = float(m)
    return matrizes


