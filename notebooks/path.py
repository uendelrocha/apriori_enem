# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 05:18:36 2023
Updated on Fri May 03 03:39:00 2024

@author: uendel
"""

import sys, os


def read_env_file(file_path):
    env_vars = {}
    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            if line:
                key, value = line.split("=", 1)
                env_vars[key] = value
    return env_vars



def path_join_subdir(
    path: str, foldername: str, create_if_it_not_exists=False, convert_to_dirname=True
):
    r"""
    Função que retorna o caminho completo para a pasta foldername que está dentro do diretório path.
    path: caminho para o diretório
    foldername: nome da pasta
    create_if_it_not_exists: se True, cria o diretório se ele não existir.
    convert_to_dirname: se True, converte foldername para um diretório. Se false, apenas concatena foldername a path.

    Use convert_to_dirname = True para indicar que foldername é um diretório. Neste caso, se path ou foldername não terminar com uma barra, o último nível será tratado como arquivo e será removido da concatenação. 
    Isso é útil para evitar problemas com a barra no final do diretório e/ou para adicionar o diretório à variável de ambiente PATH. 
    A saída será um caminho absoluto sem a barra no final no caso de mais path com mais de um nível, ou com barra no caso de root.

    Use convert_to_dirname = False para indicar que se deseja concatenar path e foldername sem verificar se foldername é um diretório. 
    A saída será um caminho resultante da concatenação path + foldername ou um caminho relativo.

    OBS1: Não é necessário adicionar uma barra no início de foldername. A função já faz isso.

    OBS2: Para indicar que path ou foldername é um diretório, adicione uma barra no final (veja o exemplo 4).

    EXEMPLOS:
    * Exemplo 1: Não usar uma barra no final de path e foldername
    path = 'C:/Users/uendel/Documents'
    foldername = 'Downloads'
    path_join_subdir(path, foldername, False, True)  -> 'C:\\Users\\uendel'
    path_join_subdir(path, foldername, False, False) -> 'C:/Users/uendel/Documents\\Downloads'

    * Exemplo 2: Usar uma barra no final de path
    path = 'C:/Users/uendel/Documents/'
    foldername = 'Downloads'
    path_join_subdir(path, foldername, False, True)  -> 'C:\\Users\\uendel\\Documents'
    path_join_subdir(path, foldername, False, False) -> 'C:/Users/uendel/Documents/Downloads'

    * Exemplo 3: Usar uma barra no final de foldername
    path = 'C:/Users/uendel/Documents'
    foldername = 'Downloads/'
    path_join_subdir(path, foldername, False, True)  -> 'C:\\Users\\uendel\\Downloads'
    path_join_subdir(path, foldername, False, False) -> 'C:/Users/uendel/Documents\\Downloads/'


    * Exemplo 4: Usar uma barra no final de path e de foldername para indicar que são diretórios
    Uso recomendado: indique com uma barra no final de path e foldername para indicar um diretório
    path = 'C:/Users/uendel/Documents/'
    foldername = 'Downloads/'
    path_join_subdir(path, foldername, False, True)  -> 'C:\\Users\\uendel\\Documents\\Downloads'
    path_join_subdir(path, foldername, False, False) -> 'C:/Users/uendel/Documents/Downloads/'


    * Exemplo 5: Aplica o path relativo, sendo './' o diretório corrente, '../' o diretório anterior
    Diretório atual: D:\code\python\ExportarPecas
    path_join_subdir('.', '..', False, True)  -> NotADirectoryError: O diretório "" não existe.
    path_join_subdir('.', '..', False, False) -> '.\\..'

    Diretório atual: D:\code\python\ExportarPecas
    path_join_subdir('.', '../', False, True)  -> 'D:\\code\\python'
    path_join_subdir('.', '../', False, False) -> '.\\../'

    Diretório atual: D:\code\python\ExportarPecas
    path_join_subdir('./', '..', False, True)  -> 'D:\\code\\python\\ExportarPecas'
    path_join_subdir('./', '..', False, False) -> './..'

    Diretório atual: D:\code\python\ExportarPecas
    path_join_subdir('./', '../', False, True)  -> 'D:\\code\\python'
    path_join_subdir('./', '../', False, False) -> './../'

    Diretório atual: D:\code\python\ExportarPecas
    path_join_subdir('..', '.', False, True)  -> NotADirectoryError: O diretório "" não existe.
    path_join_subdir('..', '.', False, False) -> '..\\.'

    Diretório atual: D:\code\python\ExportarPecas
    path_join_subdir('..', './', False, True)  -> 'D:\\code\\python\\ExportarPecas'
    path_join_subdir('..', './', False, False) -> '..\\./'

    Diretório atual: D:\code\python\ExportarPecas
    path_join_subdir('../', '.', False, True)  -> 'D:\\code\\python'
    path_join_subdir('../', '.', False, False) -> '../.'

    Diretório atual: D:\code\python\ExportarPecas
    path_join_subdir('../', './', False, True)  -> 'D:\\code\\python'
    path_join_subdir('../', './', False, False) -> '.././'


    * Exemplo 6: Aplica o path relativo '/' para o diretório raiz (root).
    Diretório atual: D:\code\python\ExportarPecas
    path_join_subdir('/', '.', False, True)  -> 'D:\\'
    path_join_subdir('/', '.', False, False) -> '/.'

    Diretório atual: D:\code\python\ExportarPecas
    path_join_subdir('/', './', False, True)  -> 'D:\\'
    path_join_subdir('/', './', False, False) -> '/./'

    Diretório atual: D:\code\python\ExportarPecas
    path_join_subdir('/', '..', False, True)  -> 'D:\\'
    path_join_subdir('/', '..', False, False) -> '/..'

    Diretório atual: D:\code\python\ExportarPecas
    path_join_subdir('/', '../', False, True)  -> 'D:\\'
    path_join_subdir('/', '../', False, False) -> '/../'

    Diretório atual: D:\code\python\ExportarPecas
    path_join_subdir('/', '/', False, True)  -> 'D:\\'
    path_join_subdir('/', '/', False, False) -> '/'

    """  
    path = os.path.dirname(path) if convert_to_dirname else path
    foldername = os.path.dirname(foldername) if convert_to_dirname else foldername

    # Retorna o caminho completo para a pasta foldername que está dentro do diretório path
    path_subdir = os.path.join(path, foldername)
    # Verifica se path é um diretório
    if not os.path.isdir(path_subdir):
        # Se não for, verifica se é para criar o diretório
        if create_if_it_not_exists:
            # Se for, cria o diretório
            os.makedirs(path_subdir)
        else:  # Se não for, retorna um erro
            raise NotADirectoryError(f'O diretório "{path_subdir}" não existe.')

    return os.path.abspath(path_subdir) if convert_to_dirname else path_subdir


def init():
    global PATH_ROOT
    global PATH_PECAS
    global PATH_PECAS_FILES
    global PATH_PECAS_OUTPUT
    global PATH_PECAS_OUTPUT_DUMP
    global PATH_PECAS_DATASET
    global PATH_PECAS_SQL
    global CHARSET
    
    CHARSET = 'utf-8'
    
    sys.path.append("./")
    env_variables = read_env_file("path.env")

    if "PATH_ROOT" in env_variables:
        PATH_ROOT = env_variables["PATH_ROOT"]
        print("O valor da variável PATH_ROOT é:", PATH_ROOT)
    else:
        print("A variável PATH_ROOT não está definida no arquivo.")
        PATH_ROOT = "."

    PATH_PECAS = path_join_subdir(PATH_ROOT, "pecas_stj/", True, False)
    PATH_PECAS_FILES = path_join_subdir(PATH_ROOT, "__files/pecas_stj/", True, False)
    PATH_PECAS_OUTPUT = path_join_subdir(PATH_PECAS_FILES, "output/", True, False)
    PATH_PECAS_OUTPUT_DUMP = path_join_subdir(PATH_PECAS_OUTPUT, "dump/", True, False)
    PATH_PECAS_DATASET = path_join_subdir(PATH_PECAS_FILES, "dataset/", True, False)
    PATH_PECAS_SQL = path_join_subdir(PATH_PECAS_FILES, "sql/", True, False)

    # Adiciona os diretórios ao path
    sys.path.append(path_join_subdir(PATH_ROOT, "my/"))
    sys.path.append(path_join_subdir(PATH_ROOT, "datalab/"))
    sys.path.append(os.path.join(os.path.dirname(PATH_ROOT), "datalab/dataexplorer/"))
    sys.path.append(os.path.join(os.path.dirname(PATH_ROOT), "datalab/datasources/"))
    sys.path.append(os.path.join(os.path.dirname(PATH_ROOT), "pdfexplorer/"))
    # sys.path.append(os.path.join(os.path.dirname(PATH_ROOT), 'stjiautil/'))
    sys.path.append(os.path.join(os.path.dirname(PATH_ROOT), "pecas_stj/"))
    sys.path.append(os.path.join(os.path.dirname(PATH_ROOT), "quotes/"))

    sys.path = sorted(list(set(sys.path)))

    # os.chdir(PATH_PECAS)
    os.chdir(PATH_ROOT)
    print(f"Diretório de trabalho atual é {os.getcwd()}")

    keychain()


def check_stop_file():
    if os.path.isfile(PATH_PECAS_OUTPUT + "stop"):
        raise RuntimeError("\nArquivo stop encontrado. Saindo...")
        return True
    else:
        return False


def keychain():
    global PATH_KEYCHAIN

    global DB2_CON_FILENAME

    global ORACLE_KEY_FILENAME
    global ORACLE_CON_FILENAME

    global SSTORE_KEY_FILENAME
    global SSTORE_CON_FILENAME
    
    global CORPUS_KEY_FILENAME
    global CORPUS_CON_FILENAME_DEV
    global CORPUS_CON_FILENAME_PRO
    
    PATH_KEYCHAIN = PATH_ROOT + "chaveiro/"

    DB2_CON_FILENAME = PATH_KEYCHAIN + "db2_conn_params.k"

    ORACLE_KEY_FILENAME = PATH_KEYCHAIN + "oracle-2.k"
    ORACLE_CON_FILENAME = PATH_KEYCHAIN + "oracle@cdbpro-leitura_conn-2.k"

    SSTORE_KEY_FILENAME = PATH_KEYCHAIN + "sstore.k"
    SSTORE_CON_FILENAME = PATH_KEYCHAIN + "sstore@svlp-memsql-01_conn.k"
    
    CORPUS_KEY_FILENAME = PATH_KEYCHAIN + "corpus.k"
    CORPUS_CON_FILENAME_DEV = PATH_KEYCHAIN + "corpus@svld-mysql-01_conn.k"
    CORPUS_CON_FILENAME_PRO = PATH_KEYCHAIN + "corpus@svlp-bdenfam-01_conn.k"


if __name__ == "__main__":
    init()
    check_stop_file()
