import generalPY

import sys
import os
import hashlib
import datetime
import time
import pickle
import signal

filesDict = dict()
pathGlobal = ''


def interrupt(*args, **kwargs):
    
    global filesDict
    global pathGlobal

    with open(pathGlobal, "wb") as f:
            pickle.dump(filesDict, f)

    print('\n\n[!] Saliendo...')
    sys.exit()

def dataFile(path):

    global filesDict
    global pathGlobal

    fileB = f"./{hashlib.md5(path.encode()).hexdigest()}.pkl"
    pathGlobal = fileB

    if os.path.isfile(fileB):
        with open(fileB, "rb") as f:
            filesDictAux = pickle.load(f)
        files = set([file for file,_ in filesDict.items()] + [file for file,_ in filesDictAux.items()])

        fileStr = f" CHANGES " 
        generalPY.printColors(f'\n{50*"#"}\n{fileStr.center(50, "#")}\n{50*"#"}\n', 'MAGENTA')

        for file in files:
            if file not in filesDictAux:
                fileText = f'[!] NEW FILE: {file} - Hash: {filesDict[file]}'
                generalPY.printColors(fileText, 'GREEN')
                generalPY.create_log(fileText)
            if file not in filesDict:
                fileText = f'[!] DELETED FILE: {file} - Hash: {filesDict[file]}'
                generalPY.printColors(fileText, 'RED')
                generalPY.create_log(fileText)
            if file in filesDict and file in filesDictAux and filesDictAux[file] != filesDict[file]:
                fileText = f'[!] MODIFIED FILE: {file} - Hash PRE: {filesDictAux[file]} - Hash POST: {filesDict[file]}'
                generalPY.printColors(fileText, 'YELLOW')
                generalPY.create_log(fileText)
        filesDict = filesDictAux
    
        
    else:
        with open(fileB, "wb") as f:
            pickle.dump(filesDict, f)

    return None


def compute_file_hash(file_path, algorithm='sha256'):
    """Compute the hash of a file using the specified algorithm."""
    hash_func = hashlib.new(algorithm)

    with open(file_path, 'rb') as file:
        # Read the file in chunks of 8192 bytes
        while chunk := file.read(8192):
            hash_func.update(chunk)

    return hash_func.hexdigest()


def getHashes(path):

    files = os.listdir(path)

    fileStr = f" FILES {str(datetime.datetime.now())} "
    generalPY.printColors(f'{50*"#"}\n{fileStr.center(50, "#")}\n{50*"#"}\n', 'GREEN')
    # Print the files
    for file in files:
        if not os.path.isdir(os.path.join(path, file)):
            hashVar = compute_file_hash(os.path.join(path, file))
            filesDict[file] = hashVar
            print(f'\t[*] File: {file} - Hash: {hashVar}')

def checkHashes(path):

    files = os.listdir(path)

    fileStr = f" CHECK FILES {str(datetime.datetime.now())} " 
    generalPY.printColors(f'\n{50*"#"}\n{fileStr.center(50, "#")}\n{50*"#"}\n', 'CYAN')
    # Print the files
    for file in files:
        if not os.path.isdir(os.path.join(path, file)):
            hashVar = compute_file_hash(os.path.join(path, file))

            if file in filesDict:
                if hashVar != filesDict[file]:
                    fileModified = f'[!] FILE: {file} HA SIDO MODIFICADO'
                    generalPY.printColors(fileModified, 'RED')
                    generalPY.create_log(fileModified)
                    filesDict[file] = hashVar
            else:
                fileCreated = f'[!] FILE: {file} HA SIDO CREADO'
                generalPY.printColors(fileCreated, 'GREEN')
                generalPY.create_log(fileCreated)
                filesDict[file] = hashVar

    pop_list = []
    for file,hashFile in filesDict.items():
        if file not in files:
            fileRemoved = f'[!] FILE: {file} HA SIDO ELIMINADO'
            generalPY.printColors(fileRemoved, 'YELLOW')
            generalPY.create_log(fileRemoved)
            pop_list.append(file)

    for file in pop_list:
        filesDict.pop(file)
    return None




if __name__ == '__main__':

    signal.signal(signal.SIGINT, interrupt)
    args = sys.argv
    route = args[1]

    if not os.path.exists(route):
        print(f'[!] La ruta no es válida. Saliendo del programa...')
        sys.exit()

    getHashes(route)
    dataFile(route)

    while True:
        checkHashes(route)
        time.sleep(30)
