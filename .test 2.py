import os
import sys
import argparse
import subprocess
import requests
from dotenv import load_dotenv
import json

# Configura o recebimento de argumentos
argumentos = argparse.ArgumentParser(description ='Recebe idioma')
argumentos.add_argument("-i", "-l", "--idioma", "--language", type=str, help="Idioma a ser traduzido", nargs="?", default="Português") #nargs: 0 ou 1 argumentos
argumentos.add_argument("arquivo", type=str, help="Arquivo a ser comitado", nargs="*", default=".") #nargs: 0 ou n arquivos
args = argumentos.parse_args()


def verificar_repositorio(file_path):
    """Verifica se o diretório atual é um repositório Git"""
    try:
        #refeito para deteectar o diretório se é repositório ou nao
        git_dir = subprocess.run(['git', 'rev-parse', '--show-toplevel'], stdout=subprocess.PIPE, text=True, check=True) #tenta pegar diretorio do repositorio git atual
        current_dir=git_dir.stdout.strip() #remove quebra de linha
        
    except:
        current_dir = os.getcwd() #se nao achar pega o normal

    print(f"📂 Diretório atual: {current_dir}")

    if not os.path.exists(os.path.join(current_dir, ".git")):
        resposta = input("❓ Não é um repositório Git. Deseja iniciar um projeto Git aqui? (s/n): ").strip().lower()
        if resposta == 's':
            try:
                nome_projeto = os.path.basename(current_dir)
                subprocess.run(["git", "init"], check=True)
                subprocess.run(["git", "config", "user.name", GIT_USER_NAME], check=True)
                subprocess.run(["git", "config", "user.email", GIT_USER_EMAIL], check=True)
                print(f"✅ Repositório Git iniciado com o nome do projeto: {nome_projeto}")
                return True
            except subprocess.CalledProcessError as e:
                print(f"❌ Erro ao inicializar repositório: {e}")
                return False
        print("❌ Operação cancelada.")
        return False
    return True

def main():
    """Função principal do programa"""
    try:
        print("🤖 AutoCommit iniciado...")
        
        file_path = list(set(args.arquivo))

        for file in file_path:
            print(os.path.abspath(file))

                    # Verifica o repositório Git
            if not verificar_repositorio(file):
                return
        
        
    except KeyboardInterrupt:
        print("\n❌ Operação cancelada pelo usuário.")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")

if __name__ == "__main__":
    main()
    print(args.idioma)
    print(args.arquivo)
