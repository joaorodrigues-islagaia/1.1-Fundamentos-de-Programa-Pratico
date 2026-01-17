# Ficheiro com as funções de validação de campos

import os
from datetime import datetime

# --- Função Auxiliar: LIMPAR ECRÃ ---
def limpar_ecra():
    os.system('cls' if os.name == 'nt' else 'clear')

# --- Função VALIDAR NUMERO INTEIRO
# --- Pede um número repetidamente até o utilizador inserir um valor inteiro válido.
# --- vamos inserir dois parametros MIN e MAX para ele também validar sempre que precisarmos (como no caso da pesquisa ou inserir Jornada)
def ler_inteiro (mensagem_input, min= None, max = None, permite_vazio = False):
    
    while True:

        valor_testar = input(mensagem_input)

        if valor_testar == '' and permite_vazio == True:
            return None
        
        try:
            valor_int = int(valor_testar)

            if (min is not None and valor_int < min) or (max is not None and valor_int > max):
                print(f"Erro: O valor tem de estar entre {min} e {max}.\n")
            
            else:
                return valor_int
        
        except:
            print("Erro: Tens de introduzir um número inteiro válido.\n")


# --- Função VALIDAR TEXTO
# --- Pede um texto e garante que não está vazio.
def ler_texto(mensagem_input, permite_vazio = False):
    while True:
        texto = input(mensagem_input).strip() # .strip() remove espaços extra

        if texto == '' and permite_vazio == True:
            return None

        elif len(texto) > 0: 
            return texto
        
        else:
            print("Erro: Este campo não pode ficar vazio.\n")

# --- Função VALIDAÇÃO DA DATA
# --- Pede uma data e verifica se é válida no formato AAAA-MM-DD.
def ler_data(mensagem_input, permite_vazio = False):
  
    while True:

        valor_testar = input(mensagem_input)

        if valor_testar == '' and permite_vazio == True:
            return None

        try:
            valor_testar = valor_testar
            # Tenta converter o texto numa data real
            datetime.strptime(valor_testar, '%Y-%m-%d')
            return valor_testar
        
        except ValueError:
            print("Erro: Data inválida! Usa o formato AAAA-MM-DD (ex: 2026-01-30).\n")