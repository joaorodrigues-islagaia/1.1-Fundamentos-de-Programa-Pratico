# estatistica.py

'''--- Função MENU ESTATISTICAS ---
1. - Apresentar um menu com opções de estatísticas
2. - Permitir ao utilizador escolher uma opção e ver o resultado
3. - Voltar ao menu principal quando o utilizador escolher sair
'''

import os
import validacoes

def menu_estatisticas(lista_jogos):

    while True:
        validacoes.limpar_ecra()
        print("\n" + "="*30)
        print("      LIGA DE FUTEBOL - Menu de Estatisticas    ")
        print("="*30)
        print("1. Jogos com mais golos")
        print("2. Média de golos por jogo")    
        print("3. Equipa com mais golos marcados")
        print("4. Equipa com mais golos sofridos")
        print("0. Voltar ao menu principal")
        
        try:
            opcao = int(input("Escolha uma opção: "))
        except:
            print("Opção inválida!")                  # se der erro na conversao para inteiro
            input()
        else:
            if opcao == 1:
                jogos_mais_golos(lista_jogos)

            elif opcao == 2:
                media_golos_por_jogo(lista_jogos)

            elif opcao == 3:
                equipa_mais_golos(lista_jogos)

            elif opcao == 4:
                equipa_mais_golos_sofridos(lista_jogos)

            elif opcao == 0:
                break 
            else:
                print("Opção errada!")

''' --- Função para CALCULAR TOTAL DE GOLOS DE UM JOGO ---
- vou usar na função de jogos com mais golos
- vou usar na função média de golos por jogo
Recebe uma lista de um jogo e devolve a soma dos golos.
'''
def calcular_total_golos(jogo):
    # jogo[3] são os golos da casa, jogo[4] são os golos de fora
    return jogo[3] + jogo[4]
# --- Fim Função CALCULAR TOTAL GOLOS JOGO ---

''' --- Função  JOGOS COM MAIS GOLOS ---
1. - Ordenar a lista de jogos com base no total de golos (golos_casa + golos_fora) em ordem decrescente
2. - Selecionar os 10 primeiros jogos da lista ordenada 

Regras:
- Validação: se lista vazia devolve lista vazia
- top_n coerente: se <= 0 devolve lista vazia; se > len(lista) devolve todos.
- Ordenação: por total_golos desc; como desempate mantém ordem original (estável).
- Retorno: lista de dicts (cópias dos jogos) com campo adicional 'total_golos' para facilitar impressão.

'''
def jogos_mais_golos(lista_jogos, top_n_default=10):
    """
    Top jogos por total de golos, assumindo cada jogo no formato: [jornada, data, equipa_casa, golos_casa, golos_fora, equipa_fora]
    Retorna uma lista de listas do mesmo formato com um campo adicional no final: total_golos
    """
    # 1) Validação básica
    if lista_jogos == []:
        validacoes.limpar_ecra()
        print("Nenhum jogo registado.")
        input("\nPressione ENTER para continuar.")
        return []

    # 2) Calcular total de golos por jogo (defensivo)
    jogos_com_totais = []

    for jogo in lista_jogos:

        total = calcular_total_golos(jogo)  # usamos a função de contar total golos por jogo

        novo = [jogo[0], jogo[1], jogo[2], jogo[3], jogo[4], jogo[5], total]

        jogos_com_totais.append(novo) # vou adicionando o jogo com total de golos à lista
        
    # 4) Ordenar por total (descendente). sort/ sorted é estável para empates.
    jogos_ordenados = sorted(jogos_com_totais, key=lambda x: x[6], reverse=True) # key=lambda x: x[6] — para cada elemento x da lista (aqui uma lista por jogo) a função lambda retorna x[6] (o indice 6, total_golos) que é usado como chave de ordenação.

    # 5) Selecionar top_n (se top_n > len, devolve tudo)
    top_jogos = jogos_ordenados[:top_n_default]

    # 6) Mostrar resultados ao utilizador
    validacoes.limpar_ecra()
    print(f"\nTop {top_n_default} jogos com mais golos:\n")
    for i in top_jogos:
        print(f"Jornada {i[0]} | {i[1]} | {i[2]} {i[3]} - {i[4]} {i[5]}  (Total: {i[6]})")
    input("\nPressione ENTER para continuar.")    
# --- Fim Função JOGO com MAIS GOLOS  ---

''' --- Função EQUIPA com MAIS GOLOS MARCADOS ---
1. - Criamos um dicionário vazio.
2. - Percorremos a lista de jogos com um ciclo for.
3. - Para cada jogo, vamos buscar quem jogou e quantos golos marcou.
4. - Somamos esses golos ao total da equipa no dicionário.
5. - No fim, fazemos outro ciclo for apenas para descobrir quem tem o valor mais alto.
'''
def equipa_mais_golos(lista_jogos):

    golos_por_equipa = {}       # dicionáro que vai guardar chave:valor ('equipa':golos marcados)

    # Validação se lista vazia
    if lista_jogos == []:
        validacoes.limpar_ecra()
        print("Nenhum jogo registado.")
        input("\nPressione ENTER para continuar.")
        return []

    for jogo in lista_jogos:

        # nomes equipas e golos
        nome_casa = jogo[2]
        golos_casa = jogo[3]

        nome_fora = jogo [5]
        golos_fora = jogo[4]

        # --- Somar golos da Equipa da Casa ---
        if nome_casa in golos_por_equipa:
            # Se já existe, então somamos ao valor de golos que já lá estava
            golos_por_equipa[nome_casa] = golos_por_equipa[nome_casa] + golos_casa # basta indicar que vamos somar (???)
        else:
            # Se não existe, cria a entrada nova com o nome da equipa e os golos deste jogo
            golos_por_equipa[nome_casa] = golos_casa

        # --- repetimos o racional agora para somar golos da Equipa de Fora ---
        if nome_fora in golos_por_equipa:
            golos_por_equipa[nome_fora] = golos_por_equipa[nome_fora] + golos_fora
        else:
            golos_por_equipa[nome_fora] = golos_fora

    # 3. Descobrir qual a equipa com mais golos (Algoritmo do Maior)
    equipas_mais_golos = []
    max_golos = -1

    # 4. Percorrer o dicionário (chave é o nome, valor são os golos)
    for equipa in golos_por_equipa:
        total_desta_equipa = golos_por_equipa[equipa]

        # CASO 1: Encontrámos um novo recorde!
        if total_desta_equipa > max_golos:
            max_golos = total_desta_equipa        # Atualizamos o recorde
            lista_vencedores = [equipa]           # IMPORTANTE: Criamos uma lista NOVA (apagamos os anteriores), pois temos um novo record
        
        # CASO 2: É um empate com o recorde atual
        elif total_desta_equipa == max_golos:
            lista_vencedores.append(equipa)       # Aqui usamos APPEND (junta-se aos lideres já encontrados)

    texto_equipas = ""
    for nome in lista_vencedores:
        if texto_equipas == "":
            texto_equipas = nome
        else:
            texto_equipas = texto_equipas + " e " + nome
    validacoes.limpar_ecra()        
    print(f"\nA equipa com mais golos marcados é: {texto_equipas}")
    print(f"Total de golos: {max_golos}")
    
    # Pausa para o utilizador ler
    input("\nPressione ENTER para continuar.")
# --- Fim Função EQUIPA com MAIS GOLOS MARCADOS ---    

''' --- Função EQUIPA com MAIS GOLOS SOFRIDOS (Versão Procedimento) ---
1. - Contar os golos sofridos 
2. - Encontrar a(s) equipa(s) com mais golos sofridos (pior defesa)
3. - Imprimir diretamente o resultado
'''
def equipa_mais_golos_sofridos(lista_jogos):

    if lista_jogos == []:
        validacoes.limpar_ecra()
        print("Nenhum jogo registado.")
        input("\nPressione ENTER para continuar.")
        return # Sai do procedimento

    golos_sofridos_por_equipa = {} 

    # 2. Somar golos SOFRIDOS
    for jogo in lista_jogos:
   
        nome_casa = jogo[2]
        golos_casa = jogo[3] # Golos que a equipa de Casa MARCOU
        
        nome_fora = jogo[5]
        golos_fora = jogo[4] # Golos que a equipa de Fora MARCOU

        # Equipa da CASA sofre os golos da equipa de FORA ---
        if nome_casa in golos_sofridos_por_equipa:
            golos_sofridos_por_equipa[nome_casa] = golos_sofridos_por_equipa[nome_casa] + golos_fora
        else:
            golos_sofridos_por_equipa[nome_casa] = golos_fora

        # Equipa de FORA sofre os golos da equipa de CASA ---
        if nome_fora in golos_sofridos_por_equipa:
            golos_sofridos_por_equipa[nome_fora] = golos_sofridos_por_equipa[nome_fora] + golos_casa
        else:
            golos_sofridos_por_equipa[nome_fora] = golos_casa

    # Descobrir qual a equipa com mais golos sofridos (Pior defesa)
    lista_piores_defesas = []
    max_golos_sofridos = -1

    for equipa in golos_sofridos_por_equipa:
        total_sofridos = golos_sofridos_por_equipa[equipa]

        if total_sofridos > max_golos_sofridos:
            max_golos_sofridos = total_sofridos    # Novo recorde negativo
            lista_piores_defesas = [equipa]        # Reinicia a lista
        
        elif total_sofridos == max_golos_sofridos:
            lista_piores_defesas.append(equipa)    # Empate

    # 4. Formatar texto e mostrar resultado
    texto_equipas = ""
    for nome in lista_piores_defesas:
        if texto_equipas == "":
            texto_equipas = nome
        else:
            texto_equipas = texto_equipas + " e " + nome

    validacoes.limpar_ecra()      
    print(f"\nA equipa com mais golos SOFRIDOS é: {texto_equipas}")
    print(f"Total de golos sofridos: {max_golos_sofridos}")
    
    input("\nPressione ENTER para continuar.")
# --- Fim Função EQUIPA com MAIS GOLOS SOFRIDOS ---


''' --- Função MEDIA DE GOLOS POR JOGO ---
1. - Iterarar todos os jogos da lista de jogos
2. - Criar um dicionario 
Somar todos os golos marcados em todos os jogos
2. - Dividir o total de golos pelo número total de jogos    
'''
def media_golos_por_jogo(lista_jogos):
    
    if len(lista_jogos) == 0:
        validacoes.limpar_ecra()
        print("Nenhum jogo registado.")
        input("\nPressione ENTER para continuar.")
        return -1

    total_golos_campeonato = 0      
    total_jogos = len(lista_jogos)

    for jogo in lista_jogos:
        # AQUI: Usamos a função auxiliar que criámos!
        golos_deste_jogo = calcular_total_golos(jogo)
        
        # Adicionamos ao acumulador
        total_golos_campeonato += golos_deste_jogo

    media = total_golos_campeonato / total_jogos
    validacoes.limpar_ecra()
    print(f'A média foi de, {media:.2f} golos/jogo\n')
    input("\nPressione ENTER para continuar.")
# --- Fim Função MEDIA DE GOLOS POR JOGO ---


'''--- Funcao TABELA CLASSIFICACAO ---
1 - Calcular os pontos de cada equipa (Vitoria = 3, Empate = 1, Derrota = 0)    
2 - Ordenar a tabela por pontos 
3 - Apresentar a tabela de classificação
4 - Carregar ENTER para voltar ao menu     
'''   
def tabela_classificacao(lista_jogos):
    
    # 1. Validação se lista vazia
    if lista_jogos == []:
        print("Nenhum jogo registado.")
        input("\nPressione ENTER para continuar.")
        return

    # Dicionário, onde a chave é o nome da equipa, o valor é uma lista: [Pontos, Jogos]
    info_equipa = {}

    for jogo in lista_jogos:
        # Extrair dados: [Jornada, Data, equipa Casa, GC, GF, equipa Fora]
        casa = jogo[2].lower()
        gc = jogo[3]
        fora = jogo[5].lower()
        gf = jogo[4]

        # Se a equipa não existe no dicionário, cria-se a entrada a zeros
        if casa not in info_equipa:
            info_equipa[casa] = [0, 0] # isto cria a chave:valro --> equipa:[Pontos, Jogos]
        if fora not in info_equipa:
            info_equipa[fora] = [0, 0]

        # --- Atualizar Jogos Realizados (índice 1) ---
        info_equipa[casa][1] += 1
        info_equipa[fora][1] += 1

        # --- Calcular Pontos (índice 0) ---
        if gc > gf:                     # Vitória da Casa
            info_equipa[casa][0] += 3   # Casa ganha 3 pontos
            
        elif gf > gc:                   # Vitória de Fora
            info_equipa[fora][0] += 3   # Fora ganha 3 pontos
            
        else:             # Empate
            info_equipa[casa][0] += 1   # 1 Ponto para casa
            info_equipa[fora][0] += 1   # 1 Ponto para fora

    # Agora converter Dicionário para Lista (para poder ordenar)
    # Formato final da lista: [Nome, Pontos, Jogos]
    tabela_final = []

    for nome_equipa in info_equipa:
        dados = info_equipa[nome_equipa]    # vou receber a lista [Pontos, Jogos] de cada nome_equipa do dicionário
        pontos = dados[0]                   # a cada lista vou ao indice 0, buscar os Pontos
        jogos = dados[1]                    # Vou ao indice 1 buscar os Jogos
        
        # Criar a linha e adicionar à tabela (lista de listas)
        linha = [nome_equipa, pontos, jogos]
        tabela_final.append(linha)

    # Ordenar a Tabela
    
    tabela_ordenada = sorted(tabela_final, key=lambda x: x[1], reverse=True) 
    # key=lambda x: x[1] -> Ordena pelos Pontos (que está no índice 1 da nossa lista 'linha'). 
    # reverse=True -> Do maior para o menor
    # Já temos a lista de listas ordenada do primeiro para o último
    # Apresentar Tabela bonitinha
    
    validacoes.limpar_ecra()
    
    print(f"\n{'POS':<4} {'EQUIPA':<30} {'PTS':<5} {'J':<5}")   # o cabeçalho da tabela
    print("="*45)

    posicao = 1     # contador para marcar a posição na tabela, de cada equipa
    for equipa in tabela_ordenada:
        # equipa = [Nome, Pontos, Jogos]
        nome = equipa[0]
        pts = equipa[1]
        j = equipa[2]
        
        print(f"{posicao:<4} {nome:<30} {pts:<5} {j:<5}")
        posicao += 1

    print("="*45)
    input("\nPressione ENTER para voltar.")

# --- Fim Função TABELA CLASSIFICACAO ---