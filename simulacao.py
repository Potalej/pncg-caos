from os import listdir, mkdir
from subprocess import DEVNULL, STDOUT, check_call
from shutil import move

def rodar_vi (arquivo:str):
    check_call(f'gravidade.exe -vi {arquivo}', stdout=DEVNULL, stderr=STDOUT)

def rodar_lista_vi (diretorio:str, out_dir:str):
    arquivos = listdir(diretorio)
    mkdir(f'./out/{out_dir}')
    for i,arquivo in enumerate(arquivos):
        # Nome do novo arquivo
        nome_split = arquivo.replace('.txt', '').split('_')[:]
        xv, yv = nome_split[1:]

        # Roda simulacao
        rodar_vi(f"{diretorio}/{arquivo}")
        
        # Move para outra pasta
        arquivo_sim = listdir('./out/data')[-1]
        move(f'./out/data/{arquivo_sim}', f'./out/{out_dir}/sim_{xv}_{yv}')
        
        print(f'{i}/{len(arquivos)}')