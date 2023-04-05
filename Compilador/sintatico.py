# importações
import Analisador_lexico  # importando a parte de análise léxica
import semantico  # importando a parte de análise semântica
import pandas as pd
import gramatica  # importando a gramática do compilador

# variáveis
arquivo = "FONTE.ALG"

# erros
erros = {
    'E0': 'Código não foi iniciado!',
    'E1': 'Código já foi iniciado!',
    'E2': 'Bloco de variáveis não foi iniciado!',
    'E3': 'Bloco de variáveis já foi iniciado!',
    'E4': 'Bloco de variáveis já foi terminado!',
    'E5': 'Bloco de variáveis não foi terminado!',
    'E6': 'Erro de sintaxe!',
    'E7': 'Fim de arquivo inesperado!',
    'E8': 'Não há nenhum \'se\' equivalente',  # (então)
    'E9': 'Não há nenhum \'se\' para ser fechado',  # (fimse)
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
cnj = ['inicio', 'varinicio', 'varfim', 'escreva', 'leia', 'se', 'entao',
       'fimse', 'fim', 'lit', 'int', 'real', ';', '(', ')', '"', 'facaAte', 'fimFaca']


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

    lista_aux = []

    for x in range(0, 75):  # total de linhas
        k = term.loc[x, token]  # procuro qual estado tem um shift
        if k[0] == 'S':
            lista_aux.append(x)

    x = max(lista_aux)

    while x not in pilha:
        lista_aux = lista_aux[:-1]
        x = max(lista_aux)

    if x in pilha:
        estado = pilha[-1]
        while estado != x:  # tira da pilha até achar algum estado que ajude o processamento
            pilha = pilha[:-1]
            estado = pilha[-1]
    else:
        pilha = pilha[:-1]
        pilha.append(x)

    return True

# ---------- EXECUÇÃO ----------


count = 0

# personalização do início
inicio(arquivo)

# pego os valores das tabelas shift reduce
nao_term = pd.read_csv('tabela_sintatica_NAO_terminais.csv', index_col=0)
term = pd.read_csv('tabela_sintatica_terminais.csv', index_col=0)

# abrir o arquivo
Analisador_lexico.OpenFile(arquivo)

# inicio o lexico
token, lexema, tipo = Analisador_lexico.gerencia()

# inicio a pilha
pilha = [0]
aux = ''

# inicio a variavel
erro_sintatico = False
erro_semantico = False

semantico.iniciar()

# inicio o processamento
while True:

    # pego o estado no topo da pilha
    s = pilha[-1]

    # pego a acao que deve ser feita de acordo com ele e o lexema lido
    acao = term.loc[s, token]

    # se for do tipo shift (empilhar)
    if acao[0] == 'S':
        pilha.append(int(acao.lstrip('S')))  # empilho o estado a ir
        semantico.pilha_semantica_aux.append([token, lexema, tipo])
        if lexema == 'facaAte':
            semantico.ocorrencias_facaAte += 1
        token, lexema, tipo = Analisador_lexico.gerencia()  # leio o proximo lexema

    # se for do tipo reduce (reduzir)
    elif acao[0] == 'R':
        prod = gramatica.gram[int(acao.lstrip('R'))]  # pego a produção da gramática referente
        lado_esq = prod.split(' -> ')[0]  # pego o lado esquerdo dividindo pelo ->
        qtd_smb = len(prod.split(' -> ')[1].split(' '))  # pego a qtd de simbolos do lado direito do ->
        pilha = pilha[:-qtd_smb]  # retiro da pilha a quantidade de simbolos do lado direito

        s = pilha[-1]  # pegando o estado ao topo da pilha
        pilha.append(int(nao_term.loc[s, lado_esq]))  # empilhando a transição GOTO[s, prod. esquerda]
        print('Topo da pilha: %#2.d. Produção: %#2.d) %s' % (s, int(acao.lstrip('R')), prod))

        for i in range(qtd_smb):
            aux = semantico.pilha_semantica_aux.pop()
            if aux is not None and aux[0] in ['id', 'int', 'real', 'lit', 'num', 'opm', 'opr', 'literal']:
                semantico.pilha_semantica.append(aux)

        semantico.pilha_semantica_aux.append(None)

        erro_semantico = semantico.avalia(prod)

        if erro_semantico:
            print(erro_semantico)
            count += 1
            continue

    # se for Accept
    elif acao == 'Acc':
        if not erro_sintatico:
            print("\n--- Código totalmente aceito! ---")
        else:
            print("\n--- Código terminado mas houveram erros. ---")
        break

    # se não for nada acima, então é um erro
    else:
        print("--- Erro Sintático %s --- " % (erros[acao]), end='')
        print("Linha: " + str(Analisador_lexico.linha), " Coluna: " + str(Analisador_lexico.coluna))
        # erro_sintatico = tratamento_erros()


# fecho o arquivo
Analisador_lexico.CloseFile()

# escrevo o arquivo C
if count == 0:
    semantico.validar()
