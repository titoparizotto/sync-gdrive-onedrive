import logging
import os
import traceback
from util import *

from logger import Logger

log = Logger(log_file="out.log", log_level=logging.DEBUG)

class Directory:
    def __init__(self, name, target_directory=None):
        self.name = name
        self.target_directory = target_directory or get_target_dir(self.name)
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
                    if path.is_file() and allow_extention(path.path):
                        #log.info("file -> " + path.path)
                        self.set_files(path)
                    elif path.is_dir():
                        #log.info("subdirectory -> " + path.path)
                        subdirectory = DirectoryBuilder(path.path, get_target_dir(path.path))
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


