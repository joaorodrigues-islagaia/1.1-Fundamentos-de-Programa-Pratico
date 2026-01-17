import dados
import estatistica
import validacoes

chave_api = '909f97df86f1442fa9611cc74f773bc2'

# --- Função MENU PRINCIPAL---
def main():

    lista_jogos = []  # Lista para armazenar os jogos na memória. 

    while True:
        validacoes.limpar_ecra()
        print("\n" + "="*30)
        print("      LIGA DE FUTEBOL - Menu Principal     ")
        print("="*30)
        print("1. Introduzir jogo manualmente")         
        print("2. Importar dados (API)")
        print("3. Guardar em Ficheiro")
        print("4. Carregar do Ficheiro")
        print("5. Editar um jogo especifico")
        print("6. MENU Consultas")
        print("7. MENU Eliminar")
        print("8. MENU Estatisticas")
        print("9. Tabela de Classificação")           
        print("0. Sair")
        
        try:
            opcao = int(input("Escolha uma opção: "))
        except:
            print("Opção inválida!")              
            input()
        else:
            if opcao == 1:
                lista_jogos = dados.inserir_jogo_manual(lista_jogos)
            elif opcao == 2:
                lista_jogos = dados.importar_jogos_api(chave_api)
            elif opcao == 3:
                dados.guardar_dados_csv("jogos_premier_league.csv", lista_jogos)
            elif opcao == 4:
                lista_jogos = dados.carregar_dados_csv()
            elif opcao == 5:
                lista_jogos = dados.alterar_jogo(lista_jogos)               
            elif opcao == 6:
                dados.menu_consultar(lista_jogos)
            elif opcao == 7:
                dados.menu_eliminar(lista_jogos)
            elif opcao == 8:
                estatistica.menu_estatisticas(lista_jogos)
            elif opcao == 9:
                estatistica.tabela_classificacao(lista_jogos)
            elif opcao == 0:
                print("Adeus.")
                break 
            else:
                print("Opção errada!")            

# --- Fim Função MENU PRINCIPAL---

main()






