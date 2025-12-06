import os
import sys
import argparse
import subprocess
import requests
from dotenv import load_dotenv
import json

#teste
# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Configura as variáveis de ambiente
API_KEY = os.getenv('API_KEY', '').strip()  # Remove espaços e caracteres extras
GIT_USER_NAME = os.getenv('GIT_USER_NAME')
GIT_USER_EMAIL = os.getenv('GIT_USER_EMAIL')

# Configura o recebimento de argumentos
argumentos = argparse.ArgumentParser(description ='Recebe idioma')
argumentos.add_argument("-i", "-l", "--idioma", "--language", type=str, help="Idioma a ser traduzido", default="Português")
argumentos.add_argument("arquivo", type=str, help="Arquivo a ser comitado", nargs="*", default=".") #nargs: 0 ou n arquivos
args = argumentos.parse_args()

def verif_dir(file_path):
    try:
        if os.path.isfile(file_path):
            #se for arquivo, força a pegar seu diretorio
            file_path = os.path.dirname(os.path.abspath(file_path))
        #deteectar o file_path, sendo diretorio, se é repositório ou nao
        git_dir = subprocess.run(['git', '-C', f'{file_path}', 'rev-parse', '--show-toplevel'], stdout=subprocess.PIPE, text=True, check=True) #tenta pegar diretorio do repositorio git atual
        return git_dir.stdout.strip() #remove quebra de linha
        
    except:
        return os.getcwd() #se nao achar pega o normal

def verificar_variaveis_ambiente():
    """Verifica se todas as variáveis de ambiente necessárias estão configuradas"""
    variaveis = {
        'API_KEY': API_KEY,
        'GIT_USER_NAME': GIT_USER_NAME,
        'GIT_USER_EMAIL': GIT_USER_EMAIL
    }
    
    faltando = [var for var, valor in variaveis.items() if not valor]
    
    if faltando:
        print("❌ As seguintes variáveis de ambiente não estão configuradas:")
        print("\n".join(f"- {var}" for var in faltando))
        print("\nPor favor, copie o arquivo .env.example para .env e configure suas variáveis.")
        return False
    return True

def verificar_repositorio(file_path):
    """Verifica se o diretório atual é um repositório Git"""

    current_dir = verif_dir(file_path)

    print(f"📂 Diretório atual: {current_dir}")

    if not os.path.exists(os.path.join(current_dir, ".git")):
        resposta = input("❓ Não é um repositório Git. Deseja iniciar um projeto Git aqui? ((s/y)/n): ").strip().lower()
        if (resposta == 'y' or resposta == 's'):
            try:
                nome_projeto = os.path.basename(current_dir)

                #inicializa repo no diretorio em que nao foi encontrado git
                subprocess.run(['git', f"init {current_dir}"], check=True)
                subprocess.run([f'git -C {current_dir}', "config", "user.name", GIT_USER_NAME], check=True)
                subprocess.run([f'git -C {current_dir}', "config", "user.email", GIT_USER_EMAIL], check=True)
                
                print(f"✅ Repositório Git iniciado com o nome do projeto: {nome_projeto}")
                return True
            except subprocess.CalledProcessError as e:
                print(f"❌ Erro ao inicializar repositório: {e}")
                return False
        print("❌ Operação cancelada.")
        return False
    return True

def obter_alteracoes(file_path):
    """Obtém as alterações pendentes no Git"""
    try:
        current_dir = current_dir = verif_dir(file_path)

        is_git_repo = os.path.exists(os.path.join(current_dir, ".git"))
        
        # Se não for um repositório git, mostra todo o conteúdo como novo
        if not is_git_repo:
            status = "\n".join(f"?? {f}" for f in os.listdir(current_dir) 
                             if not f.startswith('.') and not f.startswith('__')) #filtro
            if not status:
                print("ℹ️ Nenhum arquivo encontrado para commit.")
                return None
                
            print("📝 Arquivos NOVOS detectados:")
            print(os.path.basename(file_path))
            
            # Usa diff --no-index para mostrar todo o conteúdo como novo
            diff = subprocess.run(["git", "diff", "--no-index", "/dev/null", f"{current_dir}"], # compara com diretorio do arq
                                stdout=subprocess.PIPE, encoding='utf-8', text=True, stderr=subprocess.DEVNULL).stdout.strip()
        
        # Se for um repositório git, verifica alterações
        status = subprocess.run(["git", '-C', f'{current_dir}', "status", "--porcelain", f"{file_path}"], 
                              capture_output=True, encoding='utf-8', text=True).stdout.strip()
        
        if not status:
            print("ℹ️ Nenhuma alteração detectada para commit.")
            return None
        
        print("📝 Alterações detectadas:")
        print(status)
        
        # Se houver arquivos não rastreados (??) no status
        if "??" in status:
            # Adiciona arquivos não rastreados ao index temporariamente
            subprocess.run(["git", "-C", current_dir, "add", "-N", file_path], check=True) #adiciona...
            diff = subprocess.run(["git", "-C", current_dir, "diff", file_path],  #entao pega diferença
                                capture_output=True, encoding='utf-8', text=True).stdout.strip()
            # Reseta o index
            subprocess.run(["git", "-C", current_dir, "reset"], check=True)
        else:
            # Caso contrário, usa diff normal
            diff = subprocess.run(["git", "-C", current_dir, "diff", file_path],  #pega a diferença daquele arquivo
                                capture_output=True, encoding='utf-8', text=True).stdout.strip()
        
        if not diff:
            print("ℹ️ Nenhuma diferença detectada para gerar o descritivo.")
            return None
            
        return diff
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao obter alterações: {e}")
        return None

# configura o prompt a partir do JSON
def get_prompt(diff_text):
    prompt_path = os.path.join(os.path.dirname(__file__), 'prompt.json')
    with open(prompt_path, 'r', encoding='utf-8') as data:
        prompt = json.load(data)
        
        # filtro para substituir palavras
        prompt_text = prompt["prompt"].replace('{getIdioma}', getIdioma()).replace('{diff_text}', diff_text)
    
    return prompt_text
        

def gerar_mensagem_commit(diff_text):
    """Gera uma mensagem de commit usando a API do Gemini"""
    # Lista de modelos para tentar em ordem
    modelos = [
        'gemini-2.5-flash',  # Modelo agradável
        'gemini-2.5-flash-lite',  # Versão mais rápida em resposta
        'gemini-2.5-pro'  # Versão pro
    ]

    prompt = get_prompt(diff_text)
    
    print("🔄 Tentando gerar mensagem com API do Gemini...")
    
    # Limpa a API_KEY para garantir que não tenha caracteres extras
    api_key_limpa = API_KEY.strip().lstrip('=').rstrip('=')
    
    for modelo in modelos:
        try:
            # URL sem query parameter - a key vai no header
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent"
            
            # Headers com a API key no formato correto
            headers = {
                "Content-Type": "application/json",
                "X-goog-api-key": api_key_limpa
            }
            
            payload = {
                "contents": [{
                    "parts": [{
                        "text": prompt
                    }]
                }]
            }
            
            response = requests.post(
                url, 
                headers=headers,
                json=payload,
                timeout=30
            )
            
            # Se receber 400 ou 404, tenta próximo modelo
            if response.status_code in [400, 404]:
                print(f"⚠️  Modelo {modelo} não disponível (erro {response.status_code}). Tentando próximo...")
                continue
            
            # Se receber 429, para de tentar
            if response.status_code == 429:
                print(f"⚠️  Limite de requisições atingido (429) para {modelo}.")
                break
            
            response.raise_for_status()
            
            # Processa a resposta
            data = response.json()
            mensagem = (data.get("candidates", [{}])[0]
                       .get("content", {})
                       .get("parts", [{}])[0]
                       .get("text", "").strip())
            
            if mensagem:
                print(f"✅ Sucesso com modelo: {modelo}")
                print("\n--- Descritivo Gerado ---")
                print(mensagem)
                print("-------------------------\n")
                return mensagem
                
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code if e.response else 0
            if status_code in [400, 404]:
                print(f"⚠️  Modelo {modelo} retornou erro {status_code}. Tentando próximo modelo...")
                continue
            elif status_code == 429:
                print(f"⚠️  Limite de requisições atingido (429) para {modelo}.")
                break
            else:
                print(f"⚠️  Erro HTTP {status_code} com {modelo}.")
                continue
        except Exception as e:
            print(f"⚠️  Erro ao tentar {modelo}: {str(e)[:100]}")
            continue
    
    print("\n❌ Não foi possível gerar mensagem com nenhum modelo do Gemini.")
    print("💡 Usando mensagem padrão: 'Commit automático'")
    return "Commit automático"

# retorna Português se não especificar, caso contrário retorna valor que usuário especificou
def getIdioma(l = args.idioma):
    if str(l).isspace() or not l: #se for string com apenas espaço ou nao tiver conteudo
        raise ValueError(f"{sys.argv[(len(sys.argv)-2)]}: Valor de idioma não pode ser vazio!")
    return l

def criar_commit(mensagem, file_path):
    """Cria um novo commit com a mensagem fornecida"""
    try:
        current_dir = verif_dir(file_path)
        subprocess.run(["git", "-C", current_dir, "add", file_path], check=True)
        subprocess.run(["git", "-C", current_dir, "commit", "-m", mensagem], check=True)
        print("✅ Commit realizado com sucesso!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao criar commit: {e}")
        return False

def main():
    """Função principal do programa"""
    try:
        print("🤖 AutoCommit iniciado...")

        file_path = args.arquivo
        
        # Verifica as variáveis de ambiente
        if not verificar_variaveis_ambiente():
            return

        for file in file_path:
            file = os.path.abspath(file)

            # Verifica o repositório Git
            if not verificar_repositorio(file):
                return

            # Obtém alterações
            alteracoes = obter_alteracoes(file)
            if not alteracoes:
                return
            
            #print(alteracoes) mostra o diff
            
            # Gera mensagem de commit
            mensagem = gerar_mensagem_commit(alteracoes)
            
            # Mostra a mensagem que será usada
            if mensagem == "Commit automático":
                print(f"\n📝 Mensagem que será usada: '{mensagem}'")
            else:
                print(f"\n📝 Mensagem gerada: '{mensagem}'")

            # Confirma com o usuário
            confirmar = input("❓ Deseja usar esta mensagem para o commit? (s/n): ").strip().lower()
            if confirmar != 's':
                print("❌ Commit cancelado.")
                continue

            # Cria o commit
            criar_commit(mensagem, file)

    except KeyboardInterrupt:
        print("\n❌ Operação cancelada pelo usuário.")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")

if __name__ == "__main__":
    main()
