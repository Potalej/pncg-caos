def escrever_arquivo (info:dict, arquivo:str):
    string = "! Configs\n"
    string += "modo vi\n"
    string += 'nome "teste"\n'
    string += f"integrador {info['integrador']}\n"
    string += f"timestep {info['timestep']}\n"
    string += f"potsoft {info['potsoft']}\n"
    string += f"passos {info['passos']}\n"
    string += f"t0 {info['t0']}\n"
    string += f"tf {info['tf']}\n"
    string += f"\n"
    string += f"! Usar paralelisacao nas forcas\n"
    string += f"paralelo {info['paralelo']}\n"
    string += f"\n"
    string += f"! Opcoes do corretor\n"
    string += f"corretor {info['corretor']}\n"
    string += f"corme {info['corme']}\n"
    string += f"cormnt {info['cormnt']}\n"
    string += f"\n"
    string += f"! Opcoes de colisao\n"
    string += f"colisoes {info['colisoes']}\n"
    string += f"colmd {info['colmd']}\n"
    string += f"\n"
    string += f"! Valores do problema\n"
    string += f"N {info['N']}\n"
    string += f"G {info['G']}\n"
    string += f"\n"
    
    string += f"! Massas\n"
    for m in info['massas']:
        string += f"{m}\n"
    
    string += f"\n"
    string += f"! Posicoes\n"
    for corpo in info['posicoes']:
        string += f"{corpo[0]}, {corpo[1]}, {corpo[2]}\n"

    string += f"\n"
    string += f"! Momentos\n"
    for corpo in info['momentos']:
        string += f"{corpo[0]}, {corpo[1]}, {corpo[2]}\n"

    with open(arquivo, 'w') as arq:
        arq.write(string)