import os
import subprocess
import sys

filename = os.path.abspath("message.txt")

def start_editor(message):
    create(message)
    if (sys.platform == "win32"):
        return edit_windows(message)
    elif (sys.platform == "linux"):
        return edit_linux(message)

def save():
    file = open(filename, "r")
    content = file.read()
    file.close()
    return content

def create(message):
    #escrever o conteudo gerado em um arquivo novo e salvar
    file = open(filename, "w")
    file.write(message)
    file.close()


def edit_windows(message):
    subprocess.run(f"edit {filename}")
    return save()

def edit_linux(message):
    subprocess.run(f"vi {os.path.abspath(filename)}")
    return save()

if __name__ == "__main__":
    aa = start_editor("xablau")
    print(aa)