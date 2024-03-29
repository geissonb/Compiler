source = None
linha = 0
coluna = 0
tipo = ' '

dfa = {
    0: {'D': 1, '"': 8, 'L': 10, 'E': 10, 'e': 10, '{': 11, 'eof': 13, '<': 14, '>': 15, '=': 17, '+': 19, '-': 19,
        '*': 19, '/': 19, '(': 20, ')': 21, ';': 22, ',': 23},
    1: {'D': 1, 'E': 4, 'e': 4, '.': 2},
    2: {'D': 3},
    3: {'D': 3},
    4: {'+': 6, '-': 6, 'D': 5},
    5: {'D': 5},
    6: {'D': 7},
    7: {'D': 7},
    8: {'"': 9},
    10: {'L': 10, 'E': 10, 'e': 10, 'D': 10, '_': 10},
    11: {'}': 12},
    14: {'=': 16, '>': 16, '-': 18},
    15: {'=': 16},
}

finais = {
    1: 'num',
    3: 'num',
    5: 'num',
    7: 'num',
    9: 'literal',
    10: 'id',
    12: 'comentario',
    13: 'eof',
    14: 'opr',
    15: 'opr',
    16: 'opr',
    17: 'opr',
    18: 'rcb',
    19: 'opm',
    20: 'ab_p',
    21: 'fc_p',
    22: 'pt_v',
    23: 'vir'
}

# descrição de erros de acordo com o estado em que parou
erros = {
    0: 'Caractere Inválido!',
    2: 'Necessita de numero após o ponto.',
    4: 'Necessita de um sinal(+ ou -) após o exponencial ou dígito.',
    6: 'Necessita de um número após o sinal(+ ou -)',
    8: 'Falta fechar aspas!',
    11: 'Falta fechar chaves!'
}

# a tabela de símbolos é um dicionário de listas
# lexema = palavra, token = classe, tipo não está sendo utilizado
tabela_simbolos = {
    #  Lexema  	     Lexema        Token     Tipo
    'inicio': ['inicio', 'inicio', ''],
    'varinicio': ['varinicio', 'varinicio', ''],
    'varfim': ['varfim', 'varfim', ''],
    'escreva': ['escreva', 'escreva', ''],
    'leia': ['leia', 'leia', ''],
    'se': ['se', 'se', ''],
    'entao': ['entao', 'entao', ''],
    'fimse': ['fimse', 'fimse', ''],
    'fim': ['fim', 'fim', ''],
    'lit': ['lit', 'lit', 'literal'],
    'int': ['int', 'int', 'inteiro'],
    'real': ['real', 'real', 'real'],
    'facaAte': ['facaAte', 'facaAte', ''],
    'fimFaca': ['fimFaca', 'fimFaca', '']
}


# variáveis
global erro, Lista_tokens, TOKENS
erro = 1
TOKENS = {}


def open_file(name):
    global source
    source = open(name)


def close_file():
    source.close()


def verifica_caractere(s):

    car = str(s)

    if car == 'E' or car == 'e':
        return s

    elif car.isalpha() is True:  # verifica se é letra
        return "L"

    elif car.isdigit() is True:  # verifica se é dígito
        return "D"

    else:
        return s


def error(text, estado, linha_atual, coluna_atual):
    _linha = str(linha_atual)
    _coluna = str(coluna_atual)
    print(text + ' - ' + erros[estado] + " linha " + _linha + " coluna " + _coluna)


def processar_erro(n_erros, buffer_atual):
    global erro, check, ant, checkpoint, flag, b

    if check:
        source.seek(ant, 0)

    quantidade_erros = str(n_erros)
    string_erro = "Erro " + quantidade_erros
    TOKENS[buffer_atual] = [string_erro, buffer_atual, '']
    erro += 1
    if checkpoint:
        source.read(1)
    flag = True
    return TOKENS[buffer_atual]


def processar_dados(estado_atual, buffer_atual):
    if estado_atual in finais:
        if estado_atual == 10:
            if buffer_atual in tabela_simbolos:
                return tabela_simbolos[buffer_atual]
            else:
                tabela_simbolos[buffer_atual] = [finais[estado_atual], buffer_atual, '']
                return tabela_simbolos[buffer_atual]
        elif estado_atual != 10:
            if buffer_atual in TOKENS:
                return TOKENS[buffer_atual]
            else:
                TOKENS[buffer_atual] = [finais[estado_atual], buffer_atual, '']
                return TOKENS[buffer_atual]
    else:
        aux = processar_erro(qtd_erro, buffer_atual)
        return aux


def scanner():
    global atual, proximo, buffer, ant, linha, coluna, flag, erro, check, checkpoint, qtd_erro, caractere, tipo

    atual = 0
    buffer = ''
    flag = False
    qtd_erro = erro
    check = False
    checkpoint = False

    while True:
        encontrado = False

        ant = source.tell()
        temp = source.read(1)
        coluna += 1

        if temp == '':
            if atual == 0:
                atual = 13

            elif atual == 8 or atual == 11:

                check = True
                t = processar_erro(qtd_erro, buffer)
                return t

            if atual in finais:
                TOKENS['eof'] = ['eof', 'eof', '']
                return TOKENS['eof']

        else:
            caractere = verifica_caractere(temp)

            if atual in dfa:
                for x in dfa[atual]:
                    if x == caractere:
                        encontrado = True
                        proximo = (dfa[atual])[x]
                        break

            if atual == 8 or atual == 11:
                if caractere == '\n':
                    linha += 1
                    coluna = 0
                encontrado = True

            if encontrado:
                buffer += temp
                atual = proximo

            elif caractere in [' ', '\n', '\t']:
                if atual != 0:
                    t = processar_dados(atual, buffer)
                    return t

            else:
                source.seek(ant, 0)
                coluna -= 1
                if atual != 0:
                    t = processar_dados(atual, buffer)
                    return t

                else:
                    checkpoint = True
                    t = processar_erro(qtd_erro, caractere)
                    return t


# ----------------------EXECUÇÃO------------------------------------------


def gerencia():

    s = scanner()

    global linha, coluna, tipo

    if flag:
        error(b, atual, linha, coluna)

    if caractere == '\n':
        linha += 1
        coluna = 0

    return s
