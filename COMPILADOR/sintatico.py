# importações
from pandas.core.indexes.base import Index
import Analisador_lexico
import semantico
import pandas as pd

# variáveis
arquivo = "FONTE.ALG"

# gramática
gram = {
  '1' : 'P\' -> P',
  '2' : 'P -> inicio V A',
  '3' : 'V -> varinicio LV',
  '4' : 'LV -> D LV',
  '5' : 'LV -> varfim ;',
  '6' : 'D -> TIPO L ;',
  '7' : 'L -> id , L',
  '8' : 'L -> id',
  '9' : 'TIPO -> int',
  '10' : 'TIPO -> real',
  '11' : 'TIPO -> lit',
  '12': 'A -> ES A',
  '13': 'ES -> leia id ;',
  '14': 'ES -> escreva ARG ;',
  '15': 'ARG -> literal',
  '16': 'ARG -> num',
  '17': 'ARG -> id',
  '18': 'A -> CMD A',
  '19': 'CMD -> id rcb LD ;',
  '20': 'LD -> OPRD opm OPRD',
  '21': 'LD -> OPRD',
  '22': 'OPRD -> id',
  '23': 'OPRD -> num',
  '24': 'A -> COND A',
  '25': 'COND -> CAB CP',
  '26': 'CAB -> se ( EXP_R ) entao',
  '27': 'EXP_R -> OPRD opr OPRD',
  '28': 'CP -> ES CP',
  '29': 'CP -> CMD CP',
  '30': 'CP -> COND CP',
  '31': 'CP -> fimse',
  '32': 'A -> R A',
  '33': 'R -> facaAte ( EXP_R ) CP_R',
  '34': 'CP_R -> ES CP_R',
  '35': 'CP_R -> CMD CP_R',
  '36': 'CP_R -> COND CP_R',
	'37': 'CP_R -> fimFaca',
  '38': 'A -> fim',
}

# erros
erros = {
  'E0' : 'Código não foi iniciado!',
  'E1' : 'Código já foi iniciado!',
  'E2' : 'Bloco de variáveis não foi iniciado!',
  'E3' : 'Bloco de variáveis já foi iniciado!',
  'E4' : 'Bloco de variáveis já foi terminado!',
  'E5' : 'Bloco de variáveis não foi terminado!',
  'E6' : 'Erro de sintaxe!',
  'E7' : 'Fim de arquivo inesperado!',
  'E8' : 'Não há nenhum \'se\' equivalente', # (então)
  'E9' : 'Não há nenhum \'se\' para ser fechado', # (fimse)
  'E10': 'Falta o tipo da variável',
  'E11': 'É esperado um \';\'!',
  'E12': 'É esperado um identificador',
  'E13': 'Código já foi terminado',
  'E14': 'É esperada alguma operação ou \';\'!',
  'E15': 'É esperado um \'então\'',
  'E16': 'É esperado um operador relacional!',
  'E17': 'É esperado um \'(\'!',
  'E18': 'Não há nenhum \'facaAte\' equivalente',
  'E19': 'Não há nenhum \'facaAte\' para ser fechado'
}

# conjunto de sincronização
cnj = ['inicio', 'varinicio', 'varfim', 'escreva', 'leia', 'se', 'entao', 'fimse', 'fim', 'lit', 'int', 'real', ';', '(', ')', '"','facaAte','fimFaca']


# função de frescura pra personalizar o inicio XD
def inicio(nome):
  print("   ---- Analisador Sintático ----     ")
  print(" ---- Utilizando o Modo Pânico ----   ")
  print("--------------------------------------")
  print("- Arquivo de entrada: %s\n" % nome)


# função para implementar o modo pânico para tratar erros
def tratamento_erros():
  global token, lexema, tipo, pilha

  # procuro a proxima entrada que possa me estabelecer
  while token not in cnj:
    token, lexema, tipo = Analisador_lexico.gerencia()

  aux = []

  for x in range (0,75): # total de linhas
    k = term.loc[x, token] # procuro qual estado tem um shift
    if k[0] == 'S':
      aux.append(x)

  x = max(aux)
  
  while x not in pilha:
      aux = aux[:-1]
      x = max(aux)

  if x in pilha:
    estado = pilha[-1]
    while estado != x: # tira da pilha até achar algum estado que ajude o processamento
      pilha = pilha[:-1]
      estado = pilha[-1]
  else:
    pilha = pilha[:-1]
    pilha.append(x)

  return True

# ---------- EXECUÇÃO ----------

# personalização do início
inicio(arquivo)

# pego os valores das tabelas shift reduce
nao_term = pd.read_csv('tabela_sintatica_NAO_terminais.csv', index_col = 0)
term = pd.read_csv('tabela_sintatica_terminais.csv', index_col = 0)

# abrir o arquivo
Analisador_lexico.OpenFile(arquivo)

# inicio o lexico
token, lexema, tipo = Analisador_lexico.gerencia()

# inicio a pilha
pilha = []
pilha.append(0)
aux = ''

# inicio a variavel
erro = False

semantico.iniciar()

# inicio o processamento
while True:

  #print(pilha)

  # pego o estado no topo da pilha
  s = pilha[-1]

  # pego a acao que deve ser feita de acordo com ele e o lexema lido
  acao = term.loc[s, token] 

  # se for do tipo shift (empilhar)
  if acao[0] == 'S':
    pilha.append(int(acao.lstrip('S'))) # empilho o estado a ir
    semantico.pilha_semantica_aux.append([token,lexema,tipo])
    token, lexema, tipo = Analisador_lexico.gerencia() # leio o proximo lexema
    

  # se for do tipo reduce (reduzir)
  elif acao[0] == 'R':
    prod = gram[acao.lstrip('R')] # pego a produção da gramática referente
    lado_esq = prod.split(' -> ')[0] # pego o lado esquerdo dividindo pelo ->
    qtd_smb = len(prod.split(' -> ')[1].split(' ')) # pego a qtd de simbolos do lado direito do ->
    pilha = pilha[:-qtd_smb] # retiro da pilha a quantidade de simbolos do lado direito

    s = pilha[-1] # pegando o estado ao topo da pilha
    pilha.append(int(nao_term.loc[s, lado_esq])) # empilhando a transição GOTO[s, prod. esquerda]
    print('Topo da pilha: %#2.d. Produção: %#2.d) %s' % (s, int(acao.lstrip('R')), prod))
		
    for i in range(qtd_smb):
      aux = semantico.pilha_semantica_aux.pop()
      if aux is not None and aux[0] in ['id','int','real','lit','num','opm','opr','literal']:
        semantico.pilha_semantica.append(aux)

    semantico.pilha_semantica_aux.append(None)

    erro = semantico.avalia(prod,qtd_smb)

    if erro:
	    print(erro)
	    continue
		
  # se for Accept
  elif acao == 'Acc':
    if not erro:
      print("\n--- Código totalmente aceito! ---")
    else:
      print("\n--- Código terminado mas houveram erros. ---")
    break

  # se não for nada acima, então é um erro
  else:
    print("--- Erro Sintático %s --- " % (erros[acao]),end='')
    print("Linha: " + str(Analisador_lexico.linha)," Coluna: " + str(Analisador_lexico.coluna))
    #erro = tratamento_erros()

# fecho o arquivo
Analisador_lexico.CloseFile()


if not erro:
  semantico.escreverarq()

