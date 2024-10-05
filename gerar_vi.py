from numpy import arange, meshgrid
import os
from arquivos import escrever_arquivo

def perturbar_posicao (x0, y0, raio, delta):
    x = arange(x0-raio, x0+raio, delta)
    y = arange(y0-raio, y0+raio, delta)
    xv, yv = meshgrid(x,y)
    return xv, yv

def gerar_vi_perturbado (infos, corpo, raio, delta, nome_out):
    x0,y0 = infos['posicoes'][corpo][:2]
    xv, yv = perturbar_posicao(x0, y0, raio, delta)
    os.mkdir(f'./vi/{nome_out}')
    print(f'Serão gerados {len(xv)*len(yv)} arquivos...')
    for i in range(len(xv)):
        for j in range(len(yv)):
            nome_arq = f'./vi/{nome_out}/vi_{i:03d}_{j:03d}.txt'
            infos['posicoes'][corpo][0] = xv[i][j]
            infos['posicoes'][corpo][1] = yv[i][j]

            escrever_arquivo(infos, nome_arq)
    print("Pronto!")
    return xv, yv