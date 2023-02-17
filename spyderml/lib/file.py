from spyderml.lib.detectos import detect


def open_file(filepath):
    try:
        if '~/' in filepath:
            filepath = filepath.replace('~/', detect())
        with open(filepath, 'r') as file:
            lines = file.read().strip()
        return lines
    except FileNotFoundError:
        print(f"File NotFound({filepath})")
        exit()


def save_output(filename, text):
    if '~/' in filename:
        filename = filename.replace('~/', detect())
    with open(filename, '+a') as file:
        file.write(str(text))
        file.write('\n')


def open_headers_file(headers_file):
    if '~/' in headers_file:
        headers_file = headers_file.replace('~/', detect())
    with open(headers_file) as f:
        headers = dict(line.split(': ', 1) for line in f.read().splitlines())
    return headers
