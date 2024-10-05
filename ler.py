"""
Leitura de arquivos

Objetivos:
  Funcoes rapidas para ler arquivos diversos, como os de valores 
  iniciais e os de dados gerados por simulacoes atraves dos GFs.

Modificado:
  10 de julho de 2024

Autoria:
  oap
"""

__all__     = ["ler_valores_iniciais", "ler_dados_simulacao"]
__version__ = "20240710"
__author__  = "oap"

from numpy import array

def ler_linha (linha : str, numerico : bool = False, separador : str = ",")->list:
  """
  Dada uma string contendo uma linha de algum arquivo dos GFs, faz 
  a leitura e retorna o indice e o valor em uma lista.

  Isso eh util nas linhas que sao configuracoes, como por exemplo 
  a quantidade de corpos, o valor de G, o   modo, etc.

  Modificado
    09 de julho de 2024

  Parametros:
  -----------
  linha : str
    String com informacoes
  numerico : bool = False
    Se é uma linha totalmente numerica
  separador : str = ","
    No caso de ser uma linha totalmente numerica, eh o que separa
    os numeros

  Retorno
  -------
  Indice e valor ou array de numeros.
  """
  # Se for uma linha totalmente numerica
  if numerico:
    lista = list()
    for elemento in linha.split(","):
      try: lista.append(float(elemento))
      except: break
    return array(lista)

  indice, valor = linha.split()

  # se tiver aspas
  if '"' in valor: 
    valor = valor[1:-1] 

  # verifica se eh inteiro
  elif valor.isnumeric():
    valor = int(valor)

  # verifica se eh real
  else:
    try:
      valor = float(valor)
    except: 
      # se nao, pode ser booleano
      if valor.upper() in ["T", "F"]: 
        valor = (valor.upper() == "T")

  return indice, valor

def ler_valores_iniciais (arquivo_dir : str)->dict:
  """
  Para ler arquivos de valores iniciais.

  Parametros
  ----------
  arquivo_dir : str
    Diretorio do arquivo de valores iniciais.

  Retorno
  -------
  Dicionario com as informacoes do arquivo.
  """
  LINHA_CONFIGS_BASICAS = [1,9]
  LINHA_QNTD_CORPOS     = 23
  LINHA_CONSTANTE_G     = 24
  LINHA_INICIO_MASSAS   = 27
  LINHA_INICIO_POSICOES = 29
  LINHA_INICIO_MOMENTOS = 34

  with open(arquivo_dir, 'r') as arquivo:    
    # Quebra em linhas
    linhas = arquivo.read().split("\n")

    # Dicionario com as informacoes
    infos = dict()

    # Configuracoes basicas
    linhas_configs = linhas[LINHA_CONFIGS_BASICAS[0]:LINHA_CONFIGS_BASICAS[1]]
    for i,linha in enumerate(linhas_configs):
      indice, valor = ler_linha(linha)
      infos[indice] = valor

    # Quantidade de corpos e valor de G
    infos['N'] = ler_linha(linhas[LINHA_QNTD_CORPOS])[1]
    infos['G'] = ler_linha(linhas[LINHA_CONSTANTE_G])[1]

    # Massas
    infos['massas'] = list()
    for i in range(infos['N']):
      indice = LINHA_INICIO_MASSAS + i
      infos['massas'].append(float(linhas[indice]))

    # Posicoes
    infos['posicoes'] = list()
    for i in range(infos['N']):
      indice = LINHA_INICIO_POSICOES+infos['N']+i
      infos['posicoes'].append(ler_linha(linhas[indice], True))

    # Momentos lineares
    infos['momentos'] = list()
    for i in range(infos['N']):
      indice = LINHA_INICIO_MOMENTOS+infos['N']+i
      infos['momentos'].append(ler_linha(linhas[indice], True))
    
    # Agora gera os objetos de corpos
    infos['corpos'] = list()
    for i in range(infos['N']):
      corpo = {
        "massa": infos['massas'][i],
        "posicoes": [infos['posicoes'][i]],
        "momentos": [infos['momentos'][i]]
      }
      corpo['velocidade'] = [corpo['momentos'][0]/corpo['massa']]
      infos['corpos'].append(corpo)

    return infos

def ler_dados_simulacao (arquivo_dir : str, qnt_em_qnt : int = 1)->dict:
  """
  Para ler arquivos de dados de simulacao.

  Parametros
  ----------
  arquivo_dir : str
    Diretorio do arquivo.
  
  qnt_em_qnt : int = 1
    De quanto em quanto vai pegar os valores das posicoes e momentos.

  Retorno
  -------
  Dicionario com as informacoes do arquivo.
  """
  LINHA_TAMANHO_PASSO  = 0
  LINHA_CONSTANTE_G    = 1
  LINHA_MASSAS         = 2
  LINHA_INICIO_VALORES = 3

  with open(arquivo_dir, 'r') as arquivo:
    # Quebra em linhas
    linhas = arquivo.read().split("\n")

    # Dicionario com as informacoes
    infos = dict()

    # Tamanho do passo
    infos['h'] = ler_linha(linhas[LINHA_TAMANHO_PASSO], True)[0]

    # Valor de G
    infos["G"] = ler_linha(linhas[LINHA_CONSTANTE_G], True)[0]

    # Massas e quantidade de corpos
    infos["massas"] = ler_linha(linhas[LINHA_MASSAS], True)
    N = len(infos["massas"])
    infos['N'] = N

    # Linhas mistas
    infos["corpos"] = [
      {"massa": infos["massas"][corpo], "posicoes":list(), "momentos":list()} 
      for corpo in range(N)
      ]
    
    i = 0
    while True:
      try:
        # Leitura da linha
        linha_mista = ler_linha(linhas[LINHA_INICIO_VALORES+i], True)
        if len(linha_mista) == 0: break
        # Agora separa
        R = [linha_mista[0:N],      # X
             linha_mista[N:2*N],    # Y
             linha_mista[2*N:3*N]]  # Z
        P = [linha_mista[3*N:4*N],  # PX
             linha_mista[4*N:5*N],  # PY
             linha_mista[5*N:6*N]]  # PZ
        # Separacao por corpos
        R = list(zip(*R))
        P = list(zip(*P))
        for corpo in range(N):
          infos["corpos"][corpo]["posicoes"].append(array(R[corpo]))
          infos["corpos"][corpo]["momentos"].append(array(P[corpo]))
      except:
        break

      i += qnt_em_qnt

    return infos