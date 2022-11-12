from spyderml.lib.detectos import detect


def open_file(filepath):
    try:
        with open(filepath, 'r') as file:
            linhas = file.read()
            linhas = linhas.strip()
        linhas = linhas.split('\n')
        return linhas
    except FileNotFoundError:
        print(f"Arquivo não encontrado({filepath})")
        exit()


def save_output(filename, text):
    if '~' in filename:
        filename = filename.split('~/')
        path = detect()
        filename = path+filename[1]
    with open(filename, 'a+') as file:
        file.write(str(text))
        file.write('\n' )