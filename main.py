from gerar_vi import gerar_vi_perturbado
from simulacao import rodar_lista_vi
from os import remove, mkdir
from metrica import metrica_lista, ler_metrica_lista
from plotar import plotar_heatmap
import numpy as np

info_lemniscata = {
    'integrador': 'verlet',
    'timestep':   '0.01',
    'potsoft':    '0.001',
    'passos':     '10',
    't0':         '0',
    'tf':         '50',
    'paralelo':   'F',
    'corretor':   'F',
    'corme':      '0.01',
    'cormnt':     '15',
    'colisoes':   'F',
    'colmd':      '0.1',
    'N':          '3',
    'G':          '1.0',
    'massas':     [1.0, 1.0, 1.0],
    'posicoes':   [
        [-0.97000436,  0.1930875299999999, 0.0],
        [0.0,         0.0,        0.0],
        [0.97000436, -0.24308753, 0.0]
    ],
    'momentos':    [
        [0.4662036850, 0.4323657300, 0],
        [-0.93240737,  -0.86473146,  0],
        [0.4662036850, 0.4323657300, 0]
    ]    
}

arquivo = 'testeeee'

xv, yv = gerar_vi_perturbado(info_lemniscata, 0, 0.5, 0.005, arquivo)

rodar_lista_vi(f'vi/{arquivo}', arquivo)

metrica_lista(f'./out/{arquivo}', arquivo, 1)

matrizes = ler_metrica_lista(f'./metricas/{arquivo}.txt')

mkdir(f'./plots/{arquivo}')

for i,m in enumerate(matrizes):
    plotar_heatmap(
        f'./plots/{arquivo}/heatmap_{i}',
        np.array(m),
        xv, 
        yv,
        interp='gaussian'
    )