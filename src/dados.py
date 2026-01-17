
import os
import requests # https://requests.readthedocs.io/en/latest/
import validacoes

# necessário para abrir janela de seleção de ficheiro a carregar
import tkinter as tk
from tkinter import filedialog


'''--- Função IMPORTAR JOGOS API ---
--- Importar dados da API: https://api.football-data.org/v4/competitions/PL/matches (PL = Premier League)

O Algoritmo da Importação:
1 - Parametros: AKI Key, chave de acesso à API; Epoca, que queremos importar
2 - Criar a função GET URL e Chave 
3 - Verificar se recebemos resposta da API
    3.a - Exceção mostra ERRO com código de estado
4 - Colocamos a resposta atraves de decodificadore JSON num ficheiro
5 - Vamos ler o JSON com um ciclo, a percorrer todos os 'match'
6 - Em cada ciclo vamos ler os atributos relevantes: Jornada, Data, Equipa da Casa, Equipa Visitante, golos casa e golos fora.
5 - Criamos a linha a inserir no CSV, e adicionamos ao CSV
6 - Retona a lista de jogos em formato CSV
'''
def importar_jogos_api(api_key):

    validacoes.limpar_ecra()
    print("--- Inserir jogos API ---\n")
    epoca = int(input("Qual a época a importar (ex.: 2025): ")) 

    # Adicionámos ?season=2025 no fim
    url = f"https://api.football-data.org/v4/competitions/PL/matches?season={epoca}"
    headers = { 'X-Auth-Token': api_key }    # Chave da API

    print("\nA ligar à API da Premier League...")
    resposta = requests.get(url, headers=headers)                       # função GET, passamos os parametros URL e HEADERS

    if resposta.status_code == 200:
        dados_json = resposta.json()    # builtin JSON decoder. Se façhar o decode, gera uma excessão (https://requests.readthedocs.io/en/latest/user/quickstart/)
        lista_jogos = []

        for jogo in dados_json['matches']:
            # vamos extrair do ficheiro json os dados do JOGO
            jornada = jogo['matchday']
            data = jogo['utcDate'][0:10] # Apenas a data (AAAA-MM-DD)
            casa = jogo['homeTeam']['name']
            fora = jogo['awayTeam']['name']

            # Agora vampos extrair os golos do jogoa (recebmos None é para jogos ainda não realizados, atribuimos o valor "-1")
            g_casa = jogo['score']['fullTime']['home']
            g_fora = jogo['score']['fullTime']['away']

            if g_casa is None:
                g_casa = -1
                g_fora = -1

           # Cria a linha: [Jornada, Data, Casa, G_Casa, G_Fora, Fora]
            linha = [jornada, data, casa, g_casa, g_fora, fora]
            lista_jogos.append(linha) 
        
        print(f"\nSucesso! {len(lista_jogos)} jogos importados.")
        input("\nPressione ENTER para continuar.")
        return lista_jogos
    else:
        print(f"\nErro na API: Código {resposta.status_code}")
        input("\nPressione ENTER para continuar.")
        return []

'''--- Função GUARDA CSV ---
O Algoritmo da Guardar Ficheiro:

1 - Parametros: nome do ficheiro, que se pretende gravar; lista de dados que temos atualmente carregada no programa
2 - Tentar criar o ficheiro, em modo escrita (w)
    2.1 - Exceção, se não for possivel criar o ficheiro, apresenta erro.
3 - Escrever no ficheiro o cabeçalho, que está de acordo com a ordem definida na função _importar_jogos_api_
4 - Ciclo para percorrer a lista de jogos e inseir linha a linha no CSV
5 - Fechar o ficheiro (gravar)
'''
def guardar_dados_csv(nome_sugerido, lista_dados):
    validacoes.limpar_ecra()
    print("--- Guardar Ficheiro ---\n")

    if lista_dados == []:
            print("\nAviso: Não existem dados na memória para guardar.")
            input("\nPressione ENTER para continuar...")
            return

    # Abrir Janela de "Guardar Como"
    print("A aguardar seleção do local de gravação...")
    
    root = tk.Tk()
    root.withdraw() # Esconde a janela principal cinzenta
    
    # Abre a janela de salvar, sugerindo o nome que vem do main.py
    nome_ficheiro = filedialog.asksaveasfilename(
        title="Guardar Base de Dados",
        initialfile=nome_sugerido,       # Sugere "jogos_premier_league.csv"
        defaultextension=".csv",         # Se o utilizador não escrever extensão, mete .csv por defeito
        filetypes=[("Ficheiros CSV", "*.csv"), ("Todos os ficheiros", "*.*")]
    )
    
    root.destroy() # Fecha o processo da janela


    # Recebe a lista de jogos e guarda num ficheiro de texto (CSV).
    # Criar com excessão
    try:
        # Abrir o ficheiro em modo de escrita ('w')
        ficheiro = open(nome_ficheiro, 'w', newline='', encoding='utf-8')
        
        # Escrever o cabeçalho
        ficheiro.write("Jornada,Data,Casa,Golos C,Golos F,Fora\n")
        
        # Agora vamos percorrer a lista de jogos do nosso CSV
        for jogo in lista_dados:
            # cada jogo é uma lista: [1, '2025-08...', 'Arsenal', 2, 0, 'Chelsea'] conforme o cabeçalho que definimos.
            linha_texto = str(jogo[0]) + "," + str(jogo[1]) + "," + jogo[2] + "," + str(jogo[3]) + "," + str(jogo[4]) + "," + jogo[5] + "\n"
            # agora temos a linha da forma que pretendemos escrever no ficheiro
            ficheiro.write(linha_texto)

        # Fechar o ficheiro
        ficheiro.close()
        print(f"Ficheiro '{nome_ficheiro}' gravado com sucesso!")
        
    except:
        print(f"Erro ao gravar ficheiro")
    
    print(input('\nPrimir ENTER para continuar.'))

'''--- Função CARREGAR DO FICHEIRO CSV ---
O Algoritmo da Carregar dados de um Ficheiro:
------------------ Podemos criar aqui janela de ABRIR FICHEIRO--------------------------------------------- !!!!!!!!!!!!!!!!!!!
1 - Parametros: nome do ficheiro que queremos abrir
2 - Tentar abrir o ficheiro, modo leitura
    2.1 - Exceção, se não for possivel ler o ficheiro, apresenta erro.
3 - Ler todas as linhas, uma por uma (funão readlines) para uma lista
4 - Fechar o ficheiro
5 - Ciclo de ler cada linha da lista criada (saltar linha do cabeçalho)
6 - A cada linha (lista) da lista de linhas, separar os dados e carregar no indice correto de acordo com o definido na função _importar_jogos_api_
7 - Cada linha, é adicionada à lista de jogos
8 - Retona a lista (de listas) de jogos 
'''
def carregar_dados_csv(nome_ficheiro=None):

    validacoes.limpar_ecra()

    # SE não foi passado nome, abrimos a janela (código fonte: https://gemini.google.com/app/0dd27cfbbf71be87 )
    if nome_ficheiro is None:
        print("A aguardar seleção de ficheiro na janela...")
        root = tk.Tk()
        root.withdraw() # Esconde a janela principal "feia" do Tkinter
        
        # Abre o explorador de ficheiros
        nome_ficheiro = filedialog.askopenfilename(
            title="Selecionar Base de Dados",
            filetypes=[("Ficheiros CSV", "*.csv"), ("Todos os ficheiros", "*.*")]
        )
        
        root.destroy() # Fecha a instância do Tkinter

    # Se o utilizador cancelou a janela ou string vazia
    if not nome_ficheiro:
        print("Nenhum ficheiro selecionado.")
        input("\nPressione ENTER para continuar...")
        return []

    #     Lê o ficheiro e separa as palavras pelas vírgulas (split).
    lista_jogos = []

    try:
        # Abrir para leitura ('r')
        ficheiro = open(nome_ficheiro, 'r', encoding='utf-8')
        
        # Ler todas as linhas para uma lista de strings
        linhas_do_ficheiro = ficheiro.readlines()
        
        # Fechar ficheiro
        ficheiro.close()
        
        # Ler cada linha, e começamos no índice 1 para saltar o cabeçalho (que está no índice 0)
        for i in range(1, len(linhas_do_ficheiro)): # range de 1 ao comprimento da nossa lista de listas
            
            linha_atual = linhas_do_ficheiro[i]
            
            # .strip() remove o '\n' (o enter) do final da linha
            linha_limpa = linha_atual.rstrip()
            
            # .split(',') parte a frase onde houver vírgulas e cria uma lista com esses valores
            dados_linha = linha_limpa.split(',')
            
            # Agora temos uma lista de strings, ex: ['1', '2025...', 'Arsenal'...]
            # Precisamos de converter os valores para números inteiros
            
            jornada = int(dados_linha[0])
            data = dados_linha[1]
            casa = dados_linha[2]
            g_casa = int(dados_linha[3])
            g_fora = int(dados_linha[4])
            fora = dados_linha[5]
            
            # Reconstruir a lista final
            jogo_formatado = [jornada, data, casa, g_casa, g_fora, fora]
            lista_jogos.append(jogo_formatado)

        print("-"*30)
        print(f'Nome do ficheiro: {nome_ficheiro} carregado com sucesso.')
        print(f"{len(lista_jogos)} jogos na memória.")
        print(input("Pressione Enter para continuar..."))
        return lista_jogos

    except:
        print(f"Erro ao ler ficheiro.")
        input("\nPressione ENTER para continuar...")
        return []

''' --- Função INSERIR JOGOS MANUALMENTE --- 
Algoritmo da Inserção Manual:
1 - Parametro: lista de listas de jogos existente
2 - Tentar pedir um por um os atributos de cada jogo
3 - Criar a lista do jogo, com os atributos inseridos
-----------------------------------------------------  CRIAR VALIDAÇÃO JORNADA+EQUIPA, não aceitar duplicado  ----------------------------
4 - Adicionar o jogo à lista de jogos 

'''
'''def inserir_jogo_manual(lista_jogos):
    # Ciclo infinito para permitir inserir vários jogos
    while True:
        validacoes.limpar_ecra()
        # Pede ao utilizador os dados de um jogo e adicionar jogo (lista) à lista de jogos (lista de listas).
        print("\n--- Inserir Novo Jogo ---")
        try:
            # Pedir os dados um a um, mas permitir cancelar ação antes de inserir jornada (ENTER para sair)
            jornada = validacoes.ler_inteiro('Jornada nº (ENTER para cancelar): ', 1, 38, permite_vazio =True)

            if jornada is None:
                print("Operação cancelada.\n")
                # E quer continuar a inserir outro jogo?
                continuar = input("Deseja inserir outro jogo? (S/N): ").strip().lower()
                if continuar != 's':
                    return lista_jogos  # Sai do ciclo infinito e retorna a lista atualizada
                else:
                    continue  # volta ao inicio do ciclo para inserir novo jogo 
                
            data = validacoes.ler_data("Data (AAAA-MM-DD): ")
            casa = validacoes.ler_texto("Equipa Casa: ")
            fora = validacoes.ler_texto("Equipa Fora: ")
            
            print(f"Insira o resultado para {casa} vs {fora}:")
            g_casa = validacoes.ler_inteiro(f"Golos {casa}: ", 0, 20)
            g_fora = validacoes.ler_inteiro(f"Golos {fora}: ", 0, 20)

            # Criar a linha igual à estrutura da API: [Jornada, Data, Casa, GC, GF, Fora]
            novo_jogo = [jornada, data, casa, g_casa, g_fora, fora]

            # Confirmar dados de inserção e se pretende adicionar ou cancelar
            print("\nNovo Jogo a Registar:")  
            print(f"Jornada: {jornada}, Data: {data}, {casa} {g_casa} - {g_fora} {fora}\n")

            confirmar = input("Confirma a inserção deste jogo? (S/N): ").strip().lower()    
            if confirmar != 's':
                print("Operação cancelada.\n")
                # E quer continuar a inserir outro jogo?
                continuar = input("Deseja inserir outro jogo? (S/N): ").strip().lower()
                if continuar != 's':
                    return lista_jogos  # Sai do ciclo infinito e retorna a lista atualizada
                else:
                    continue  # volta ao inicio do ciclo para inserir novo jogo
            
            # Adicionar à lista principal
            lista_jogos.append(novo_jogo)
            print("Jogo registado com sucesso!\n")
            consultar_todos_jogos(lista_jogos)
            print(input(''))
        
            # Perguntar se quer inserir outro jogo
            continuar = input("Deseja inserir outro jogo? (S/N): ").strip().lower()
            if continuar != 's':
                return lista_jogos  # Sai do ciclo infinito e retorna a lista atualizada    

        except:
            print("ERRO: Não foi possivel registar o jogo.")
            continuar = input("Deseja inserir outro jogo? (S/N): ").strip().lower()
            if continuar != 's':
                return lista_jogos # Sai do ciclo infinito e retorna a lista atualizada
'''
# --- Função INSERIR JOGOS MANUALMENTE ---
def inserir_jogo_manual(lista_jogos):
    while True:
        validacoes.limpar_ecra()
        print("--- Inserir Novo Jogo ---\n")
        
        jornada = validacoes.ler_inteiro('Jornada nº (ENTER para cancelar): ', 1, 38, permite_vazio=True)
        if jornada is None:
            return lista_jogos

        data = validacoes.ler_data("Data (AAAA-MM-DD): ")
        casa = validacoes.ler_texto("Equipa Casa: ")
        fora = validacoes.ler_texto("Equipa Fora: ")
        
        print(f"\nResultado para {casa} vs {fora}:")
        g_casa = validacoes.ler_inteiro(f"Golos {casa}: ", 0, 20)
        g_fora = validacoes.ler_inteiro(f"Golos {fora}: ", 0, 20)

        novo_jogo = [jornada, data, casa, g_casa, g_fora, fora]

        print("\n--- Resumo do Jogo ---")  
        print(f"Jornada: {jornada} | {data}")
        print(f"{casa} {g_casa} - {g_fora} {fora}")

        confirmar = input("\nConfirma a inserção? (S/N): ").strip().lower()    
        if confirmar == 's':
            lista_jogos.append(novo_jogo)
            print("Jogo registado com sucesso!")
        else:
            print("Operação cancelada.")
            validacoes.limpar_ecra()
        
        if input("\nDeseja inserir outro jogo? (S/N): ").strip().lower() != 's':
            return lista_jogos


'''--- Funcao ELIMINAR TUDO ---
O Algoritmo da Eliminação de todos os jogos:
1 - Parametro: Lista de jogos
2 - Mensagem de confirmação se pretende de facto eliminar tudo
    2.a - Se "N", sistema não elimina e mostra mensagem "Opoeração Cancelada"
3 - Se "S", sistema vai limpar a variavel global lista de jogos
(Nota: não precisa de return por ser uma variavel global)
'''
def eliminar_tudo(lista_jogos):
    validacoes.limpar_ecra()
    print("--- ATENÇÃO: Eliminar Todos os Jogos ---\n")

    confirmar = input("Tem a certeza que quer apagar TODOS os jogos? (S/N): ")
    if confirmar.lower() == 's':
        lista_jogos # Precisamos de global para "limpar" a variavel original --- PRECISO DISTO AQUI??
        lista_jogos.clear()  # Limpa a lista de jogos 
        print("Todos os jogos foram apagados da memória.")
        
    else:
        print("Operação cancelada.")
    
    input("Pressione Enter para continuar...")

''' --- Funcao PESQUISAR JOGO ESPECIFICO ---
Algoritmo da Pesquisa de um jogo especifico:
1 - Parametro: Lista de jogos
2 - Pede a jornada que se pretende pesquisar (Invoca a função de validação, para validação inteiros, texto e data)
    2.a Opção '0' permite sair da pesquisa
3 - Pede equipa a pesquisar (que pode ter jogado em casa ou fora)
4 - Sistema vai iterar a lista de jogos, e para cada jogos separa os atributos (da lista do jogo)) e compara com os valores pesquisados.
5 - Se encontrar valor igual para jornada E equipa, apresenta o jogo encontrado
    5.a - Se não encontrar jornada E equipa, mostra mensagem de erro
6 - Apos mostrar permitem ao utilizador repetir a pesquisa
7 - A função retorna sempre o indice do jogo (referente à lista de jogos) para poder ser usada para Alterar e Eliminar jogo.
    7.a - Ou no caso da pesquisa não ter resultados não devolve indice
'''
def pesquisar_jogo(lista_jogos):
    validacoes.limpar_ecra()
    print("--- Pesquisar Jogo ---")
    
    while True:

        jornada_pesquisar = validacoes.ler_inteiro("\nQual a Jornada que procura (1-38)? (ENTER para sair) ", 1, 38, permite_vazio = True)
        
        if jornada_pesquisar is None:
            print('Sair da pesquisa')
            return -1, None
    
        # Pedir a equipa a pesquisar
        equipa_pesquisar = validacoes.ler_texto("\nQual a Equipa (Casa ou Fora)? ").lower()

        print(f"\nA procurar na Jornada {jornada_pesquisar} por '{equipa_pesquisar}'...\n")
    
        for i in range(len(lista_jogos)):
            jogo = lista_jogos[i]
            # jogo: [0=Jornada, 1=Data, 2=Casa, 3=GC, 4=GF, 5=Fora]
        
            if jogo[0] == jornada_pesquisar and (equipa_pesquisar in jogo[2].lower() or equipa_pesquisar in jogo[5].lower()):
                resumo = f"ENCONTRADO: J{jogo[0]} | {jogo[1]} | {jogo[2]} {jogo[3]} - {jogo[4]} {jogo[5]}"
                print("\n" + resumo)
                input("\nPressione ENTER para continuar...")
                return i, resumo

        print("\nJogo não encontrado.")
        input("\nPressione ENTER para continuar...")
        return -1, None

''' --- Funcao ALTERAR JOGO PESQUISADO ---
O Algoritmo da Eliminação:
1 - Parametro: Lista de jogos
2 - Pedir Jornada e Equipa (usar Funcao PESQUISAR JOGO ESPECIFICO).
    2.1 - Percorrer a lista à procura.
        2.1.1 - Se não encontrar: Mostra mensagem de erro
    2.1 - Se encontrar: Mostrar o jogo ao utilizador.
4 - Pedir confirmação ("Tem a certeza que pretende eliminar o jogo?").
5 - Se sim, apagar usando .pop(i).
    5.1 - Se não, cancela a ação e voltar ao inicio da função eliminar
6 - Continuar a apagar jogos?
7 - Se sim, volta para o inicio do algoritmo
Parar (break), porque a lista mudou de tamanho e continuar o loop daria erro.
'''
def alterar_jogo(lista_jogos):

    indice_jogo_alterar, str_jogo_alterar = pesquisar_jogo(lista_jogos)

    if indice_jogo_alterar == -1:
        print("Nenhum jogo seleccionado.")
        return lista_jogos # termina aqui a função
    
    print("\n--- Menu de Edição ---")

    confirmar_alterar = input("Tem a certeza que quer alterar este jogo? (S/N): ").strip().lower()

    if confirmar_alterar == 's':

        print("\nComo deseja editar?")
        print("S - Editar TUDO (Reescrever todos os dados do jogo)")
        print("N - Editar Campo a Campo (Para manter valor, primir ENTER)")
        opcao = input("Opção (S/N): ").strip().lower()

        if opcao == 's':

            # Pedir os dados um a um, mas vamos obrigar a preencher novos valores em todos eles
            jornada = validacoes.ler_inteiro("\nJornada (1-38): \n", 1, 38)
            data = validacoes.ler_data("Data (AAAA-MM-DD): \n")
            casa = validacoes.ler_texto("Equipa Casa: \n")
            fora = validacoes.ler_texto("Equipa Fora: \n")
            
            print(f"Insira o resultado para {casa} vs {fora}:\n")
            g_casa = validacoes.ler_inteiro(f"Golos {casa}: \n", 0, 20)
            g_fora = validacoes.ler_inteiro(f"Golos {fora}: \n", 0, 20)

            # Criar a linha igual à estrutura da API: [Jornada, Data, Casa, GC, GF, Fora]
            jogo_alterado = [jornada, data, casa, g_casa, g_fora, fora]

            print(str_jogo_alterar)
            print(f'\nALTERADO PARA: {jogo_alterado[0]} | {jogo_alterado[1]} | {jogo_alterado[2]}  {jogo_alterado[3]} - {jogo_alterado[4]} {jogo_alterado[5]}\n')  

            # continuar a alterar depois de rever o antes e o depois
            confirmar_alteracao_final = input("Confirma a alteração deste jogo? (S/N): ").strip().lower()
            if confirmar_alteracao_final == 's':
                # Adicionar à lista principal
                lista_jogos[indice_jogo_alterar] = jogo_alterado # no indice do jogo alterar, colocamos o jogo alterado
                print("Jogo alterado com sucesso!")   
            else:
                print("Operação cancelada.")
                return lista_jogos # termina aqui a função

        # --- Se não é todo o jogo, então temos de ir campo a campo perguntar se quer alterar esse campo ---
        elif opcao == 'n':
            # Edição campo-a-campo, ENTER mantém valor atual

            # guardo uma copia da lista do jogo selecionado, para comparar no final se existiram de facto alterações
            jogo_selecionado = lista_jogos[indice_jogo_alterar].copy()
            
            print("ENTER para manter o valor atual.")

            # Jornada (aceita ENTER para manter)
            nova_jornada = validacoes.ler_inteiro(f"Jornada atual ({jogo_selecionado[0]}). Nova jornada: ", 1, 38, True)
            if nova_jornada is not None:
                jogo_selecionado[0] = nova_jornada

            # Data
            nova_data = validacoes.ler_data(f"Data atual ({jogo_selecionado[1]}). Nova data: ", permite_vazio=True)
            if nova_data is not None:
                jogo_selecionado[1] = nova_data

            # Equipa Casa
            nova_casa = validacoes.ler_texto(f"Equipa Casa atual ({jogo_selecionado[2]}). Nova Equipa: ", permite_vazio=True)
            if nova_casa is not None:
                jogo_selecionado[2] = nova_casa
                
            # Golos Casa
            novos_golos_casa = validacoes.ler_inteiro(f"Golos {jogo_selecionado[2]} atuais ({jogo_selecionado[3]}). Novos golos: ", 0, 20, permite_vazio=True)
            if novos_golos_casa is not None:
                jogo_selecionado[3] = int(novos_golos_casa) 

            # Equipa Fora
            nova_fora = validacoes.ler_texto(f"Equipa Fora atual ({jogo_selecionado[5]}). Nova equipa: ", permite_vazio=True)
            if nova_fora is not None:
                jogo_selecionado[5] = nova_fora

            # Golos Fora
            novos_golos_fora = validacoes.ler_inteiro(f"Golos {jogo_selecionado[5]} atuais ({jogo_selecionado[4]}). Novos golos: ", 0, 20, permite_vazio=True)
            if novos_golos_fora is not None:
                jogo_selecionado[4] = int(novos_golos_fora)
            
            if lista_jogos[indice_jogo_alterar] == jogo_selecionado: #compara a copia que fizesmos (original) com o que foi alterado
                print('Não realizou nenhuma alteração.')
                print(input('\nPrimir ENTER para continuar.'))
                return lista_jogos # termina aqui a função
             
            print(str_jogo_alterar)
            print(f'\nALTERADO PARA: {jogo_selecionado[0]} | {jogo_selecionado[1]} | {jogo_selecionado[2]}  {jogo_selecionado[3]} - {jogo_selecionado[4]} {jogo_selecionado[5]}\n')   

            # Confirmar ação final 
            confirmar_alterar = input("Confirma a alteração deste jogo? (S/N): ").strip().lower()
            if confirmar_alterar == 's':
                # Adicionar à lista principal
                lista_jogos[indice_jogo_alterar] = jogo_selecionado
                print("\nJogo alterado com sucesso!\n")
                print(input('\nPrimir ENTER para continuar.'))
            else:
                print("Alteração cancelada.")
                return lista_jogos # termina aqui a função
        else:   
            print("Opção inválida.\n")
    else:
        print("Operação cancelada.\n")  
    return lista_jogos     

'''--- Funcao ELIMINAR JOGO PESQUISADO ---
O Algoritmo da ELIMINAR jogo pesquisado:
1 - Pedir Jornada e Equipa (Função pesquisar_jogo --» devolve indice do jogo e string resumo). (opção 0 para sair da função)
    1.1 - Se não encontrar: Mostra mensagem de erro
2 - Se encontrar: Mostrar o jogo ao utilizador.
8 - Perguntar se quer Continuar a apagar jogos?
7 - Se sim, volta para o inicio do algoritmo (opção 0 para sair da função)
Parar (break), porque a lista mudou de tamanho e continuar o loop daria erro.
'''
def eliminar_jogo(lista_jogos):
    indice_jogo_eliminar, str_jogo_eliminar = pesquisar_jogo(lista_jogos)

    if indice_jogo_eliminar == -1:
        print("Nenhum jogo seleccionado.")
        return
    
    print('\n--- APAGAR Jogo ---')
    confirmar_eliminar = input("\nTem a certeza que quer APAGAR este jogo? (S/N): ").strip().lower()

    if confirmar_eliminar == 's':
        lista_jogos.pop(indice_jogo_eliminar)
        print("Jogo apagado com sucesso!")
        input('\nPrimir ENTER para continuar.')
    else:
        print("Operação cancelada.")

    input('\nPrimir ENTER para continuar.')     
    return lista_jogos

''' --- Funcao CONSULTAR TODOS OS JOGOS ---
O Algoritmo da Edição:
1 - Apresentar 1 tabela por jornada
2 - Carregar ENTER para voltar ao menu
'''
def consultar_todos_jogos(lista_jogos):
    validacoes.limpar_ecra()
    print('--- Consultar Todos os Jogos ---\n') 

    print('--- NOTA: jogos por realizar tem "golos" = -1')  
    input("\nPressione ENTER para continuar.")
    if len(lista_jogos) == 0:
        print("Nenhum jogo registado.")
        input("\nPressione ENTER para continuar.")
        return  
    
    # Agrupar os jogos por jornada
    jogos_por_jornada = {} # Vamos criar um dicionário para agrupar os jogos por jornada
    for jogo in lista_jogos: # cada jogo é uma lista [Jornada, Data, Casa, G_Casa, G_Fora, Fora]
        jornada = jogo[0]   # extrair a jornada do jogo
        if jornada not in jogos_por_jornada:    # isto vai criar a chave (Jornada) se não existir
            jogos_por_jornada[jornada] = []     # cria uma lista vazia para essa chave (jornada)
        jogos_por_jornada[jornada].append(jogo) # adiciona o jogo à lista da jornada correspondente

    # Apresentar os jogos agrupados DE CADA jornada (chave do dicionário)
    validacoes.limpar_ecra()
    
    print('--- Consultar Todos os Jogos ---\n')
    print('--- NOTA: jogos por realizar tem "golos" = -1\n')

    for jornada, jogos in jogos_por_jornada.items():
        print(f"\n--- Jornada {jornada} ---")
        for jogo in jogos:
            print(f"  {jogo[1]} - {jogo[2]} vs {jogo[5]} ({jogo[3]}-{jogo[4]})")
    input("\nPressione ENTER para continuar.")   
    return  

'''--- MENU CONSULTAR 
'''
def menu_consultar(lista_jogos):
    while True:
        validacoes.limpar_ecra()

        print("\n" + "="*30)
        print("      LIGA DE FUTEBOL - Menu de Consulta    ")
        print("="*30)
        print("1. Consultar todos os jogos")   
        print("2. Consultar jogo especifico")
        print("0. Voltar ao menu principal")

        try:
            opcao = int(input("Escolha uma opção: "))

            if opcao == 1:
                consultar_todos_jogos(lista_jogos)
            elif opcao == 2:
                pesquisar_jogo(lista_jogos)
            elif opcao == 0:
                break 
            else:
                print("Opção errada!")

        except:
            print("Opção inválida!")        
            input()    

'''--- MENU ElIMINAR 
'''
def menu_eliminar(lista_jogos):
    while True:
        validacoes.limpar_ecra()
        
        print("\n" + "="*30)
        print("      LIGA DE FUTEBOL - Menu de Eliminar    ")
        print("="*30)
        print("1. Eliminar todos os jogos")   
        print("2. Eliminar jogo especifico")
        print("0. Voltar ao menu principal")

        try:
            opcao = int(input("Escolha uma opção: "))

            if opcao == 1:
                eliminar_tudo(lista_jogos)
            elif opcao == 2:
                eliminar_jogo(lista_jogos)
            elif opcao == 0:
                break 
            else:
                print("Opção errada!")

        except:
            print("Opção inválida!")        
            input()    