# coding: utf-8

import sys

# Dicionário global para armazenar as informações da máquina de estados (autômato).
maquina = {}

# Função para processar o arquivo que define o autômato.
def processar_arquivo_automato(arquivo):
    with open(arquivo, 'r') as f:  # Abre o arquivo para leitura.
        linhas = f.readlines()  # Lê todas as linhas do arquivo.

        # Armazena os estados, o estado inicial e os estados finais na máquina.
        maquina["estados"] = linhas[0].strip().split()  # Primeira linha: estados.
        maquina["inicial"] = linhas[1].strip()  # Segunda linha: estado inicial.
        maquina["final"] = linhas[2].strip().split()  # Terceira linha: estados finais.

        maquina["transicoes"] = []  # Inicializa a lista de transições.
        # Processa cada linha de transição no arquivo.
        for linha in linhas[3:]:
            partes = linha.strip().split()  # Divide a linha em partes.
            if len(partes) == 3:  # Verifica se a linha tem o formato correto.
                # Adiciona a transição (estado inicial, símbolo, estado final).
                maquina["transicoes"].append([partes[0], partes[2], partes[1]])

# Função para ler um autômato a partir de um arquivo.
def ler_automato(arquivo_automato):
    with open(arquivo_automato, 'r') as f:
        linhas = f.readlines()  # Lê todas as linhas do arquivo.

    # Armazena os estados, estados iniciais e finais do autômato.
    estados = linhas[0].strip().split()  # Primeira linha: estados.
    estados_iniciais = linhas[1].strip().split()  # Segunda linha: estado inicial.
    estados_finais = linhas[2].strip().split()  # Terceira linha: estados finais.

    transicoes = {}  # Dicionário para armazenar transições.
    for linha in linhas[3:]:  # Processa cada linha de transição.
        estado_inicial, simbolo, estado_final = linha.strip().split()  # Divide a linha.
        # Adiciona o estado final à lista de transições do estado inicial e símbolo.
        if (estado_inicial, simbolo) not in transicoes:
            transicoes[(estado_inicial, simbolo)] = []
        transicoes[(estado_inicial, simbolo)].append(estado_final)

    return estados, estados_iniciais, estados_finais, transicoes

# Função para ler a lista de palavras a serem verificadas.
def ler_lista_palavras(arquivo_palavras):
    with open(arquivo_palavras, 'r') as f:
        # Lê cada linha do arquivo e remove espaços em branco.
        palavras = [linha.strip() for linha in f.readlines()]
    return palavras  # Retorna a lista de palavras.

# Função para verificar se uma palavra é aceita pelo autômato.
def verificar_se_aceita(automato, palavra):
    estados, estados_iniciais, estados_finais, transicoes = automato  # Desempacota os componentes do autômato.

    # Função auxiliar recursiva que verifica se a palavra é aceita.
    def aceita(estado_atual, restante_palavra):
        if not restante_palavra:  # Se não há mais símbolos para processar.
            return estado_atual in estados_finais  # Verifica se o estado atual é um estado final.

        simbolo_atual = restante_palavra[0]  # Obtém o primeiro símbolo da palavra.
        restante_palavra = restante_palavra[1:]  # Remove o símbolo atual da palavra.

        if (estado_atual, simbolo_atual) in transicoes:  # Se há transições do estado atual com o símbolo atual.
            for proximo_estado in transicoes[(estado_atual, simbolo_atual)]:  # Para cada próximo estado.
                if aceita(proximo_estado, restante_palavra):  # Chama a função recursivamente.
                    return True  # Se a palavra é aceita.
        return False  # Se nenhuma transição aceita a palavra.

    for estado_inicial in estados_iniciais:  # Para cada estado inicial.
        if aceita(estado_inicial, palavra):  # Verifica se a palavra é aceita a partir do estado inicial.
            return True  # Se aceita, retorna True.

    return False  # Se nenhuma aceitação foi encontrada, retorna False.

# Função para formatar a saída do autômato.
def formatar_saida(estados_lista, estado_inicial, estados_finais_lista, transicoes_lista):
    resultado = []  # Inicializa a lista de resultados.
    resultado.append(" ".join(estados_lista))  # Adiciona os estados.
    resultado.append(estado_inicial)  # Adiciona o estado inicial.
    resultado.append(" ".join(estados_finais_lista))  # Adiciona os estados finais.

    transicoes_formatadas = []
    for elemento in transicoes_lista:  # Formata as transições.
        transicoes_formatadas.append(f"{elemento[0]} {elemento[2]} {''.join(elemento[1])}")  # Formato: estado_inicial simbolo estado_final.
    resultado.append("\n".join(transicoes_formatadas))  # Junta as transições em uma string.

    return "\n".join(resultado)  # Retorna a saída formatada.



# Função para converter a máquina de um AFN para uma AFD.
def converter_maquina(maquina):
    novo_resultado = {}  # Inicializa o dicionário para a nova máquina.
    estados_novos = gerar_estados(maquina["estados"])  # Gera novos estados.
    estado_inicial = gerar_estado_inicial(maquina, estados_novos)  # Gera o estado inicial.
    estados_aceitacao = gerar_estados_aceitacao(maquina["final"], estados_novos)  # Gera estados de aceitação.
    transicoes_novas = gerar_transicoes(maquina["transicoes"], estados_novos)  # Gera novas transições.

    # Organiza os componentes da nova máquina.
    novo_resultado["estados"] = organizar_estados(estados_novos)
    novo_resultado["inicial"] = "".join(estado_inicial)
    novo_resultado["final"] = organizar_estados(estados_aceitacao)
    novo_resultado["transicoes"] = organizar_transicoes(transicoes_novas)
    return novo_resultado  # Retorna a nova máquina.

# Função para organizar a lista de estados.
def organizar_estados(estados_novos):
    resultado = []
    for elemento in estados_novos:  # Para cada novo estado.
        estado_atual = "".join(elemento)  # Concatena os estados.
        if estado_atual not in resultado:  # Verifica se já está na lista.
            resultado.append(estado_atual)  # Adiciona se não estiver.
    return resultado  # Retorna a lista organizada.

# Função para organizar as transições.
def organizar_transicoes(transicoes_novas):
    resultado = []
    for elemento in transicoes_novas:  # Para cada nova transição.
        transicao_atual = ["".join(elemento[0]), elemento[1], "".join(elemento[2])]  # Formata a transição.
        if transicao_atual not in resultado:  # Verifica se já está na lista.
            resultado.append(transicao_atual)  # Adiciona se não estiver.
    return resultado  # Retorna a lista de transições organizadas.

# Função para gerar os estados de aceitação a partir dos estados finais.
def gerar_estados_aceitacao(lista_aceitacao, estados_novos):
    resultado = []
    for estado in estados_novos:  # Para cada novo estado.
        for e in estado:  # Para cada estado composto.
            if (e in lista_aceitacao):  # Verifica se está na lista de estados finais.
                resultado.append(estado)  # Adiciona o estado se for de aceitação.
                break
    return resultado  # Retorna os estados de aceitação gerados.

# Função para gerar as novas transições a partir das transições antigas.
def gerar_transicoes(lista_transicoes, estados_novos):
    resultado = []  # Inicializa a lista de transições.
    alfabeto = []  # Inicializa a lista do alfabeto.
    casos_epsilon = []  # Inicializa a lista para transições epsilon.

    for transicao in lista_transicoes:  # Para cada transição antiga.
        if transicao[2] != "h" and transicao[2] not in alfabeto:  # Se não for epsilon e não está no alfabeto.
            alfabeto.append(transicao[2])  # Adiciona ao alfabeto.
        if transicao[2] == "h":  # Se for uma transição epsilon.
            casos_epsilon.append(transicao)  # Adiciona à lista de transições epsilon.

    alfabeto.sort()  # Ordena o alfabeto.

    for estado in estados_novos:  # Para cada novo estado.
        for entrada in alfabeto:  # Para cada símbolo do alfabeto.
            aux = []  # Inicializa a lista auxiliar.
            for elemento in lista_transicoes:  # Para cada transição antiga.
                # Se o elemento pertence ao estado atual e a entrada corresponde.
                if (elemento[0] in estado and (elemento[2] == entrada) and elemento[1] not in aux):
                    aux.append(elemento[1])  # Adiciona o estado seguinte à lista auxiliar.
                    # Verifica se há uma transição epsilon a partir do estado atual.
                    if([elemento[1], elemento[0], "h"] in casos_epsilon and elemento[0] not in aux):
                        aux.append(elemento[0])  # Adiciona estado atual se tiver transição epsilon.
            aux.sort()  # Ordena a lista auxiliar.
            transicao_atual = [estado, aux, entrada]  # Formata a nova transição.
            # Verifica se a nova transição não está na lista de resultados.
            if transicao_atual not in resultado:
                if aux in estados_novos:  # Se a nova lista de estados existe.
                    resultado.append(transicao_atual)  # Adiciona a nova transição.
                elif len(aux) == 0:  # Se não houver estados na lista auxiliar.
                    resultado.append([estado, ["h"], entrada])  # Adiciona transição epsilon.
    return resultado  # Retorna as novas transições geradas.

# Função para gerar o estado inicial da nova máquina a partir da máquina antiga.
def gerar_estado_inicial(maquina, estados_novos):
    resultado = []  # Inicializa a lista do estado inicial.
    estado_inicial_antigo = maquina["inicial"]  # Obtém o estado inicial antigo.
    resultado.append(estado_inicial_antigo)  # Adiciona o estado inicial à lista de resultados.

    for e in maquina["transicoes"]:  # Para cada transição antiga.
        if e[0] == estado_inicial_antigo and e[2] == "h" and (e[1] not in resultado):
            resultado.append(e[1])  # Adiciona estados a partir de transições epsilon.

    # Retorna o estado inicial na nova máquina.
    if resultado in estados_novos:
        return resultado
    else:
        return [estado_inicial_antigo]  # Retorna apenas o estado inicial se não houver transições.

# Função para gerar todos os estados possíveis (potência do conjunto) a partir da lista de estados.
def gerar_estados(lista_estados):
    resultado = [x for x in powerset(lista_estados)]  # Gera o conjunto das partes (potência do conjunto).
    resultado.sort(reverse=True, key=len)  # Ordena por tamanho dos estados.
    resultado.reverse()  # Inverte a lista para que os maiores estados venham primeiro.
    for e in resultado:
        if len(e) == 0:  # Se a lista está vazia.
            e.append("h")  # Adiciona o estado vazio.
            break
    return resultado  # Retorna todos os estados gerados.

# Função para gerar o conjunto das partes (potência do conjunto).
def powerset(lista):
    if len(lista) <= 1:  # Se a lista tem 0 ou 1 elemento.
        yield lista  # Retorna a lista como está.
        yield []  # Também retorna a lista vazia.
    else:
        for item in powerset(lista[1:]):  # Para os itens restantes na lista.
            yield [lista[0]] + item  # Inclui o primeiro item.
            yield item  # Não inclui o primeiro item.

# Função principal que executa o código.
def main():
    # Define os arquivos de entrada.
    arquivo_automato = "src/inicial.txt"  # Caminho do arquivo do autômato.
    arquivo_palavras = "src/palavras.txt"  # Caminho do arquivo das palavras.
    
    # Processa o arquivo do autômato.
    processar_arquivo_automato(arquivo_automato)

    # Sempre converter, pois não verificamos se é AFD.
    nova_maquina = converter_maquina(maquina)  # Converte a máquina.
    # Formata a saída da nova máquina.
    resultado = formatar_saida(nova_maquina["estados"], nova_maquina["inicial"], nova_maquina["final"], nova_maquina["transicoes"])
    
    # Grava o resultado da nova máquina em um arquivo.
    with open("resultado_automato.txt", "w") as f:
        f.write(resultado)  # Escreve no arquivo.

    # Lê o autômato a partir do arquivo.
    automato = ler_automato(arquivo_automato)
    # Lê a lista de palavras a serem verificadas.
    palavras = ler_lista_palavras(arquivo_palavras)

    # Verifica cada palavra e grava o resultado em um arquivo.
    with open("resultado_verificacao.txt", "w") as f:
        for palavra in palavras:
            if verificar_se_aceita(automato, palavra):  # Verifica se a palavra é aceita.
                f.write(f"{palavra} - Aceita\n")  # Se aceita, escreve no arquivo.
            else:
                f.write(f"{palavra} - Não aceita\n")  # Se não aceita, escreve no arquivo.

# Verifica se o script está sendo executado diretamente e chama a função principal.
if __name__ == "__main__":
    main()
