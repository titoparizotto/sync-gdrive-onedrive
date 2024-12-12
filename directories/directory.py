import filecmp
import logging
import os
import shutil
import traceback
import subprocess

from logger import Logger

log = Logger(log_file="out.log", log_level=logging.DEBUG)

class Directory:
    def __init__(self, name, target_directory=None):
        self.name = name
        self.target_directory = target_directory or self.get_target_dir(self.name)
        self.subdirectories = []
        self.files = []

    def __str__(self,level=1):
        indent = "--" * level
        result = f"|{indent}{self.name}\n"
        for file in self.files:
            result += f"|{indent}{file}\n"
        for directory in self.subdirectories:
            result += directory.__str__(level+1)
        return result

    def get_target_dir(self,current_path):
            source_target_list = [["G:\\Meu Drive\\geral", "C:\\Users\\titop\\OneDrive\\Documentos\\geral"],
                    ["G:\\Meu Drive\\fotos_videos", "C:\\Users\\titop\\OneDrive\\Imagens"],
                    ["G:\\Meu Drive\\backup", "C:\\Users\\titop\\OneDrive\\Documentos\\backup"],
                    ["G:\\Meu Drive\\fotos_videos\\00_geral", "C:\\Users\\titop\\OneDrive\\Imagens\\00_geral"]
                    ]
            for index, pair_path in enumerate(source_target_list):
                if str(pair_path[0]) in current_path:
                    target_directory = current_path.replace(source_target_list[index][0], source_target_list[index][1])
                    return target_directory





class DirectoryBuilder:
    def __init__(self, name, target_directory=None):
        self.directory = Directory(name, target_directory)

    def set_root(self, name):
        self.directory.name = name
        return self

    def set_target_diretory(self,target_directory):
        self.directory.target_directory = target_directory
        return self

    def _build_subdirectory(self,current_path):
        try:
            with os.scandir(current_path) as paths:
                for path in paths:
                    if path.is_file():
                        #log.info("file -> " + path.path)
                        self.set_files(path)
                    elif path.is_dir():
                        #log.info("subdirectory -> " + path.path)
                        subdirectory = DirectoryBuilder(path.path,self.directory.get_target_dir(path.path))
                        subdirectory._build_subdirectory(path.path)
                        self.directory.subdirectories.append(subdirectory.directory)
                return self.directory

        except Exception as e:
            log.error(f"Ocorreu um erro {e} ao ler o diretório {subdirectory.directory}"
                      f"\n{traceback.extract_stack()}")
            return

    def build(self):
        if os.path.exists(self.directory.name):
            self.directory = self._build_subdirectory(self.directory.name)
            return self.directory
        else:
            log.error("Diretório raiz informado não existe")
            raise ValueError(f"O caminho '{self.directory.name}' não é um diretório válido.")

    def set_files(self,files):
        self.directory.files.append(files)
        return self

    def sync_directories_files(self, directory):
        self.create_target_directory(directory)
        if len(directory.subdirectories) > 0:
            for subdirectoy in directory.subdirectories:
                self.sync_directories_files(subdirectoy)
        else:
            log.info("Diretório origem: " + directory.name + " -> " + directory.target_directory)
            self.sync_files(directory)
            self.one_drive_free_disk(directory.target_directory)

    def sync_files(self,directory):
        try:
            for file in directory.files:
                target_file = self.get_target_file(file, directory)
                try:
                    if not os.path.exists(target_file):
                        try:
                            log.info("Copiando o arquivo: " + file.name)
                            if target_file is not None:
                                shutil.copy2(file.path, target_file)
                        except Exception as e:
                            log.error("Erro ao copiar o arquivo: " + file.name)

                    elif self.get_file_compare(file, target_file):
                       log.info("Arquivos diferentes")
                       log.info("Copiando o arquivo" + file.name)
                       shutil.copy2(file.path, target_file)
                except Exception as e:
                    log.error("Erro ao copiar o arquivo: " + file.name + f"\n{e}")

        except Exception as e:
            log.error("Erro ao copiar o arquivo: " + file.name + f"\n{e}")

    def create_target_directory(self,directory):
        try:
            if not os.path.exists(directory.target_directory):
                os.mkdir(directory.target_directory)
                log.info("Criado diretório destino:" + directory.target_directory)
        except Exception as e:
            log.erro("Erro ao criar o diretório: " + directory.target_directory)

    def get_target_file(self,file,directory):
        if not directory.target_directory is None:
            return file.path.replace(directory.name, directory.target_directory)
        else:
            return None
    def get_file_compare(self,file,target_file):
        if target_file is not None:
            log.info("Verificando arquivo: " + file.name)
            return filecmp.cmp(file.path, target_file, shallow=False)
        else:
            return False

    def one_drive_free_disk(self, current_path):
        try:
            command = f'attrib +U -P "{current_path}"'
            subprocess.run(command, shell=True, check=True)
            log.info("Liberando espaço em disco para o diretório: "+ command)
        except Exception as e:
            log.error("Erro ao executar comando: " + command)























