import platform
import getpass


def detect():
    user = getpass.getuser()
    my_os = platform.system()
    if my_os == 'Linux':
        path = '/home/' + user + '/'
    else:
        path = 'C:/Users/' + user + '/'
    return path
