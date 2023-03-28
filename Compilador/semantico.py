import Analisador_lexico  # para modificar a tabela de símbolos

# novamente a gramática para eu identificar a produção
gram = {
    1: 'P\' -> P',
    2: 'P -> inicio V A',
    3: 'V -> varinicio LV',
    4: 'LV -> D LV',
    5: 'LV -> varfim ;',
    6: 'D -> TIPO L ;',
    7: 'L -> id , L',
    8: 'L -> id',
    9: 'TIPO -> int',
    10: 'TIPO -> real',
    11: 'TIPO -> lit',
    12: 'A -> ES A',
    13: 'ES -> leia id ;',
    14: 'ES -> escreva ARG ;',
    15: 'ARG -> literal',
    16: 'ARG -> num',
    17: 'ARG -> id',
    18: 'A -> CMD A',
    19: 'CMD -> id rcb LD ;',
    20: 'LD -> OPRD opm OPRD',
    21: 'LD -> OPRD',
    22: 'OPRD -> id',
    23: 'OPRD -> num',
    24: 'A -> COND A',
    25: 'COND -> CAB CP',
    26: 'CAB -> se ( EXP_R ) entao',
    27: 'EXP_R -> OPRD opr OPRD',
    28: 'CP -> ES CP',
    29: 'CP -> CMD CP',
    30: 'CP -> COND CP',
    31: 'CP -> fimse',
    32: 'A -> R A',
    33: 'R -> facaAte ( EXP_R ) CP_R',
    34: 'CP_R -> ES CP_R',
    35: 'CP_R -> CMD CP_R',
    36: 'CP_R -> COND CP_R',
    37: 'CP_R -> fimFaca',
    38: 'A -> fim',
}

tipo_var = {
    'literal': 'char',
    'inteiro': 'int',
    'real': 'double'
}

# pilha_semantica semântica
pilha_semantica = []
pilha_semantica_aux = []
cabecalho = []
corpo_temporarias = []
corpo = []
# nome do arquivo resultado
resultado = 'PROGRAMA.C'


def iniciar():

    cabecalho.append('#include<stdio.h>\n')
    cabecalho.append('#include<stdlib.h>\n')
    cabecalho.append('#include<stdbool.h>\n\n')
    cabecalho.append('typedef char lit[256];\n\n')
    cabecalho.append('int main(){\n\n')

    corpo_temporarias.append(' /*variáveis temporarias*/\n')

    corpo.append('\n\n /*variáveis*/\n')


def validar():
    escrever_arq(cabecalho)
    escrever_arq(corpo_temporarias)
    escrever_arq(corpo)


# variáveis para gerenciar os temporários
numTemp = 0
indent = 0

# conferir declaração de variável
def conferir_declaracao(valores):
    if valores[2] != '':
        return True
    else:
        return False


def escrever_arq(buffer):
    with open(resultado, 'a') as F:
        F.writelines(buffer)


# empilhar na pilha_semantica semantica
def empilhar(token, lexema, tipo):
    pilha_semantica.append([token, lexema, tipo])


# função geral do semantico
def avalia(prod):
    global pilha_semantica, numTemp, indent

    indentacao = ' '
    erro = False

    # começo a testar as produções
    if prod == gram[5]:   # LV -> varfim
        corpo.append('\n'*3)

    elif prod == gram[6]:   # D -> TIPO L
        i = -1
        while pilha_semantica[i][2] not in ['inteiro', 'real', 'literal']:
            i -= 1
        tipo_verifica = pilha_semantica[i][2]
        i = -1
        while pilha_semantica[i][0] == 'id':
            if Analisador_lexico.tabela_simbolos[pilha_semantica[i][1]][2] != '':
                break
            Analisador_lexico.tabela_simbolos[pilha_semantica[i][1]][2] = tipo_verifica
            indent += 1
            indentacao = ' ' * indent
            texto = str(indentacao) + tipo_var[tipo_verifica] + ' ' + pilha_semantica[i][1] + ';\n'
            indent -= 1
            corpo.append(texto)
            i -= 1

    elif prod == gram[7]:  # L -> id, L
        i = -1
        while pilha_semantica[i][2] not in ['inteiro', 'real', 'literal']:
            if conferir_declaracao(pilha_semantica[i]):
                print("Variavel já foi declarada na linha: " + str(Analisador_lexico.linha),
                      " coluna : " + str(Analisador_lexico.coluna))
                erro = True
            i -= 1

    elif prod == gram[8]:  # L -> id
        aux = pilha_semantica.pop()
        if conferir_declaracao(aux):
            print("Variavel já foi declarada na linha: " + str(Analisador_lexico.linha),
                  " coluna : " + str(Analisador_lexico.coluna))
            erro = True
        else:
            pilha_semantica.append(aux)

    elif prod == gram[13]:  # ES -> leia id
        if conferir_declaracao(pilha_semantica[-1]):
            if pilha_semantica[-1][2] == 'literal':
                indent += 1
                indentacao = ' ' * indent
                corpo.append(str(indentacao) + 'scanf("%s", &' + pilha_semantica[-1][1]+');\n')
                indent -= 1
            elif pilha_semantica[-1][2] == 'inteiro':
                indent += 1
                indentacao = ' ' * indent
                corpo.append(str(indentacao) + 'scanf("%d",&' + pilha_semantica[-1][1]+');\n')
                indent -= 1
            elif pilha_semantica[-1][2] == 'real':
                indent += 1
                indentacao = ' ' * indent
                corpo.append(str(indentacao) + 'scanf("%f",&' + pilha_semantica[-1][1]+');\n')
                indent -= 1
        else:
            print("Variável não declarada linha:"+str(Analisador_lexico.linha),
                  "coluna : " + str(Analisador_lexico.coluna))
            erro = True

    elif prod == gram[14]:  # ES -> escreva ARG
        argumento = pilha_semantica[-1][2]
        if argumento == 'literal':
            indent += 1
            indentacao = ' ' * indent
            corpo.append(str(indentacao) + 'printf("%s",' + pilha_semantica[-1][1] + ');\n')
            indent -= 1
        elif argumento == 'inteiro':
            indent += 1
            indentacao = ' ' * indent
            corpo.append(str(indentacao) + 'printf("%d",' + pilha_semantica[-1][1] + ');\n')
            indent -= 1
        elif argumento == 'real':
            indent += 1
            indentacao = ' ' * indent
            corpo.append(str(indentacao) + 'printf("%f"' + pilha_semantica[-1][1] + ');\n')
            indent -= 1
        else:
            print("Variável não declarada linha:"+str(Analisador_lexico.linha),
                  "coluna : " + str(Analisador_lexico.coluna))
            erro = True

    elif prod == gram[15]:  # ARG -> literal
        pilha_semantica[-1][2] = 'literal'

    elif prod == gram[16]:   # ARG -> num
        aux = pilha_semantica[-1]
        if '.' in aux[1] or 'e' in aux[1]:
            pilha_semantica[-1][2] = 'real'
        else:
            pilha_semantica[-1][2] = 'inteiro'

    elif prod == gram[17]:  # ARG -> id
        if not conferir_declaracao(pilha_semantica[-1]):
            print("Variável não declarada linha:"+str(Analisador_lexico.linha),
                  "coluna : " + str(Analisador_lexico.coluna))
            erro = True

    elif prod == gram[19]:  # CMD -> id rcb LD
        x1 = Analisador_lexico.tabela_simbolos[pilha_semantica[-1][1]][2]
        x2 = pilha_semantica[-2][2]
        flag = True
        if x2 == '':
            flag = False
            x2 = pilha_semantica[-3][2]

        if x1 != x2:
            print("Tipos incompatíveis na atribuição linha : " + str(Analisador_lexico.linha))
            erro = True

        indent += 1
        indentacao = ' ' * indent
        text = str(indentacao) + str(pilha_semantica[-1][1]) + '=' + str(pilha_semantica[-2][1]) + ';\n'
        indent -= 1

        if flag:
            corpo.append(text)

    elif prod == gram[20]: 	# LD -> OPRD opm OPRD
        x1 = pilha_semantica[-3][2]
        x2 = pilha_semantica[-2][2]

        if x1 != x2:
            print("Erro semântico linha : " + str(Analisador_lexico.linha))
            erro = True

        indentacao = ' ' * 1
        text0 = str(indentacao) + tipo_var[x1] + ' T' + str(numTemp) + ';\n'

        indent += 1
        indentacao = ' ' * indent
        text = str(indentacao) + 'T' + str(numTemp) + ' = ' + str(pilha_semantica[-3][1])\
               + '' + str(pilha_semantica[-1][1]) + \
               '' + str(pilha_semantica[-2][1]) + ';\n'
        indent -= 1

        corpo_temporarias.append(text0)
        corpo.append(text)
        indent += 1
        indentacao = ' ' * indent
        text2 = str(indentacao) + (pilha_semantica[-3][1]) + ' = ' + 'T' + str(numTemp) + ';\n'
        indent -= 1
        corpo.append(text2)
        numTemp += 1

    elif prod == gram[23]:  # OPRD -> num
        aux = pilha_semantica[-1]
        if '.' in aux[1] or 'e' in aux[1]:
            pilha_semantica[-1][2] = 'real'
        else:
            pilha_semantica[-1][2] = 'inteiro'

    elif prod == gram[26]:  # CAB -> se (EXP_R) entao
        x1 = pilha_semantica.pop()
        x2 = pilha_semantica.pop()
        x3 = pilha_semantica.pop()
        exp_r = str(x3[1]) + ' ' + str(x1[1]) + ' ' + str(x2[1])
        indentacao = ' ' * 1
        text0 = str(indentacao) + 'bool' + ' T' + str(numTemp) + ';\n'

        indent += 1
        indentacao = ' ' * indent
        text = str(indentacao) + 'T' + str(numTemp) + ' = ' + str(exp_r) + ';\n'
        indent -= 1

        indent += 1
        indentacao = ' ' * indent
        text2 = str(indentacao) + "if (" + 'T' + str(numTemp) + ') {\n'
        indent += 1
        corpo_temporarias.append(text0)
        corpo.append(text)
        corpo.append(text2)
        numTemp += 1

    elif prod == gram[31] or prod == gram[37] or prod == gram[38]:
        indent -= 1
        indentacao = ' ' * indent
        corpo.append(str(indentacao) + '}\n')
        indent -= 1

    return erro
