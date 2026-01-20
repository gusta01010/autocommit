import os
import subprocess
import sys

filename = os.path.abspath("./message.txt")

def start_editor(message):
    create(message)
    if (sys.platform == "win32"):
        return edit_windows()
    elif (sys.platform == "linux"):
        return edit_linux()

def save():
    #ler e retornar o valor
    file = open(filename, "r")
    content = file.read()
    content = verify(content)
    file.close()
    return content

def verify(content):
    #recursao ate acertar
    while content == "":
        print("Erro inesperado: A mensagem não pode estar vazia!")
        input("Press Enter to continue...")
        if (sys.platform == "win32"):
            subprocess.run(f"edit {filename}")
        elif (sys.platform == "linux"):
            subprocess.run(f"vi {filename}")
        return save()
    return content

def create(message):
    #escrever o conteudo gerado em um arquivo novo e salvar para o editor ler (edit, vim...)
    file = open(filename, "w")
    file.write(message)
    file.close()

def edit_windows():
    subprocess.run(f"edit {filename}")
    return save()

def edit_linux():
    subprocess.run(f"vi {filename}")
    return save()

if __name__ == "__main__":
    aa = start_editor("test")
    print(aa)