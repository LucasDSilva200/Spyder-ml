from spyderml.lib.detectos import detect


def open_file(filepath):
    try:
        if '~/' in filepath:
            filepath = filepath.replace('~/',detect())
        with open(filepath, 'r') as file:
            lines = file.read()
            lines = lines.strip()
        lines = lines.split('\n')
        return lines
    except FileNotFoundError:
        print(f"File NotFound({filepath})")
        exit()


def save_output(filename, text):
    if '~/' in filename:
        filename = filename.replace('~/',detect())
    with open(filename, 'a+') as file:
        file.write(str(text))
        file.write('\n')