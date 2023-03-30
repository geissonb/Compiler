import Analisador_lexico  # para modificar a tabela de símbolos
import gramatica  # importando a gramática do compilador

tipo_var = {
    'literal': 'lit',
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

    corpo_temporarias.append('    /*variáveis temporarias*/\n')

    corpo.append('\n\n    /*variáveis*/\n')


def validar():
    escrever_arq(cabecalho)
    escrever_arq(corpo_temporarias)
    escrever_arq(corpo)


def indentar(numero_indentacao, texto):
    numero_indentacao += 4
    indentacao = ' ' * numero_indentacao
    texto = str(indentacao) + texto
    numero_indentacao -= 4

    return texto


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

    erro = False

    # começo a testar as produções
    if prod == gramatica.gram[5]:   # LV -> varfim
        corpo.append('\n'*3)

    elif prod == gramatica.gram[6]:   # D -> TIPO L
        i = -1
        while pilha_semantica[i][2] not in ['inteiro', 'real', 'literal']:
            i -= 1
        tipo_verifica = pilha_semantica[i][2]
        i = -1
        while pilha_semantica[i][0] == 'id':
            if Analisador_lexico.tabela_simbolos[pilha_semantica[i][1]][2] != '':
                break
            Analisador_lexico.tabela_simbolos[pilha_semantica[i][1]][2] = tipo_verifica
            texto = tipo_var[tipo_verifica] + ' ' + pilha_semantica[i][1] + ';\n'
            texto = indentar(indent, texto)
            corpo.append(texto)
            i -= 1

    elif prod == gramatica.gram[7]:  # L -> id, L
        i = -1
        while pilha_semantica[i][2] not in ['inteiro', 'real', 'literal']:
            if conferir_declaracao(pilha_semantica[i]):
                print("Variavel já foi declarada na linha: " + str(Analisador_lexico.linha),
                      " coluna : " + str(Analisador_lexico.coluna))
                erro = True
            i -= 1

    elif prod == gramatica.gram[8]:  # L -> id
        aux = pilha_semantica.pop()
        if conferir_declaracao(aux):
            print("Variavel já foi declarada na linha: " + str(Analisador_lexico.linha),
                  " coluna : " + str(Analisador_lexico.coluna))
            erro = True
        else:
            pilha_semantica.append(aux)

    elif prod == gramatica.gram[13]:  # ES -> leia id
        if conferir_declaracao(pilha_semantica[-1]):
            if pilha_semantica[-1][2] == 'literal':
                texto = 'scanf("%s", &' + pilha_semantica[-1][1]+');\n'
                texto = indentar(indent, texto)
                corpo.append(texto)
            elif pilha_semantica[-1][2] == 'inteiro':
                texto = 'scanf("%d",&' + pilha_semantica[-1][1]+');\n'
                texto = indentar(indent, texto)
                corpo.append(texto)
            elif pilha_semantica[-1][2] == 'real':
                texto = 'scanf("%f",&' + pilha_semantica[-1][1]+');\n'
                texto = indentar(indent, texto)
                corpo.append(texto)
        else:
            print("Variável não declarada linha:"+str(Analisador_lexico.linha),
                  "coluna : " + str(Analisador_lexico.coluna))
            erro = True

    elif prod == gramatica.gram[14]:  # ES -> escreva ARG
        argumento = pilha_semantica[-1][2]
        if argumento == 'literal':
            texto = 'printf("%s",' + pilha_semantica[-1][1] + ');\n'
            texto = indentar(indent, texto)
            corpo.append(texto)
        elif argumento == 'inteiro':
            texto = 'printf("%d",' + pilha_semantica[-1][1] + ');\n'
            texto = indentar(indent, texto)
            corpo.append(texto)
        elif argumento == 'real':
            texto = 'printf("%f",' + pilha_semantica[-1][1] + ');\n'
            texto = indentar(indent, texto)
            corpo.append(texto)
        else:
            print("Variável não declarada linha:"+str(Analisador_lexico.linha),
                  "coluna : " + str(Analisador_lexico.coluna))
            erro = True

    elif prod == gramatica.gram[15]:  # ARG -> literal
        pilha_semantica[-1][2] = 'literal'

    elif prod == gramatica.gram[16]:   # ARG -> num
        aux = pilha_semantica[-1]
        if '.' in aux[1] or 'e' in aux[1]:
            pilha_semantica[-1][2] = 'real'
        else:
            pilha_semantica[-1][2] = 'inteiro'

    elif prod == gramatica.gram[17]:  # ARG -> id
        if not conferir_declaracao(pilha_semantica[-1]):
            print("Variável não declarada linha:"+str(Analisador_lexico.linha),
                  "coluna : " + str(Analisador_lexico.coluna))
            erro = True

    elif prod == gramatica.gram[19]:  # CMD -> id rcb LD
        x1 = Analisador_lexico.tabela_simbolos[pilha_semantica[-1][1]][2]
        x2 = pilha_semantica[-2][2]
        flag = True
        if x2 == '':
            flag = False
            x2 = pilha_semantica[-3][2]

        if x1 != x2:
            print("Tipos incompatíveis na atribuição linha : " + str(Analisador_lexico.linha))
            erro = True

        text = str(pilha_semantica[-1][1]) + '=' + str(pilha_semantica[-2][1]) + ';\n'
        text = indentar(indent, text)

        if flag:
            corpo.append(text)

    elif prod == gramatica.gram[20]: 	# LD -> OPRD opm OPRD
        x1 = pilha_semantica[-3][2]
        x2 = pilha_semantica[-2][2]

        if x1 != x2:
            print("Erro semântico linha : " + str(Analisador_lexico.linha))
            erro = True

        text0 = tipo_var[x1] + ' T' + str(numTemp) + ';\n'
        text0 = indentar(indent, text0)

        text = 'T' + str(numTemp) + ' = ' + str(pilha_semantica[-3][1])\
               + '' + str(pilha_semantica[-1][1]) + \
               '' + str(pilha_semantica[-2][1]) + ';\n'
        text = indentar(indent, text)

        corpo_temporarias.append(text0)
        corpo.append(text)

        text2 = (pilha_semantica[-3][1]) + ' = ' + 'T' + str(numTemp) + ';\n'
        text2 = indentar(indent, text2)

        corpo.append(text2)
        numTemp += 1

    elif prod == gramatica.gram[23]:  # OPRD -> num
        aux = pilha_semantica[-1]
        if '.' in aux[1] or 'e' in aux[1]:
            pilha_semantica[-1][2] = 'real'
        else:
            pilha_semantica[-1][2] = 'inteiro'

    elif prod == gramatica.gram[26]:  # CAB -> se (EXP_R) entao
        x1 = pilha_semantica.pop()
        x2 = pilha_semantica.pop()
        x3 = pilha_semantica.pop()
        exp_r = str(x3[1]) + ' ' + str(x1[1]) + ' ' + str(x2[1])

        text0 = 'bool' + ' T' + str(numTemp) + ';\n'
        text0 = indentar(0, text0)

        text = 'T' + str(numTemp) + ' = ' + str(exp_r) + ';\n'
        text = indentar(indent, text)

        indent += 4
        indentacao = ' ' * indent
        text2 = str(indentacao) + "if (" + 'T' + str(numTemp) + '){\n'
        corpo_temporarias.append(text0)
        corpo.append(text)
        corpo.append(text2)
        numTemp += 1

    # elif prod == gramatica.gram[33]:  # R -> facaAte ( EXP_R ) CP_R
    # x1 = pilha_semantica.pop()
    # x2 = pilha_semantica.pop()
    # x3 = pilha_semantica.pop()
    # exp_r = str(x3[1]) + ' ' + str(x1[1]) + ' ' + str(x2[1])
    #
    # text0 = 'bool' + ' T' + str(numTemp) + ';\n'
    # text0 = indentar(0, text0)
    #
    # text = 'T' + str(numTemp) + ' = ' + str(exp_r) + ';\n'
    # text = indentar(indent, text)
    #
    # indent += 4
    # indentacao = ' ' * indent
    # text2 = str(indentacao) + "if (" + 'T' + str(numTemp) + '){\n'
    # corpo_temporarias.append(text0)
    # corpo.append(text)
    # corpo.append(text2)
    # numTemp += 1

    elif prod == gramatica.gram[31] or prod == gramatica.gram[37] or prod == gramatica.gram[38]:
        indentacao = ' ' * indent
        corpo.append(str(indentacao) + '}\n')
        indent -= 4

    return erro
