import logging
import os
import re
import shutil
import subprocess
from collections import defaultdict
from datetime import datetime
from .Logger import *
from .ConfigManager import *


log = Logger(log_file="log_file" , log_level=logging.INFO)

def allow_extention(file):
    ignored_extention = ConfigManager.get("files.ignored_extensions")
    if os.path.splitext(file)[1][1:] in ignored_extention:
        #log.info(f"Arquivo {file} ignorado!")
        return False
    else:
        return True

def check_duplicated_files(path):
    file_suffix = re.compile(ConfigManager.get("files.duplicated_files_regex"))
    list_files = defaultdict(list)
    duplicated_files = defaultdict(list)

    for root,_,files in os.walk(path):
        for file in files:
            if allow_extention(file):
                file_name = file_suffix.sub("",file).strip()
                path = os.path.join(root, file)
                list_files[file_name].append(path)

    for file_name, path in list_files.items():
        if len(path) > 1:
            duplicated_files[file_name] = path

    for file_name, path in duplicated_files.items():
        log.info(f"#\"{file_name}\"#{"#".join([f'\"{p}\"' for p in path])}")

    #rename_duplicated_files_for_directory(duplicated_files)

def check_original_file_is_updated(file, target_file):
    date_mod_original_file = int(os.path.getmtime(file))
    date_mod_target_file = int(os.path.getmtime(target_file))

    if date_mod_original_file > date_mod_target_file:
        log.info(f"Data arquivo {file.name}: {datetime.fromtimestamp(date_mod_original_file).strftime('%d/%m/%y %H:%M:%S')}"
                 f"-> Data arquivo {target_file} {datetime.fromtimestamp(date_mod_original_file).strftime('%d/%m/%y %H:%M:%S')}")
        return True
    else:
        return False

def create_target_directory(directory):
    try:
        if not os.path.exists(directory.target_directory):
            os.mkdir(directory.target_directory)
            log.info("Criado diretório destino:" + directory.target_directory)
    except Exception as e:
        log.error("Erro ao criar o diretório: " + directory.target_directory)

def get_list_files_updated(directory):
    for file in directory.files:
        target_file = get_target_file(file, directory)
        if os.path.exists(target_file):
            check_original_file_is_updated(file.path,target_file)
        else:
            log.info(f"Arquivo {target_file} não existe!")
    for subdirectory in directory.subdirectories:
        get_list_files_updated(subdirectory)

def get_target_file(file, directory):
    if not directory.target_directory is None:
        return file.path.replace(directory.name, directory.target_directory)
    else:
        return None

def get_target_dir(current_path):
    source_target_list = ConfigManager.get("directory.source_target")
    for index, pair_path in enumerate(source_target_list):
        if str(pair_path[0]) in current_path:
            target_directory = current_path.replace(source_target_list[index][0], source_target_list[index][1])
            return target_directory

def one_drive_free_disk(current_path):
    command = f'attrib +U -P "{current_path}"'
    try:
        subprocess.run(command, shell=True, check=True)
        log.info("Liberando espaço em disco para o diretório: "+ command)
    except Exception as e:
        log.error("Erro ao executar comando: " + command)

def rename_duplicated_files_for_directory(duplicated_files):
    regex = re.compile(ConfigManager.get("files.rename_files_regex"), re.IGNORECASE)
    for file_name, path in duplicated_files.items():
        if regex.match(file_name):
            for p in path:
                new_file_name = f"{os.path.basename(os.path.dirname(p))}_{file_name}"
                new_path = os.path.join(os.path.dirname(p),new_file_name)
                os.rename(p,new_path)
                log.info(f"Arquivo {file_name} renomeado para {new_path}")

def delete_files_from_file():
    to_delete = ConfigManager.get("files.path_to_delete")
    with open(to_delete,"r") as td:
        paths = td.read().splitlines()
    for path in paths:
        os.remove(path)


def sync_directories_files(directory):
    if directory.target_directory is not None:
        create_target_directory(directory)
    if directory.subdirectories is not None:
        for subdirectoy in directory.subdirectories:
            sync_directories_files(subdirectoy)
        else:
            log.info("Diretório origem: " + directory.name + " -> " + (directory.target_directory or "Diretório destino vazio"))
            sync_files(directory)
            one_drive_free_disk(directory.target_directory)

def sync_files(directory):
    try:
        for file in directory.files:
            target_file = get_target_file(file, directory)
            try:
                if not os.path.exists(target_file):
                    try:
                        log.info("Copiando o arquivo: " + file.name)
                        if target_file is not None:
                            shutil.copy2(file.path, target_file)
                    except Exception as e:
                        log.error("Erro ao copiar o arquivo: " + file.name)

                elif not os.path.exists(target_file) or check_original_file_is_updated(file, target_file):
                   log.info("Copiando o arquivo: " + file.path)
                   shutil.copy2(file.path, target_file)
                   #shutil.move(file.path, target_file)
                   one_drive_free_disk(target_file)
            except Exception as e:
                log.error("Erro ao copiar o arquivo: " + file.name + f"\n{e}")

    except Exception as e:
        log.error("Erro ao copiar o arquivo: " + file.name + f"\n{e}")