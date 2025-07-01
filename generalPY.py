
import time
import os
import datetime
import signal
import sys

def prettyPrint(text):

    print(f'[+] {text}')

    return None

def infoPrint(text):

    print(f'[INFO] type: {type(text)} - Value: {text}')

    return None

def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time} seconds to run.")
        return result
    return wrapper

def create_log(text, path='.'):
    date = str(datetime.datetime.now())[:10]
    file = f'{path}/{date}_log.log'

    file_exist = os.path.isfile(file)    
    text = f'{datetime.datetime.now()} || {text}'

    if file_exist:
        with open(file, 'a') as f:
            f.write('\n')
            f.write(text)
            f.close()
    else:
        with open(file, 'w') as f:
            f.write(text)
            f.close()

def create_log_decorator(path):
    print("Inside decorator")

    def inner(func):
        # code functionality here
        print("Inside inner function")
        print("I like", like)

        def wrapper():
            func()

        return wrapper

    # returning inner function
    return inner

def includeSignals():
    signal.signal(signal.SIGINT, interrupt)

def interrupt(*args, **kwargs):

    print('\n\n[!] Saliendo...')
    sys.exit()


def printColors(text: str = '', color: str = 'WHITE', background: str = 'BACKGROUND_BLACK'):

    colors = {
    'BLACK': '\033[30m',
    'RED': '\033[31m',
    'GREEN': '\033[32m',
    'YELLOW': '\033[33m', # orange on some systems
    'BLUE': '\033[34m',
    'MAGENTA': '\033[35m',
    'CYAN': '\033[36m',
    'LIGHT_GRAY': '\033[37m',
    'DARK_GRAY': '\033[90m',
    'BRIGHT_RED': '\033[91m',
    'BRIGHT_GREEN': '\033[92m',
    'BRIGHT_YELLOW': '\033[93m',
    'BRIGHT_BLUE': '\033[94m',
    'BRIGHT_MAGENTA': '\033[95m',
    'BRIGHT_CYAN': '\033[96m',
    'WHITE': '\033[97m',
    'RESET': '\033[0m',
    }

    backGrounds = {
            'BACKGROUND_BLACK': '\033[40m',
    'BACKGROUND_RED': '\033[41m',
    'BACKGROUND_GREEN': '\033[42m',
    'BACKGROUND_YELLOW': '\033[43m', # orange on some systems
    'BACKGROUND_BLUE': '\033[44m',
    'BACKGROUND_MAGENTA': '\033[45m',
    'BACKGROUND_CYAN': '\033[46m',
    'BACKGROUND_LIGHT_GRAY': '\third-party033[47m',
    'BACKGROUND_DARK_GRAY': '\033[100m',
    'BACKGROUND_BRIGHT_RED': '\033[101m',
    'BACKGROUND_BRIGHT_GREEN': '\033[102m',
    'BACKGROUND_BRIGHT_YELLOW': '\033[103m',
    'BACKGROUND_BRIGHT_BLUE': '\033[104m',
    'BACKGROUND_BRIGHT_MAGENTA': '\033[105m',
    'BACKGROUND_BRIGHT_CYAN': '\033[106m',
    'BACKGROUND_WHITE': '\033[107m',
    }

    if color not in colors:
        print(f'[!] NO EXISTE EL COLOR')
    if background not in backGrounds:
        print(f'[!] NO EXISTE EL BACKGROUND')

    print(colors[color] + backGrounds[background] + f"{text}" + colors['RESET'])
